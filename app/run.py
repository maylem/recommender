import os

import connexion
from flask import render_template

from db.create_db import create_db
from db.table_config import DATA_FILE_PATHS, TABLE_DESC

app = connexion.App(__name__, specification_dir="./")

app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    create_db('db/ps.sqlite', file_paths=DATA_FILE_PATHS, table_desc=TABLE_DESC)

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
