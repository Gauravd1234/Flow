from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "Flow"

db = SQLAlchemy(app)
app.config['SECRET_KEY'] = app.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


class User(db.Model):
    # The id variable contains the id of every table and item in the database
    _id = db.Column(db.Integer, primary_key=True)

    # 255 is the largest characteer entry that can be stored in a database
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = password



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/user")
def user():
    
    if "username" in session:
        username = session["username"]
        return render_template("user.html", username = username)   

    else:
        return redirect(url_for("login"))

@app.route("/view")
def view():
    return render_template("view.html", values = User.query.all())

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        key = request.form["password"]

        if "username" in session:
            return redirect(url_for("user", username = user))

        
        
        
        if len(User.query.filter_by(username=user).all()) > 0:
            if (User.query.filter_by(username=user).first().password) == key:
                flash("Successfully signed in", "info")
                session["username"] = user
                session["logged_in"] = True
                return redirect(url_for("user", username = user))

            else:
                flash("Credentials invalid", "info")
                return redirect(url_for("login"))

        else:
            flash("User not found", "info")
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
            flash("User already exists")
            return redirect(url_for("registration"))

        else:
            new_user = User(user, key, email)
            db.session.add(new_user)
            db.session.commit()


            session["username"] = user
            session["logged_in"] = True

            return redirect(url_for("home"))

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    flash("Logged out successfully", "info")

    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)