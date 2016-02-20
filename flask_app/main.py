from flask import Flask, render_template,request
from flask_socketio import SocketIO

from Core import Song,User,Action
from youtube_search import search_youtube


# queue is a list of Song objects, ordered by score
queue = []

users = []

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

@app.route('/')
def get_page():
    connected_user = User(request.remote_addr)
    if get_user(connected_user) is None:
        users.append(connected_user)
    return render_template('index.html')

    return render_template('guest.html')

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