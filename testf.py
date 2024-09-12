from flask import Flask, request, abort, render_template, redirect, url_for, session
import sqlite3
import subprocess
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return redirect(url_for('login'))  

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
                try:
                    result = subprocess.run(["nmap", "-A", client_ip], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"Nmap scan results for IP {client_ip}:\n{result.stdout}")
                    else:
                        print(f"Nmap scan failed: {result.stderr}")
                except Exception as e:
                    print(f"Error scanning IP {client_ip}: {e}")
                
                try:
                    res = subprocess.run(['nmap', '-p', '1-65535', '--open', client_ip], capture_output=True, text=True)
                    if res.returncode == 0:
                        open_ports = res.stdout
                        print(f"Open ports for the IP {client_ip}:\n{open_ports}")
                    else:
                        print(f"Error in port scan: {res.stderr}")
                except Exception as e:
                    print(f"Error scanning open ports for IP {client_ip}: {e}")
                
                try:
                    response = requests.get(f"http://ipinfo.io/{client_ip}/json")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"IP Information: {data}")
                    else:
                        print(f"Failed to fetch IP information: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching IP information: {e}")
                
                abort(403)
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
