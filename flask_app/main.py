from flask import Flask, render_template,request
from flask_socketio import SocketIO
import threading

from Core import Song,User,Action
from youtube_search import search_youtube


# queue is a list of Song objects, ordered by score
queue = []

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
    queue.sort(key=lambda song: song.score(), reverse=True)



app = Flask(__name__,static_url_path="/static")

# what is this
app.config['SECRET_KEY'] = 'sekrit!'

socketio = SocketIO(app)

'''
@app.route('/host/')
def hello(name=None):
    return render_template('host.html', name=name)
'''

@app.route('/guest')
def get_guest_page():
    connected_user = User(request.remote_addr)
    if get_user(connected_user) is None:
        users.append(connected_user)
    return render_template('index.html')


def nowplaying_send_heartbeat():
    global heartbeat_response_received

    socketio.emit('heartbeat_to_client', None, broadcast=True)
    heartbeat_response_received = False
    threading.Timer(0.5, nowplaying_timeout).start()

@socketio.on('heartbeat_to_server')
def nowplaying_receive_heartbeat(message):
    global heartbeat_response_received

    heartbeat_response_received = True
    threading.Timer(0.5,nowplaying_send_heartbeat).start()


def nowplaying_timeout():
    global nowplaying_ip
    if heartbeat_response_received == False:
        nowplaying_ip = None
        print "Now Playing user has disconnected."



@app.route('/nowplaying')
def get_nowplaying_page():
    global nowplaying_ip
    if nowplaying_ip == None:
        nowplaying_ip = User(request.remote_addr)
        threading.Timer(2,nowplaying_send_heartbeat).start()
        return render_template('nowplaying.html')
    else:
        print "Someone tried to connect to nowplaying.html, but there's already a connection."
        return "Can't connect - there is already a user on the Now Playing screen."


@socketio.on('search')
def handle_search(message):
    search_results = search_youtube(message[u"query"])
    emit_search_results(search_results)

@socketio.on('add')
def handle_add(message):
    title=message[u"title"]
    url=message[u"url"]

    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) > 0:
        print "Song has already been added!"
    else:
        queue.append(
            Song(title,url)
        )
        get_user(request.remote_addr).add_song(url)
        get_user(request.remote_addr).add_action(url,Action.UPVOTE)
        update_queue_order()
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
        print "Set '%s' upvotes to %d" % (songs_with_url[0].title,songs_with_url[0].upvotes)
        get_user(request.remote_addr).add_action(upvoted_song.url,Action.UPVOTE)
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
        print "Set '%s' downvotes to %d" % (songs_with_url[0].title,songs_with_url[0].downvotes)
        get_user(request.remote_addr).add_action(downvoted_song.url,Action.DOWNVOTE)
        update_queue_order()
        emit_update_list()

def emit_update_list():
    socketio.emit('update_list', get_queue_json(), broadcast=True)

def emit_search_results(search_results):
    socketio.emit('search_results', search_results, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)