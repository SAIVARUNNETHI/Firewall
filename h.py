from flask import Flask, request

app = Flask(__name__)

@app.route("/",methods=["POST"])
def receive_data():
    if not request.is_json:
        return "Invalid content type", 400

    data = request.json.get('info', '')
    if not data:
        return "Missing 'info' field", 400

    try:
        with open("device_information.txt", "a") as file:
            file.write(data + "\n")
        return "Data written successfully", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3000)


from flask import Flask, request, abort, render_template, redirect, url_for, session
import sqlite3
import subprocess
import requests

app = Flask(_name_)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        client_ip = request.remote_addr
        
        conn = get_db_connection()
        conn.execute("INSERT INTO users (username, password, ip_address) VALUES (?, ?, ?)",
                     (username, password, client_ip))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        client_ip = request.remote_addr
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                            (username, password)).fetchone()
        conn.close()
        
        if user:
            if client_ip == user['ip_address']:
                session['user_id'] = user['id']
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('forbidden'))
        else:
            return "Invalid username or password!"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        return "Welcome to your dashboard!"
    return redirect(url_for('login'))

@app.route("/forbidden")
def forbidden():
    return "Forbidden: You do not have access to this resource."

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000, debug=True)