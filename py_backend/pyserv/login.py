# a tiny backend component to get data from the login screen

from flask import Flask, render_template, request
from pydb_api import *
# needs fixing
# from pydb.pydb_api import check_login_db

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get email input
        email = str(request.form['inputEmail'])
        password = str(request.form['inputPassword'])
        new_user_db((email, password))
        return "test login: " + email + ":" + password
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
