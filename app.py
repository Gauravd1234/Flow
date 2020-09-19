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
    spotify_id = db.Column(db.String(255))
    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password



@app.route("/", methods=['GET', 'POST'])
def home():
    try:
        if request.method == "POST":
                i = request.form["ids"]

                return render_template("display.html", val=return_song(i))
        else:
            return render_template("home.html", logged_in=session["logged_in"])

    except:
            return render_template("home.html", logged_in=False)
    

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        key = request.form["password"]
        session["logged_in"] = True


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
    current_spotify_id =  User.query.filter_by(username=session.get("username")).first().spotify_id
    return render_template("profile.html", spotify_id=current_spotify_id)

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect(url_for("home"))

@app.route("/change_spotify_id", methods=["GET", "POST"])
def change_spotify_id():
    spotify_id = request.form["spotify_id"]
    password = request.form["password"]
    current_user = User.query.filter_by(username=session.get("username")).first()
    if(current_user.password == password):
        current_user.spotify_id = spotify_id
        db.session.commit()
        flash("Spotify ID Successfully Connected!")
    else:
        flash("Spotify ID Not Connected! Invalid Password!")
    return redirect(url_for("home"))

@app.route("/change_password", methods=["POST", "GET"])
def change_password():
    if(request.method == "POST"):
        current_password = request.form["current-password"]
        new_password = request.form["new-password"]

        if(User.query.filter_by(username=session.get("username")).first().password == current_password):
            User.query.filter_by(username=session.get("username")).first().password = new_password
            db.session.commit()
            flash("Password Change Successful!")
        else:
            flash("Current Password Doesn't Match!")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("profile"))
        
@app.route("/change_email", methods=["POST", "GET"])
def change_email():
    if(request.method == "POST"):
        current_email = request.form["current-email"]
        new_email = request.form["new-email"]

        if(User.query.filter_by(username=session.get("username")).first().email == current_email):
            User.query.filter_by(username=session.get("username")).first().email = new_email
            db.session.commit()
            flash("Email Change Successful!")
        else:
            flash("Current Email Doesn't Match")
        return redirect(url_for("home"))
    else:
        return redirect(url_for("profile"))
        
@app.route("/user_list")
def user_list():
    for i in User.query.all():
        if(i.spotify_id):
            return "Username: "+i.username+" Password: "+i.password+" Email: "+i.email+" Spotify ID: "+i.spotify_id
        else:
            return "Username: "+i.username+" Password: "+i.password+" Email: "+i.email+" Spotify ID: None"

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)