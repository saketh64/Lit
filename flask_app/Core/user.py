class User:
    """
    Fields:
        user_id
            The user's ID - should be persistent across sessions, because it'll be stored as a cookie client side.
        room_id
            The session ID - new every time the user refreshes. Used to emit socket events JUST to that user.
        added_songs (list)
            Songs added by the user
            (note: don't think this is currently being used)
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.added_songs = []

    def set_room_id(self,room_id):
        self.room_id = room_id

    def has_upvoted(self,song):
        return (self.user_id in song.upvotes)

    def has_downvoted(self,song):
        return (self.user_id in song.downvotes)

    def upvote(self,song):
        song.upvotes.append(self.user_id)
        if self.user_id in song.downvotes:
            song.downvotes.remove(self.user_id)

    def downvote(self,song):
        song.downvotes.append(self.user_id)
        if self.user_id in song.upvotes:
            song.upvotes.remove(self.user_id)

    def add_song(self, song_url):
        self.added_songs.append(song_url)
