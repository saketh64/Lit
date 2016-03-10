import threading
import traceback
import sys

from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO,rooms

from Core import Song, User, Party, search_youtube
from sessions import *

"""
STRUCTURE:
    Client:
        user_id (cookie)
        party_name (url)
    Server:
        parties (party_name to Party obj)
            Party
                party_name
                users (user_id to User obj)
                    User
                        user_id
                        emit_id
                hosts
                queue
                    Song
                        title
                        url
                        upvotes
                            user_id
                        downvotes
                            user_id
                now_playing
"""

parties = {} # global mapping of party names to party objects

app = Flask(__name__, static_url_path="/static")

# Read in secret key for Flask from local text file
f = open("flask_key.txt")
app.config['SECRET_KEY'] = f.readline()
f.close()

socketio = SocketIO(app)


#########################################
# ENDPOINTS
#########################################

@app.route('/')
def get_landing_page():
    return render_template('index.html')


@app.route('/<party_name>')
def get_party_page(party_name):
    global parties
    new_user = False

    # get user info
    user_id = request.cookies.get('user_id')
    if user_id == None:
        user_id = get_random_user_id()
        new_user = True
        print "NEW connection, user_id=", user_id
    else:
        print "Repeated connection, user_id=", user_id

    # make new party if needed
    if party_name not in parties:
        parties[party_name] = Party(party_name, user_id)

    party = parties[party_name]

    # add user to party if needed
    if user_id not in party.users:
        party.users[user_id] = User(user_id)

    # render host or user page
    if user_id in party.hosts:
        resp = make_response(render_template('nowplaying.html'))
    else:
        if party.now_playing == None:
            now_playing_title = "No song is playing."
        else:
            now_playing_title = party.now_playing.title
        resp = make_response(render_template('guest.html',queue=party.get_queue_json(party.users[user_id]),now_playing_title=now_playing_title))

    if new_user:
        resp.set_cookie('user_id', user_id)

    return resp

#########################################
# HANDLERS FOR SOCKET MESSAGES FROM CLIENTS
#########################################

@socketio.on('search')
def handle_search(message):
    party, user, error = init_socket_event(message)
    if error: return

    results = search_youtube(message[u"query"])
    socketio.emit('search_results', {
        "search_results" : results
    }, room=user.emit_id)


@socketio.on('add')
def handle_add(message):
    party, user, error = init_socket_event(message)
    if error: return

    party.add_song(user, message['song_url'], message['title'])
    emit_queue(party)


@socketio.on('upvote')
def handle_upvote(message):
    party, user, error = init_socket_event(message)
    if error: return

    party.upvote_song(user, message['song_url'])
    emit_queue(party)


@socketio.on('downvote')
def handle_downvote(message):
    party, user, error = init_socket_event(message)
    if error: return

    party.downvote_song(user, message['song_url'])
    emit_queue(party)


@socketio.on('on_connect')
def handle_user_connection(message):
    party, user, error = init_socket_event(message)
    if error: return

    user.emit_id = rooms()[0]


@socketio.on('song_end')
def next_song(message):
    party, user, error = init_socket_event(message)
    if error: return

    party.now_playing = None
    party.reorder_queue()
    emit_nowplaying(party)
    emit_queue(party)


#########################################
# METHODS FOR EMITTING MESSAGES TO CLIENTS
#########################################

def emit_queue(party):
    # emit the queue to each user individually
    for user_id, user in party.users.iteritems():
        queue_json = party.get_queue_json(user)
        print "Emitting a list update: # of songs=", len(queue_json)
        socketio.emit('update_list',
                      {
                          "queue": queue_json
                      },room=user.emit_id)


def emit_nowplaying(party):
    for user_id, user in party.users.iteritems():
        if party.now_playing is not None:
            socketio.emit('new_song', party.now_playing.get_json(), room=user.emit_id)
        else:
            socketio.emit('new_song', None, room=user.emit_id)


#########################################
# HELPER METHODS
#########################################

def init_socket_event(message):
    global parties

    party_name = parse_party_from_url(message['party_url'])
    user_id = request.cookies.get('user_id')
    if error_check(party_name, user_id):
        return None, None, True
    else:
        return parties[party_name], parties[party_name].users[user_id], False


def parse_party_from_url(party_url):
    # Wilson's going to castrate me when he sees that I didn't use a regex lel
    # basically this avoids HTML anchors, then removes trailing slashes, then splits on slashes and returns the last item
    # we should probably rewrite this (or find a better way of getting the party_name than sending the url over from the frontside)
    return party_url.split('#')[0].rstrip('/').split('/')[-1]


def error_check(party_name, user_id):
    global parties

    if party_name not in parties:
        print "ERROR: party_name not found. Leaving function early."
        # this whole thing is needed to print the stack trace
        try:
            raise Exception
        except Exception:
            traceback.print_tb(sys.exc_info()[2])
        return True

    if user_id not in parties[party_name].users:
        print "ERROR: user_id not found. Leaving function early."
        try:
            raise Exception
        except Exception:
            traceback.print_tb(sys.exc_info()[2])
        return True

    return False


#########################################
# MAIN ENTRY POINT OF FLASK APP
#########################################

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
