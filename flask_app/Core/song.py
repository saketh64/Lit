import time

class Song:
    title = None
    url = None
    upvotes = 1
    downvotes = 0

    time_added = None

    def __init__(self,title,url):
        self.title = title
        self.url = url
        self.upvotes = 1
        self.downvotes = 0

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
        return (self.upvotes / (float(self.downvotes) + 1.0)) ** VOTE_WEIGHT * time_minutes ** TIME_WEIGHT

    def get_json(self):
        result = {}
        result["title"] = self.title
        result["url"] = self.url
        result["upvotes"] = self.upvotes
        result["downvotes"] = self.downvotes
        return result
