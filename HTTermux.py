from flask import Flask, send_file, request, jsonify
import os
variables = {}
app = Flask(__name__)

@app.route('/')
def app_route():
    return send_file(os.path.join(os.path.dirname(__file__), 'index.html')), 200

# Define a dictionary to store dynamic variables
variables = {}

def LoopParseFunc(var, delimiter1="", delimiter2=""):
    import re
    if not delimiter1 and not delimiter2:
        # If no delimiters are provided, return a list of characters
        items = list(var)
    else:
        # Construct the regular expression pattern for splitting the string
        pattern = r'[' + re.escape(delimiter1) + re.escape(delimiter2) + r']+'
        # Split the string using the constructed pattern
        items = re.split(pattern, var)
    return items

def Trim(inputString):
    if inputString is None:
        return ""
    return inputString.strip()
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
    items = LoopParseFunc(variables['fileName'], "\n", "\r")
    for A_Index1, A_LoopField1 in enumerate(items, start=1):
        variables['A_Index1'] = A_Index1
        variables['A_LoopField1'] = A_LoopField1
        if (variables['A_Index1'] == 1):
            variables['fileName'] = Trim(variables['A_LoopField1'])
    variables['data'] = RunCMD("cat " + variables['fileName'])
    print(variables['data'])
    variables['data'] = str(variables['data'])
    return variables['data']


@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
