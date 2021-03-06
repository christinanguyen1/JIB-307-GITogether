# a tiny backend component to get data from the login screen

from flask import Flask, render_template, request, flash, redirect, url_for, session
from pydb_api import *
from flask_mail import Mail, Message
import sys
from tags import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
        session["email"] = email
        password = str(request.form['inputPassword'])
        print(email)
        print(password)
        # returns TRUE if login successful, FALSE if not
        try:
            login_status = check_login_db((email, password))
            if login_status:
                items = render_clubs_homepage()
                return render_template("home.html", email=email, password=password, items=items)
        except IncorrectLoginError:
            flash("Malformed login tuple")
            return redirect(url_for('login'))
        except UnknownError:
            flash("Database table not found")
            return redirect(url_for('login'))
        except EmailNotFoundError:
            flash("Email not found")
            return redirect(url_for('login'))
        except Exception as e:
            print(e)
            flash("Other error")
            return redirect(url_for('login'))
        # print(login_status)
        # print(email)
        # print(password)

    return render_template("index.html")

# loads signup page
@app.route('/signup.html', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        new_email = str(request.form['inputEmail'])
        new_password = str(request.form['inputPassword'])
        confirm_password = str(request.form['confirmPassword'])
        # returns TRUE if registration successful, FALSE if not
        try:
            register_status = new_user_db(
                (new_email, new_password, confirm_password))
            if register_status:
                return render_template("index.html")
        except InvalidEmailError:
            flash("Email must include @ and domain")
            return redirect(url_for('signup'))
        except InvalidPasswordError:
            flash(
                "Password must be at least 8 characters \nand must contain at least 1 letter and number")
            return redirect(url_for('signup'))
        except PasswordNotMatched:
            flash("Both passwords must match")
            return redirect(url_for('signup'))
        except UserAlreadyRegisteredError:
            flash("User already registered:\ntry logging in?")
            return redirect(url_for('signup'))
        except Exception as e:
            print(e)
            flash("Database error occurred")
            return redirect(url_for('signup'))
    return render_template("signup.html")

# loads signout page
@app.route('/index.html', methods=["GET", "POST"])
def signout():
    return render_template("index.html")


# loads register club page
@app.route('/register_club.html', methods=["GET", "POST"])
def reg_club():
    return render_template("register_club.html")


@app.route('/club_page.html/<variable>/<favorite>', methods=["GET", "POST"])
def club_page(variable, favorite):
    # print("THIS IS A FAVORITE")
    # print(favorite)
    # print("THIS IS A VARIABLE")
    # print(variable)
    print("Signed as User:")
    print(session["email"])
    userEmail = session["email"]
    isFav = False
    if (favorite == "notKnown"):
        # need to know whether a club is favorited or not in the database first
        if checkFavorite(userEmail, variable):
            isFav = True
        else:
            isFav = False
    elif (favorite == "favorite"):
        # change the database so that the club is favorited 
        isFav = True
        favoriteClub(userEmail, variable)
    elif (favorite == "unfavorite"):
        # change the database so that the club is unfavorited
        isFav = False
        unfavoriteClub(userEmail, variable)
    else: 
        # usually when the program enters here, it means that the user had tagged. 
        # now we need to make sure that tagged clubs' favorite information is consistent
        if checkFavorite(userEmail, variable):
            isFav = True
        else:
            isFav = False
    items = render_clubs_clubpage(variable)
    for item in items:
        item1 = item[0]
        item2 = item[1]
        item3 = item[2]
    return render_template("club_page.html", item1=item1, item2=item2, item3=item3, isFav=isFav)


@app.route('/forgot.html', methods=["GET", "POST"])
def reset_password():
    return render_template("forgot.html")


@app.route('/action', methods=["POST"])
def send_email():
    recip = str(request.form['inputEmail'])
    try:
        forgotten_password = forgot_email(recip)
        msg = Message('Hello', sender='gitogether307@gmail.com',
                      recipients=[recip])
        msg.body = "Your password is: {0}".format(forgotten_password[0])
        mail.send(msg)
        return render_template("reset.html")
    except:
        flash("That email does not exist")
        return redirect(url_for('reset_password'))

# run home() wheneever we un-toggle from the dropdown menu
@app.route('/home.html', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        print("entered home fucntion")
        club_name = str(request.form['club_name'])
        club_description = str(request.form['description'])
        club_recruitment = str(request.form['recruitment'])
        # add the tags for the club
        if request.form.get('academic') == "checked":
            add_club_tags(club_name, 'academic')
        if request.form.get('social') == "checked":
            add_club_tags(club_name, 'social')
        if request.form.get('cultural') == "checked":
            add_club_tags(club_name, 'cultural')
        if request.form.get('athletic') == "checked":
            add_club_tags(club_name, 'athletic')
        if request.form.get('service') == "checked":
            add_club_tags(club_name, 'service')
        if request.form.get('creativity') == "checked":
            add_club_tags(club_name, 'creativity')

        insert_into_club_table(club_name, club_description, club_recruitment)
        flash("Club Verification Received")
        items = render_clubs_homepage()
        return render_template("home.html", items=items)
    items = render_clubs_homepage()
    return render_template("home.html", items=items)

# server side when the favorite button is toggled
@app.route('/home/favorite-toggled', methods=["GET", "POST"])
def toggle_favorite():
    # if request.method == 'POST':
    tagged = False
    userEmail = session["email"]
    items = get_favorite_clubs(userEmail) 
   
    return render_template("home.html",items=items, tagged=tagged)

# managing the tag stuff when toggeld
@app.route('/home/<variable>', methods=["GET", "POST"])
def toggle_tag(variable):
    # print("entered next variable")
    tagged = True
    print(variable)
    if variable == 'Academic-toggled':
        items = get_tag_clubs('academic')
    if variable == 'Social-toggled':
        items = get_tag_clubs('social')
    if variable == 'Cultural-toggled':
        items = get_tag_clubs('cultural')
    if variable == 'Athletic-toggled':
        items = get_tag_clubs('athletic')
    if variable == 'Service-toggled':
        items = get_tag_clubs('service')
    if variable == 'Creativity-toggled':
        items = get_tag_clubs('creativity')
     
    return render_template("home.html",items=items, tagged=tagged)

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'GET':
        query = request.args.get('search')
        items = render_clubs_homepage_search(query)
        return render_template("home.html", items=items)
    return render_clubs_homepage("home.html")

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
