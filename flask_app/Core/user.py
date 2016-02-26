class User:
    """
    Fields:
        ip_addr (str)
            IP address of the user (public IP?)
        activity (list)
            What has the user upvoted/downvoted?
        added_songs (list)
            What songs has the user added?
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.added_songs = []

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


class Action:
    UPVOTE = 0
    DOWNVOTE = 1
