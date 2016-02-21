import random
import string

users = []

def get_random_user_id():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


def get_user(user_id):
    global users
    for user in users:
        if user.user_id == user_id:
            return user

def does_user_exist(user_id):
    return get_user(user_id) != None

def get_all_user_activity_json():
    global users
    """
    :return: a JSON object of all user activity
    """
    result = {}
    for user in users:
        result[user.user_id] = user.activity
    return result