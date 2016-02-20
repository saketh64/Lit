

class Song:
    title = None
    url = None
    upvotes = 0
    downvotes = 0

    time_added = None

    def __init__(self,title,url):
        self.title = title
        self.url = url
        self.upvotes = 0
        self.downvotes = 0

        # TODO: initialize time_added

    def score(self):
        """
        :return: the 'score' of this link, based on:
            upvotes
            downvotes
            time since added
        """
        return 0 # TODO

    def get_json(self):
        result = {}
        result["title"] = self.title
        result["url"] = self.url
        result["upvotes"] = self.upvotes
        result["downvotes"] = self.downvotes
        return result
