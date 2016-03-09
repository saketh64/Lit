"""
ATTRIBUTES:
    user_id
        The user's ID - should be persistent across sessions, because it'll be stored as a cookie client side.
    emit_id
        Used to emit socket events JUST to that user. Unique to each page the user is connected to.
CLARIFICATION:
    A User object represents a user-party pairing.
    There can be multiple User objects for a single user if they are active in more than one party.
    user_ids are unique to each user. So there can be multiple User objects with the same user_id.
    emit_id will always be unique to each User object
    We should maybe consider restructuring how we handle users.
"""

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.emit_id = None
