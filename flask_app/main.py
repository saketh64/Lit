import threading

from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO,rooms

from Core import Song, User, Party, search_youtube
from sessions import *


#########################################
# ~~~~~~~~~~~~~STRUCTURE~~~~~~~~~~~~~~~ #
#   Client:
#       user_id (cookie)
#       party_name (url)
#   Server:
#       parties (party_name to Party obj)
#           Party
#               party_name
#               users (user_id to User obj)
#                   User
#                       user_id
#                       emit_id
#               hosts
#               queue
#                   Song
#                       title
#                       url
#                       upvotes
#                           user_id
#                       downvotes
#                           user_id
#
#########################################


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

    # get user info
    user_id = request.cookies.get('user_id')
    if user_id == None:
        user_id = get_random_user_id()
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
        return render_template('nowplaying.html')
    else:
        if party.now_playing == None:
            now_playing_title = "No song is playing."
        else:
            now_playing_title = party.now_playing.title
        return make_response(render_template('guest.html',queue=party.get_queue_json(party.users[user_id]),now_playing_title=now_playing_title))


#########################################
# HANDLERS FOR SOCKET MESSAGES FROM CLIENTS
#########################################

@socketio.on('search')
def handle_search(message):
    party, user, error = init_socket_event(message, 'handle_search')
    if error: return

    socketio.emit('search_results', {
        "search_results" : search_youtube(message['query'])
    }, room=user.emit_id)


@socketio.on('add')
def handle_add(message):
    party, user, error = init_socket_event(message, 'handle_add')
    if error: return

    party.add_song(user, message['song_url'], message['title'])
    emit_queue(party)


@socketio.on('vote')
def handle_vote(message):
    party, user, error = init_socket_event(message, 'handle_vote')
    if error: return

    party.vote(user, message['song_url'], message['dir'])
    emit_queue(party)


@socketio.on('connect')
def handle_user_connection(message):
    party, user, error = init_socket_event(message, 'handle_user_connection')
    if error: return

    user.emit_id = rooms()[0]


@socketio.on('song_end')
def next_song(message):
    global parties

    party_name = parse_party_from_url(message['party_url'])

    if party_name not in parties:
        print "ERROR: in next_song, either parse_party_from_url fucked up or something went terribly wrong."
        return

    parties[party_name].now_playing = None
    parties[party_name].update_queue_order()
    emit_nowplaying(parties[party_name])
    emit_queue(parties[party_name])


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

def init_socket_event(message, source):
    global parties

    party_name = parse_party_from_url(message['party_url'])
    user_id = request.cookies.get('user_id')
    if error_check(party_name, user_id, source):
        return None, None, True
    else:
        return parties[party_name], parties[party_name].users[user_id], False


def parse_party_from_url(party_url):
    # Wilson's going to castrate me when he sees that I didn't use a regex lel
    # basically this avoids HTML anchors, then removes trailing slashes, then splits on slashes and returns the last item
    # we should probably rewrite this (or find a better way of getting the party_name than sending the url over from the frontside)
    return party_url.split('#')[0].rstrip('/').split('/')[-1]


def error_check(party_name, user_id, source):
    global parties

    if party_name not in parties:
        print "ERROR: party_name not found in function: " + source + ". Leaving function early."
        return True
    if user_id not in parties[party_name].users:
        print "ERROR: user_id not found in function: " + source + ". Leaving function early."
        return True
    return False


#########################################
# MAIN ENTRY POINT OF FLASK APP
#########################################

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=True)
