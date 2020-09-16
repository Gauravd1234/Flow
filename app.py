from flask import Flask, redirect, url_for, render_template, request, session, flash

app = Flask(__name__)
app.secret_key = "Flow"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/user")
def user():
    
    if "username" in session:
        username = session["username"]
        return render_template("user.html", usr = username)   

    else:
        return redirect(url_for("login"))


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form["username"]
        key = request.form["password"]
        
        session["username"] = user
        session["logged_in"] = True

        flash("Successfully signed in", "info")
        return redirect(url_for("user"))

    else:
        if "username" in session:
            return redirect(url_for("user"))
            
        return render_template("login.html")


@app.route("/register", methods = ['GET', 'POST'])
def register():
    return render_template("register.html")


@app.route("/logout")
def logout():
    flash("Logged out successfully", "info")

    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)