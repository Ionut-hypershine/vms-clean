
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret123'

def get_db_connection():
    conn = sqlite3.connect('vms.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/admin')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            return redirect('/admin')
        else:
            error = 'Nume sau parolă greșită.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect('/login')
    return render_template('admin_dashboard.html', username=session['username'])

@app.route('/jobs')
def list_jobs():
    if not session.get('is_admin'):
        return redirect('/login')
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/add-job', methods=['GET', 'POST'])
def add_job():
    if not session.get('is_admin'):
        return redirect('/login')
    if request.method == 'POST':
        title = request.form['title']
        location = request.form['location']
        conn = get_db_connection()
        conn.execute('INSERT INTO jobs (title, location) VALUES (?, ?)', (title, location))
        conn.commit()
        conn.close()
        return redirect('/jobs')
    return render_template('add_job.html')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/add-car', methods=['GET', 'POST'])
def add_car():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        vin = request.form['vin']
        representative = request.form['representative']
        scheduled_time = request.form['scheduled_time']
        added_by = session['user_id']
        status = 'în așteptare'

        conn = get_db_connection()
        conn.execute('INSERT INTO cars (vin, representative, added_by, scheduled_time, status) VALUES (?, ?, ?, ?, ?)',
                     (vin, representative, added_by, scheduled_time, status))
        conn.commit()
        conn.close()
        return redirect('/cars')

    return render_template('add_car.html')
