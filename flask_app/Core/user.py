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

    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        self.activity = []
        self.added_songs = []

    def add_action(self, song_url, action_type):
        self.activity.append({
            "url":song_url,
            "action_type":action_type
        })

    def remove_action(self, song_url, action_type):
        self.activity.remove({
            "url":song_url,
            "action_type":action_type
        })

    def has_upvoted(self,song_url):
        for action in self.activity:
            if action["url"] == song_url and action["action_type"] == Action.UPVOTE:
                return True
        return False

    def has_downvoted(self,song_url):
        for action in self.activity:
            if action["url"] == song_url and action["action_type"] == Action.DOWNVOTE:
                return True
        return False

    def add_song(self, song_url):
        self.added_songs.append(song_url)


class Action:
    UPVOTE = 0
    DOWNVOTE = 1
