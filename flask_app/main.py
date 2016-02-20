import threading

from flask import Flask, render_template, request
from flask_socketio import SocketIO

from Core import Song, User, Action, search_youtube



# queue is a list of Song objects, ordered by score
queue = []

# a Song object, the currently playing song
now_playing = None

users = []

# IP of the user currently on nowplaying.html
# We only allow one user at a time, because this page plays audio
# We'll track connections with a heartbeat
nowplaying_ip = None

heartbeat_response_received = False


def get_user(ip):
    for user in users:
        if user.ip_addr == ip:
            return user


def get_queue_json():
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


app = Flask(__name__, static_url_path="/static")

# what is this
app.config['SECRET_KEY'] = 'sekrit!'

socketio = SocketIO(app)


@app.route('/')
def get_landing_page():
    return render_template('index.html')


@app.route('/nowplaying')
def get_nowplaying_page():
    global nowplaying_ip
    if nowplaying_ip == None:
        nowplaying_ip = User(request.remote_addr)
        threading.Timer(2, nowplaying_send_heartbeat).start()
        return render_template('nowplaying.html')
    else:
        print "Someone tried to connect to nowplaying.html, but there's already a connection."
        return "Can't connect - there is already a user on the Now Playing screen."


@app.route('/host')
def get_host_page():
    connected_user = User(request.remote_addr)
    if get_user(connected_user) is None:
        users.append(connected_user)
    return render_template("host.html")


@app.route('/user')
def get_user_page():
    connected_user = User(request.remote_addr)
    if get_user(connected_user) is None:
        users.append(connected_user)
    threading.Timer(1, emit_update_list).start()
    return render_template('guest.html')


@socketio.on('search')
def handle_search(message):
    search_results = search_youtube(message[u"query"])
    emit_search_results(search_results)


@socketio.on('add')
def handle_add(message):
    title = message[u"title"]
    url = message[u"url"]

    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) > 0:
        print "Song has already been added!"
    else:
        queue.append(
            Song(title, url)
        )
        get_user(request.remote_addr).add_song(url)
        get_user(request.remote_addr).add_action(url, Action.UPVOTE)
        update_queue_order()
        if now_playing == None:
            next_song()
        emit_update_list()


@socketio.on('upvote')
def handle_upvote(message):
    url = message[u"url"]
    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) != 1:
        print "Couldn't upvote."
    else:
        upvoted_song = songs_with_url[0]
        upvoted_song.upvotes += 1
        print "Set '%s' upvotes to %d" % (songs_with_url[0].title, songs_with_url[0].upvotes)
        get_user(request.remote_addr).add_action(upvoted_song.url, Action.UPVOTE)
        update_queue_order()
        emit_update_list()


@socketio.on('downvote')
def handle_downvote(message):
    url = message[u"url"]
    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) != 1:
        print "Couldn't downvote."
    else:
        downvoted_song = songs_with_url[0]
        downvoted_song.downvotes += 1
        print "Set '%s' downvotes to %d" % (songs_with_url[0].title, songs_with_url[0].downvotes)
        get_user(request.remote_addr).add_action(downvoted_song.url, Action.DOWNVOTE)
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
def next_song():
    global queue, now_playing
    now_playing = None
    if len(queue) > 0:
        now_playing = queue[0]
        if len(queue) >= 2:
            queue = queue[1:]
        else:
            queue = []
        socketio.emit('new_song', now_playing.get_json())


######################
# Emitting events to clients
######################

def emit_update_list():
    socketio.emit('update_list', get_queue_json(), broadcast=True)


def emit_search_results(search_results):
    socketio.emit('search_results', search_results, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
