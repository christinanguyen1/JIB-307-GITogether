# a tiny backend component to get data from the login screen

from flask import Flask, render_template, request

from flask_mail import Mail, Message
# needs fixing
# from pydb.pydb_api import check_login_db

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'GITogether307@gmail.com'
app.config['MAIL_PASSWORD'] = 'gitogether123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get email input
        email= str(request.form['inputEmail'])
        password = str(request.form['inputPassword'])
        msg = Message('Hello', sender = 'GITogether307@gmail.com', recipients = ['christinan2010@gmail.com'])
        msg.body = "This is the email body"
        mail.send(msg)
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

@app.route('/forgot.html', methods=["GET", "POST"])
def reset_password():
    return render_template("forgot.html")

@app.route("/reset.html", methods=["GET", "POST"])
def index():
    # recip = str(request.form['inputEmail'])
    msg = Message('Hello', sender = 'GITogether307@gmail.com', recipients = ['christinan2010@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return render_template("reset.html")


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
