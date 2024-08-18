from flask import Flask, send_file, request, jsonify
import os
variables = {}
app = Flask(__name__)

@app.route('/')
def app_route():
    return send_file(os.path.join(os.path.dirname(__file__), 'index.html')), 200

# Define a dictionary to store dynamic variables
variables = {}

import os
def FileRead(path):
    # Remove any extra double quotes around the path
    path = path.strip('"')
    # Ensure the path is absolute
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ''
    except Exception as e:
        return None
import subprocess
def RunCMD(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return e.stdout + "\n" + e.stderr
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ""

@app.route('/test', methods=['POST'])
def test():
    variables['command'] = request.get_json()
    variables['data'] = RunCMD(variables['command'])
    return variables['data']
@app.route('/open', methods=['POST'])
def open():
    variables['fileName'] = request.get_json()
    print(variables['fileName'])
    variables['data'] = FileRead(variables['fileName'])
    print(variables['data'])
    variables['data'] = str(variables['data'])
    return variables['data']


@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
