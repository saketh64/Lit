import threading

from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO


from Core import Song, User, Action, search_youtube
from sessions import *


# queue is a list of Song objects, ordered by score
queue = []

# a Song object, the currently playing song
now_playing = None

# IP of the user currently on nowplaying.html
# We only allow one user at a time, because this page plays audio
# We'll track connections with a heartbeat
nowplaying_ip = None

heartbeat_response_received = False


def get_queue_json():
    global queue
    """
    :return: a JSON object to send to the client
    """
    result = []
    for song in queue:
        result.append(song.get_json())
    return result



def update_queue_order():
    global queue, now_playing
    queue.sort(key=lambda song: song.score(), reverse=True)

    if now_playing == None:
        now_playing = queue[0]
        if len(queue) >= 2:
            queue = queue[1:]
        else:
            queue = []
            socketio.emit('new_song', now_playing.get_json(),broadcast=True)
            emit_update_list()


app = Flask(__name__, static_url_path="/static")

# what is this
app.config['SECRET_KEY'] = 'sekrit!'

socketio = SocketIO(app)



#########################################
# ENDPOINTS
#########################################


@app.route('/')
def get_landing_page():
    return render_template('index.html')


@app.route('/nowplaying')
def get_nowplaying_page():
    global nowplaying_ip
    if nowplaying_ip == None:
        nowplaying_ip = User(request.remote_addr)
        threading.Timer(2, nowplaying_send_heartbeat).start()
        threading.Timer(1, emit_new_nowplaying_song).start()
        return render_template('nowplaying.html')
    else:
        print "Someone tried to connect to nowplaying.html, but there's already a connection."
        return "Can't connect - there is already a user on the Now Playing screen."

@app.route('/user')
def get_user_page():
    resp = make_response(render_template('guest.html',queue=get_queue_json()))

    user_id = request.cookies.get('user_id')

    if user_id == None:
        user_id = get_random_user_id()
        resp.set_cookie('user_id', user_id)
        users.append(User(user_id))
        print "NEW connection, user_id=", user_id
    else:
        print "Repeated connection, user_id=", user_id

        if not does_user_exist(user_id):
            print "Adding user to the users list - they weren't there for some reason. (likely debugging)"
            users.append(User(user_id))

    # threading.Timer(1, emit_update_list).start()
    threading.Timer(1,emit_now_playing_song_title).start()
    return resp


#########################################
# NOW PLAYING HEARTBEAT METHODS
#########################################


def nowplaying_send_heartbeat():
    global heartbeat_response_received

    socketio.emit('heartbeat_to_client', None, broadcast=True)
    heartbeat_response_received = False
    threading.Timer(0.5, nowplaying_timeout).start()


@socketio.on('heartbeat_to_server')
def nowplaying_receive_heartbeat(message):
    global heartbeat_response_received

    heartbeat_response_received = True
    threading.Timer(0.5, nowplaying_send_heartbeat).start()


def nowplaying_timeout():
    global nowplaying_ip
    if heartbeat_response_received == False:
        nowplaying_ip = None
        print "Now Playing user has disconnected."


#########################################
# HANDLERS FOR SOCKET MESSAGES FROM CLIENTS
#########################################


@socketio.on('search')
def handle_search(message):
    user_id = request.cookies.get('user_id')
    search_results = search_youtube(message[u"query"])
    emit_search_results({
      "user_id" : user_id,
      "search_results" : search_results
    })


@socketio.on('add')
def handle_add(message):
    global queue

    user_id = request.cookies.get('user_id')

    title = message[u"title"]
    url = message[u"url"]

    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) > 0:
        print "Song has already been added!"
    else:
        print "Adding a new song with title '%s'" % title
        queue.append(
            Song(title, url)
        )
        get_user(user_id).add_song(url)
        get_user(user_id).add_action(url, Action.UPVOTE)
        update_queue_order()
        if now_playing == None:
            next_song()
        emit_update_list()


