DATA_FILE_PATHS = ['data/course_tags.csv', 'data/user_assessment_scores.csv', 'data/user_course_views.csv',
                   'data/user_interests.csv']

TABLE_DESC = {
    'course_tags': [
        ('course_id', 'TEXT'),
        ('course_tags', 'TEXT')
    ],
    'user_assessment_scores': [
        ('user_handle', 'INTEGER'),
        ('assessment_tag', 'TEXT'),
        ('user_assessment_date', 'TEXT'),
        ('user_assessment_score', 'INTEGER')
    ],
    'user_course_views': [
        ('user_handle', 'INTEGER'),
        ('view_date', 'TEXT'),
        ('course_id', 'TEXT'),
        ('author_handle', 'INTEGER'),
        ('level', 'TEXT'),
        ('view_time_seconds', 'INTEGER')
    ],
    'user_interests': [
        ('user_handle', 'INTEGER'),
        ('interest_tag', 'TEXT'),
        ('date_followed', 'TEXT')
    ]
}
