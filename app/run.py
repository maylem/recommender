import os
import sqlite3

import connexion
from flask import render_template

from build_user_matrix import get_user_data
from db.create_db import create_db
from db.table_config import DATA_FILE_PATHS, TABLE_DESC
from user_recommender import build_recommender

app = connexion.App(__name__, specification_dir="./")

app.add_api("swagger.yml")

db_conn = sqlite3.connect('db/ps.sqlite')
users = get_user_data(db_conn)
build_recommender(users)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    db_conn = create_db('db/ps.sqlite', file_paths=DATA_FILE_PATHS, table_desc=TABLE_DESC)
    users = get_user_data(db_conn)
    build_recommender(users)

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
