import os

import connexion
from flask import render_template

app = connexion.App(__name__, specification_dir="./")

app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
