from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)

# what is this
app.config['SECRET_KEY'] = 'sekrit!'

socketio = SocketIO(app)


@app.route('/host/')
def hello(name=None):
    return render_template('host.html', name=name)


@app.route('/guest/')
def hello(name=None):
    return render_template('host.html', name=name)


@socketio.on('upvote')
def handle_message(message):
    print "RECEIVED:\n", message


@socketio.on('downvote')
def handle_message(message):
    print "RECEIVED:\n", message


@socketio.on('search')
def handle_message(message):
    print "RECEIVED:\n", message


@socketio.on('add')
def handle_message(message):
    print "RECEIVED:\n", message


if __name__ == "__main__":
    socketio.run(app)