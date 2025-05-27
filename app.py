from flask import Flask, render_template, redirect, url_for, request, session
from auth import users

app = Flask(__name__)
app.secret_key = 'supersecret'

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("admin"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("admin"))
        else:
            error = "Invalid credentials"
    return render_template("login.html", error=error)

@app.route("/admin")
def admin():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("admin.html", user=session['username'])

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
