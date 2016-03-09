class Party:

    def __init__(self, party_name, host_id):
        self.party_name = party_name
        self.hosts = [host_id]
        self.users = {host_id: User(host_id)}
        self.now_playing = None
        self.queue = []


    def add_song(self, user, song_url, title):
        if any(song.url == song_url for song in self.queue)
            print "Song has already been added!"
        else:
            print "Adding a new song with title '%s'" % title
            self.queue.append(
                Song(title, song_url, user.user_id)
            )
            self.update_queue_order()


    def handle_vote(self, user, song_url, dir):
        song = next((song for song in queue if song.url == song_url), None)

        # check for errors
        if song == None:
            print "ERROR: Song URL not found."
            return

        if dir == 'up':
            # avoid double voting
            if user.user_id in song.upvotes:
                print "User tried to upvote song '%s' again - ignoring." % song.title
                return
            song.upvotes.append(user.user_id)
            # remove user's downvote if there
            song.downvotes.remove(user.user_id)
        else:
            # avoid double voting
            if user.user_id in song.downvotes:
                print "User tried to downvote song '%s' again - ignoring." % song.title
                return
            song.downvotes.append(user.user_id)
            # remove user's downvote if there
            song.upvotes.remove(user.user_id)

        self.update_queue_order()


    def get_queue_json(self, user):
        """
        user is used to give the user THEIR particular vote data
        :return: a JSON object to send to the client
        """
        result = []
        for song in self.queue:
            result.append(song.get_json(user.user_id))
        return result

    def update_queue_order(self):
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
