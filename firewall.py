from flask import Flask , request , abort
import socket
import subprocess
import requests
app = Flask(__name__)

allowed_ips = { '127.0.0.1','192.168.1.100'}


@app.before_request
def limit_access():
    client_ip = request.remote_addr
    print(f"Client_IP:{client_ip}")
    if client_ip not in allowed_ips:
        
        try :
             result = subprocess.run(["nmap", "-A", client_ip], capture_output=True, text=True)
             print(result.stdout)
        except Exception as e:
            print(f"Error scanning IP {client_ip}: {e}")
        try:
            res = subprocess.run(['nmap','-p','--open'],capture_output=True,text=True)
            open_ports = res.stdout
            print(f"Open_ports for the ip{client_ip}:\n{open_ports}")
        except Exception as e:
            print(f"Error Scanning open ports:{e}")
        try:
                response = requests.get(f"http://ipinfo.io/{client_ip}/json")
                data = response.json()
                print(data)
        except Exception as e:
            print(f"error exception:{e}")
        abort(403)
@app.route("/")
def index():
    return " Welcome to secure website"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    