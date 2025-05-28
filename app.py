import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from auth import users

app = Flask(__name__)
app.secret_key = 'supersecret'
DB_PATH = 'vms.db'

def get_payslips():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT name, amount, week, created_at FROM payslips ORDER BY id DESC")
        return c.fetchall()

def get_jobs():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT title, location, created_at FROM jobs ORDER BY id DESC")
        return c.fetchall()

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
    slips = get_payslips()
    return render_template("admin.html", user=session['username'], payslips=slips)

@app.route("/add", methods=["GET", "POST"])
def add_payslip():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]
        week = request.form["week"]
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO payslips (name, amount, week) VALUES (?, ?, ?)", (name, amount, week))
            conn.commit()
        return redirect(url_for("admin"))
    return render_template("add_payslip.html")
@app.route("/jobs")
def jobs():
    conn = sqlite3.connect("vms.db")
    c = conn.cursor()
    c.execute("SELECT id, title, location FROM jobs ORDER BY id DESC")
    jobs = c.fetchall()
    conn.close()
    return render_template("jobs.html", jobs=jobs)

@app.route("/add-job", methods=["GET", "POST"])
def add_job():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        location = request.form["location"]
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO jobs (title, location) VALUES (?, ?)", (title, location))
            conn.commit()
        return redirect(url_for("jobs"))
    return render_template("add_job.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
@app.route("/delete-job/<int:job_id>")
def delete_job(job_id):
    conn = sqlite3.connect("vms.db")
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("jobs"))
