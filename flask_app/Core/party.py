from user import User
from song import Song

"""
PUBLIC ATTRIBUTES:
    party_name
    hosts[user_id]
    users\{user_id: User\}
    Song now_playing
    queue[Song]
PUBLIC METHODS:
    add_song(User, song_url, title)
    upvote_song(User, song_url)
    downvote_song(User, song_url)
    get_queue_json(User)
        returns list of JSON formatted song data
PRIVATE METHODS:
    reorder_queue()
"""

class Party:
    def __init__(self, party_name, host_id):
        self.party_name = party_name
        self.hosts = [host_id]
        self.users = {host_id: User(host_id)}
        self.now_playing = None
        self.queue = []


    def add_song(self, user, song_url, title):
        if any(song.url == song_url for song in self.queue):
            print "Song has already been added!"
        else:
            print "Adding a new song with title '%s'" % title
            self.queue.append(
                Song(title, song_url, user.user_id)
            )
            self.reorder_queue()


    def upvote_song(self, user, song_url):
        song = next((song for song in self.queue if song.url == song_url), None)

        # check for errors
        if song == None:
            print "ERROR: Song URL not found."
            return

        # avoid double voting
        if user.user_id in song.upvotes:
            print "User tried to upvote song '%s' again - ignoring." % song.title
            return

        song.upvotes.append(user.user_id)
        song.downvotes.remove(user.user_id) # remove user's downvote if there

        self.reorder_queue()


    def downvote_song(self, user, song_url):
        song = next((song for song in self.queue if song.url == song_url), None)

        # check for errors
        if song == None:
            print "ERROR: Song URL not found."
            return

        # avoid double voting
        if user.user_id in song.downvotes:
            print "User tried to upvote song '%s' again - ignoring." % song.title
            return

        song.downvotes.append(user.user_id)
        song.upvotes.remove(user.user_id) # remove user's downvote if there

        self.reorder_queue()


    def get_queue_json(self, user):
        # user is used to give the user THEIR particular vote data
        return [song.get_json(user.user_id) for song in self.queue]


    def reorder_queue(self):
        # if needed, update now_playing BEFORE reordering the queue
        # sacrifices accuracy for user experience
        # (it would be jarring for the user if the song ended and the "up next" song didn't play next
        # 99% of the time it won't matter
        if self.now_playing == None:
            self.now_playing = self.queue.pop(0)

        self.queue.sort(key=lambda song: song.score(), reverse=True)
