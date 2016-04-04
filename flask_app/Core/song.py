import time

"""
PUBLIC ATTRIBUTES:
    title
    url (youtube)
    upvotes[user_id]
    downvotes[user_id]
PRIVATE ATTRIBUTES
        time_added
PUBLIC METHODS
    score()
    get_json(user_id=None)
        vote info is specific to user_id when provided
"""

class Song:
    title = None
    url = None
    upvotes = []
    downvotes = []
    time_added = None

    def __init__(self,title,url,user_id):
        self.title = title
        self.url = url
        self.upvotes = [user_id]
        self.downvotes = []
        self.time_added = time.time()

    def score(self):
        """
        :return: the 'score' of this link, based on:
            upvotes
            downvotes
            time since added
        """
        VOTE_WEIGHT = 1.0
        TIME_WEIGHT = 1.1
        time_minutes = (time.time() - self.time_added) / 60.0
        return (len(self.upvotes) / (float(len(self.downvotes)) + 1.0)) ** VOTE_WEIGHT * time_minutes ** TIME_WEIGHT

    def get_json(self,user_id=None):
        result = {}
        result["title"] = self.title
        result["url"] = self.url
        if user_id is not None:
            result["upvote"] = user_id in self.upvotes
            result["downvote"] = user_id in self.downvotes
        else:
            result["upvote"] = self.upvotes
            result["downvote"] = self.downvotes
        return result
