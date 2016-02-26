import time

class Song:
    title = None
    url = None
    upvotes = []
    downvotes = []

    time_added = None

    def __init__(self,title,url,userID):
        self.title = title
        self.url = url
        self.upvotes = [userID]
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

    def get_json(self,userID=None):
        result = {}
        result["title"] = self.title
        result["url"] = self.url
        if userID is not None:
            result["upvote"] = userID in self.upvotes
            result["downvote"] = userID in self.downvotes
        else:
            result["upvote"] = self.upvotes
            result["downvote"] = self.downvotes
        return result
