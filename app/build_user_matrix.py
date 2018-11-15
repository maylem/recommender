import pandas as pd
from sklearn.preprocessing import StandardScaler


def transform_user_interests(user_interests):
    """
    Pivot user interest data and fill with binary values.
    :param user_interests: Pandas DataFrame with user interest data
    :return: Pandas DataFrame
    """
    user_interests = pd.pivot_table(user_interests, index='user_handle', columns='interest_tag', fill_value=0.0,
                                    aggfunc=lambda x: 1.0)
    user_interests.columns = user_interests.columns.droplevel()
    return user_interests


def get_course_data(user_course_views):
    """
    Create binary variables out of the course_id column in the DataFrame.
    :param user_course_views: Pandas DataFrame on users' course views
    :return: Pandas DataFrame with binary course values
    """
    courses = pd.pivot_table(user_course_views, index='user_handle', columns='course_id', fill_value=0.0,
                             aggfunc=lambda x: 1.0)
    courses.columns = courses.columns.droplevel()
    courses = courses.add_prefix('course_')
    return courses


def get_view_data(user_course_views):
    """
    Create a new variable with the total number of views per user.
    :param user_course_views: Pandas DataFrame on users' course views
    :return: Pandas DataFrame with total view data
    """
    views = user_course_views.groupby('user_handle').size().reset_index().rename(columns={0: 'total_views'})
    views.set_index('user_handle', inplace=True)
    views['total_views'] = StandardScaler().fit_transform(views)
    return views


def get_num_courses_data(user_course_views):
    """
    Create a new variable with the total number of courses taken per user.
    :param user_course_views: Pandas DataFrame on users' course views
    :return: Pandas DataFrame with course count data
    """
    num_courses = user_course_views.groupby('user_handle')['course_id'].nunique().reset_index().rename(
        columns={'course_id': 'total_courses'})
    num_courses.set_index('user_handle', inplace=True)
    num_courses['total_courses'] = StandardScaler().fit_transform(num_courses)

    return num_courses


def get_level_data(user_course_views):
    """
    Create variables for each of the level categories with the total number of courses taken per user under each level.
    :param user_course_views: Pandas DataFrame on users' course views
    :return: Pandas DataFrame with level count data
    """
    levels = pd.pivot_table(user_course_views.drop_duplicates(['user_handle', 'course_id']).groupby(
        ['user_handle', 'level']).size().reset_index().rename(columns={0: 'total_levels'}), index='user_handle',
                            columns='level', values='total_levels', fill_value=0.0)
    levels = levels.add_prefix('level_')
    levels[levels.columns] = StandardScaler().fit_transform(levels)

    return levels


def get_view_times_data(user_course_views):
    """
    Calculate the total view time per user.
    :param user_course_views: Pandas DataFrame on users' course views
    :return: Pandas DataFrame with total view times (in seconds)
    """
    view_times = user_course_views.groupby('user_handle')['view_time_seconds'].sum().reset_index().rename(
        columns={'view_time_seconds': 'total_view_time_s'})
    view_times.set_index('user_handle', inplace=True)
    view_times['total_view_time_s'] = StandardScaler().fit_transform(view_times)

    return view_times


def get_author_data(user_course_views):
    """
    Create binary variables out of the author_handle column in the DataFrame.
    :param user_course_views: Pandas DataFrame on users' course views
    :return: Pandas DataFrame with binary author variables
    """
    authors = pd.pivot_table(user_course_views, index='user_handle', columns='author_handle', fill_value=0.0,
                             aggfunc=lambda x: 1.0)
    authors.columns = authors.columns.droplevel()
    authors = authors.add_prefix('author_')

    return authors


def transform_user_course_views(user_course_views):
    """
    Pivot, group and merge data variables in the DataFrame.
    :param user_course_views: Pandas DataFrame on users' course views
    :return: Pandas DataFrame
    """
    views = get_view_data(user_course_views)
    num_courses = get_num_courses_data(user_course_views)
    levels = get_level_data(user_course_views)
    view_times = get_view_times_data(user_course_views)

    all_data = pd.merge(views, num_courses, 'left', on='user_handle')
    all_data = pd.merge(all_data, levels, 'left', on='user_handle')
    all_data = pd.merge(all_data, view_times, 'left', on='user_handle')

    return all_data


def transform_user_assessment_scores(user_assessment_scores):
    """
    Get the mean assessment score per user and scale the values.
    :param user_assessment_scores: Pandas DataFrame with user assessment data
    :return: Pandas DataFrame
    """
    user_assessment_scores = user_assessment_scores.groupby('user_handle')[
        'user_assessment_score'].mean().reset_index().rename(
        columns={'user_assessment_score': 'avg_score'})
    user_assessment_scores.set_index('user_handle', inplace=True)
    user_assessment_scores['avg_score'] = StandardScaler().fit_transform(user_assessment_scores[['avg_score']])

    return user_assessment_scores


def get_user_data(conn):
    """
    Query db for user data, transform the data, and return a merged user DataFrame.
    :param conn: sqlite db connection
    :return: Pandas DataFrame with user handles as indices, and interests, courses, and assessments as columns
    """
    user_interests = pd.read_sql_query('SELECT * FROM user_interests;', conn)
    user_course_views = pd.read_sql_query('SELECT * FROM user_course_views;', conn)
    user_assessment_scores = pd.read_sql_query('SELECT * FROM user_assessment_scores;', conn)

    user_interests = transform_user_interests(user_interests)
    user_course_views = transform_user_course_views(user_course_views)
    user_assessment_scores = transform_user_assessment_scores(user_assessment_scores)

    users = pd.merge(user_interests, user_course_views, 'left', on='user_handle')
    users = pd.merge(users, user_assessment_scores, 'left', on='user_handle')
    users.fillna(0.0, inplace=True)

    conn.close()

    return users
