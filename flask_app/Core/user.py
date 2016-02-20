class User:
    """
    Fields:
        ip_addr (str)
            IP address of the user (public IP?)
        activity (dict)
            What has the user upvoted/downvoted?
        added_songs (list)
            What songs has the user added?
    """

    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        self.activity = []
        self.added_songs = []

    def add_action(self, song_url, action_type):
        self.activity[song_url] = action_type

    def add_song(self, song_url):
        self.added_songs.append(song_url)


class Action:
    UPVOTE = 0
    DOWNVOTE = 1