@socketio.on('upvote')
def handle_upvote(message):
    user_id = request.cookies.get('user_id')

    url = message[u"url"]
    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) != 1:
        print "Couldn't upvote."
    else:
        upvoted_song = songs_with_url[0]

        this_user = get_user(user_id)

        # the user can't upvote this song again!
        if this_user.has_upvoted(upvoted_song.url):
            print "User tried to upvote song '%s' again - ignoring." % upvoted_song.title
            return


        # if the user had previously downvoted, remove that downvote
        if this_user.has_downvoted(upvoted_song.url):
            this_user.remove_action(upvoted_song.url, Action.DOWNVOTE)
            upvoted_song.downvotes -= 1

        upvoted_song.upvotes += 1
        print "Set '%s' upvotes to %d" % (songs_with_url[0].title, songs_with_url[0].upvotes)
        this_user.add_action(upvoted_song.url, Action.UPVOTE)
        update_queue_order()
        emit_update_list()


@socketio.on('downvote')
def handle_downvote(message):
    user_id = request.cookies.get('user_id')

    url = message[u"url"]
    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) != 1:
        print "Couldn't downvote."
    else:
        downvoted_song = songs_with_url[0]

        this_user = get_user(user_id)

        # the user can't downvote this song again!
        if this_user.has_downvoted(downvoted_song.url):
            print "User tried to downvote song '%s' again - ignoring." % downvoted_song.title
            return

        # if the user had previously upvoted, remove that upvote
        if this_user.has_upvoted(downvoted_song.url):
            this_user.remove_action(downvoted_song.url, Action.UPVOTE)
            downvoted_song.upvotes -= 1

        downvoted_song.downvotes += 1
        print "Set '%s' downvotes to %d" % (songs_with_url[0].title, songs_with_url[0].downvotes)
        this_user.add_action(downvoted_song.url, Action.DOWNVOTE)
        update_queue_order()
        emit_update_list()


######################
# Events for the Now Playing page
######################
def nowplaying_send_heartbeat():
    global heartbeat_response_received

    socketio.emit('heartbeat_to_client', None, broadcast=True)
    heartbeat_response_received = False
    threading.Timer(0.5, nowplaying_timeout).start()


@socketio.on('heartbeat_to_server')
def nowplaying_receive_heartbeat(message):
    global heartbeat_response_received

    heartbeat_response_received = True
    threading.Timer(0.5, nowplaying_send_heartbeat).start()


def nowplaying_timeout():
    global nowplaying_ip
    if heartbeat_response_received == False:
        nowplaying_ip = None
        print "Now Playing user has disconnected."


@socketio.on('song_end')
def next_song(message):
    global queue, now_playing
    now_playing = None
    if len(queue) > 0:
        now_playing = queue[0]
        if len(queue) >= 2:
            queue = queue[1:]
        else:
            queue = []
    emit_new_nowplaying_song()
    emit_update_list()


#########################################
# METHODS FOR EMITTING MESSAGES TO CLIENTS
#########################################

def emit_update_list():
    global users

    queue_json = get_queue_json()
    print "Emitting a list update: # of songs=", len(queue_json)
    activity_json = get_all_user_activity_json()
    socketio.emit('update_list',
                  {
                      "queue": queue_json,
                      "activity": activity_json
                  })


def emit_search_results(search_results):
    socketio.emit('search_results', search_results, broadcast=True)

def emit_now_playing_song_title():
    if now_playing is not None:
        socketio.emit('now_playing_song_title', now_playing.get_json(),broadcast=True)
    else:
        socketio.emit('now_playing_song_title', None,broadcast=True)

def emit_new_nowplaying_song():
    if now_playing is not None:
        socketio.emit('new_song', now_playing.get_json(),broadcast=True)
    else:
        socketio.emit('new_song', None,broadcast=True)


#########################################
# MAIN ENTRY POINT OF FLASK APP
#########################################

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
