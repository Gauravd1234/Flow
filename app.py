from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from spotify import return_song


app = Flask(__name__)
app.secret_key = "Flow"
app.config['SECRET_KEY'] = app.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    # The id variable contains the id of every table and item in the database
    _id = db.Column(db.Integer, primary_key=True)

    # 255 is the largest characteer entry that can be stored in a database
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    profile_pic = db.Column(db.LargeBinary); 
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/view", methods=['GET', 'POST'])
def view():
    if request.method == "POST":
        i = request.form["ids"]

        return render_template("display.html", val=return_song(i))


    else:
        return render_template("view.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        key = request.form["password"]
        
        if len(User.query.filter_by(username=user).all()) > 0:
            if (User.query.filter_by(username=user).first().password) == key:

                session["username"] = user
                
                flash("Successfully logged in!")
                return redirect(url_for("home"))
            else:
                flash("Password doesn't match user!")
                return redirect(url_for("login"))
        else:
            flash("User doesn't exist")
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form["email"]
        user = request.form["username"]
        key = request.form["password"]
        
        if(len(User.query.filter_by(username=user).all()) > 0 or len(User.query.filter_by(email=email).all()) > 0):
            flash("Username or password already exists!")
            return redirect(url_for("registration"))

        else:
            new_user = User(user, key, email)
            db.session.add(new_user)
            db.session.commit()

            session["username"] = user
            session["logged_in"] = True
            
            flash("Successfully registered!")
            return redirect(url_for("home"))

    else:
        return render_template("register.html")

@app.route("/profile", methods = ['GET', 'POST'])
def profile():
    return render_template("profile.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)