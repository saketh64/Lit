from flask import Flask, render_template,request
from flask_socketio import SocketIO

from Core.song import Song


# queue is a list of Song objects, ordered by score
queue = []


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



app = Flask(__name__)

# what is this
app.config['SECRET_KEY'] = 'sekrit!'

socketio = SocketIO(app)

'''
@app.route('/host/')
def hello(name=None):
    return render_template('host.html', name=name)
'''

@app.route('/guest/')
def get_page():
    print request.remote_addr
    return render_template('guest.html')


@socketio.on('add')
def handle_add(message):
    print request.remote_addr
    title=message[u"title"]
    url=message[u"url"]

    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) > 0:
        print "Song has already been added!"
    else:
        queue.append(
            Song(title,url)
        )

@socketio.on('upvote')
def handle_upvote(message):
    url = message[u"url"]
    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) != 1:
        print "Couldn't upvote."
    else:
        songs_with_url[0].upvotes += 1
        print "Set '%s' upvotes to %d" % (songs_with_url[0].title,songs_with_url[0].upvotes)
        update_queue_order()
        emit_update_list()

@socketio.on('downvote')
def handle_downvote(message):
    url = message[u"url"]
    songs_with_url = filter(lambda x: x.url == url, queue)

    if len(songs_with_url) != 1:
        print "Couldn't downvote."
    else:
        songs_with_url[0].downvotes += 1
        print "Set '%s' downvotes to %d" % (songs_with_url[0].title,songs_with_url[0].downvotes)
        update_queue_order()
        emit_update_list()

def emit_update_list():
    socketio.emit('update_list', get_queue_json(), broadcast=True)

def emit_search_results(search_results):
    socketio.emit('search_results', search_results, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)