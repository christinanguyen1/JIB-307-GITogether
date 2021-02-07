# a tiny backend component to get data from the login screen

from flask import Flask, render_template, request
# needs fixing
# from pydb.pydb_api import check_login_db

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get email input
        email= str(request.form['inputEmail'])
        password = str(request.form['inputPassword'])
        return render_template("home.html", email = email, password = password)
    return render_template("index.html")

# loads signup page
@app.route('/signup.html', methods=["GET", "POST"])
def signup():
    return render_template("signup.html")

# loads signout page
@app.route('/signout.html', methods=["GET", "POST"])
def signout():
    return render_template("signout.html")

# loads home page
# @app.route('/home.html', methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         # get email input
        
#         # need to get fname and lname still
#         email= str(request.form['inputEmail'])
#         password = str(request.form['inputPassword'])
#         return render_template("home.html", email = email, password = password,)
#     return render_template("home.html")









if __name__ == '__main__':
    app.run()
