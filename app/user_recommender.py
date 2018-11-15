import pandas as pd
from flask import abort
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

recommender = None


def set_recommender(user_similarity):
    """
    Set global recommender variable to similarity matrix of users.
    :param corr: Cosine similarity matrix
    """
    global recommender
    recommender = user_similarity


def build_recommender(users):
    """
    Apply SVD to user matrix and calculate the cosine similarity between users. Set the recommender of the system to
    the calculated cosine similarity matrix.
    :param users: Pandas DataFrame of user handles and all their course, interest, and assessment features
    """
    svd = TruncatedSVD(n_components=100, random_state=0)
    svd_users = svd.fit_transform(users)

    user_similarity = pd.DataFrame(data=cosine_similarity(svd_users), index=users.index, columns=users.index)

    set_recommender(user_similarity)


def get_similar_users(user_handle):
    """
    Given a user handle, get the 10 most similar users (based on cosine similarity).
    :param user_handle: Integer user handle
    :return: A list of dictionaries of the form {"user_handle": 5, "similarity": 0.785}. If the user handle does not
        exist, raise an error.
    """
    if user_handle in recommender.index:
        all_users = recommender[user_handle].drop(user_handle, axis=0)
        top_users = all_users.nlargest(10).round(3)

        top_user_sim_list = []

        for user, similarity in top_users.iteritems():
            top_user_sim_list.append({"user_handle": user, "similarity": similarity})

        return top_user_sim_list
    else:
        abort(404, "User handle {user_handle} not found".format(user_handle=user_handle))
