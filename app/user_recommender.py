from flask import abort

SIMILAR_USERS = {0: {"user_handle": 0, "similarity": 0.7},  # placeholder data structure
                 1: {"user_handle": 1, "similarity": 0.85}}


def get_similar_users(user_handle):
    if user_handle in SIMILAR_USERS:
        return [SIMILAR_USERS[key] for key in SIMILAR_USERS.keys() if key == user_handle]  # placeholder logic
    else:
        abort(
            404, "User handle {user_handle} not found".format(user_handle=user_handle)
        )
