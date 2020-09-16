from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    return render_template("register.html")
    
if __name__ == "__main__":
    app.run(debug=True)