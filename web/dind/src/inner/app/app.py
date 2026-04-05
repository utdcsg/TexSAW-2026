from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['POST'])
def ping():
    host = request.form.get('host', '')
    # I hope this isn't vulnerable to command injection...
    try:
        result = subprocess.check_output(
             f"sudo -u ctfer ping -c 1 {host}",
            shell=True, 
            stderr=subprocess.STDOUT, 
            text=True, 
            timeout=5
        )
    except subprocess.CalledProcessError as e:
        result = e.output
    except Exception as e:
        result = str(e)
    return f'<pre>{result}</pre>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)