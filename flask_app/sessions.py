import random
import string

all_user_ids = set()

def get_random_user_id():
    global all_user_ids
    while 1:
        ret = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        if ret not in all_user_ids:
            all_user_ids.add(ret)
            return ret
