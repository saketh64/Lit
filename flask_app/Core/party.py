from song import Song
from user import User

class Party:

    def __init__(self):
        self.queue = []

    def get_queue_json(userID):
        """
        userID is used to give the user THEIR particular vote data
        :return: a JSON object to send to the client
        """
        global queue
        result = []
        for song in queue:
            result.append(song.get_json(userID))
        return result

    def update_queue_order():
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
