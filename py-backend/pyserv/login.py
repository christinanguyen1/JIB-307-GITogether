# a tiny backend component to get data from the login screen

import flask
import

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get email input
        email = str(request.form['inputEmail'])
        password = str(request.form['inputPassword'])
        return "test login: " + email + ":" + password
    return render_template()
