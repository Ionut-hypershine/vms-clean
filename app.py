from flask import Flask, render_template, request, redirect, url_for, session
from auth import users

app = Flask(__name__)
app.secret_key = 'supersecret'

payslips = []  # Listă simplă în memorie pentru test

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
    return render_template("admin.html", user=session['username'], payslips=payslips)

@app.route("/add", methods=["GET", "POST"])
def add_payslip():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]
        week = request.form["week"]
        payslips.append({"name": name, "amount": amount, "week": week})
        return redirect(url_for("admin"))
    return render_template("add_payslip.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
