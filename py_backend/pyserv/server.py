# a tiny backend component to get data from the login screen

from flask import Flask, render_template, request
from pydb_api import *
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gitogether307@gmail.com'
app.config['MAIL_PASSWORD'] = 'gitogether123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = str(request.form['inputEmail'])
        password = str(request.form['inputPassword'])
        # returns TRUE if login successful, FALSE if not
        login_status = check_login_db((email, password))
        if login_status:
            return render_template("home.html", email=email, password=password)
    return render_template("index.html")

# loads signup page


@app.route('/signup.html', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        new_email = str(request.form['inputEmail'])
        new_password = str(request.form['inputPassword'])
        confirm_password = str(request.form['confirmPassword'])
        # returns TRUE if registration successful, FALSE if not
        register_status = new_user_db(
            (new_email, new_password, confirm_password))
        if register_status:
            # TODO: NEED A CONFIRMATION PAGE AFTER SUBMITTING
            return render_template("index.html")
    return render_template("signup.html")

# loads signout page


@app.route('/signout.html', methods=["GET", "POST"])
def signout():
    return render_template("signout.html")


@app.route('/forgot.html', methods=["GET", "POST"])
def reset_password():
    return render_template("forgot.html")


@app.route('/action', methods=["POST"])
def send_email():
    recip = str(request.form['inputEmail'])
    msg = Message('Hello', sender='gitogether307@gmail.com',
                  recipients=[recip])
    msg.body = "You requested to reset your password"
    mail.send(msg)
    return render_template("reset.html")


if __name__ == '__main__':
    # app.run(debug = True)
    app.run()
