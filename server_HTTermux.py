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
    # Check if the path is absolute
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    try:
        with open(path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        raise RuntimeError(f"Error: Could not open the file. {e}")
import os
def FileAppend(content, path):
    # Check if the path is absolute
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    try:
        with open(path, 'a') as file:
            file.write(content)
    except Exception as e:
        raise RuntimeError(f"Error: Could not open the file for appending. {e}")
import subprocess
def RunCMD(command):
    """
    Run a specified command in Termux and return the output.
    Args:
        command (str): The command to run in Termux.
    Returns:
        tuple: A tuple containing the standard output and standard error of the command.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return (result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return (e.stdout, e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ("", "")

@app.route('/Open', methods=['POST'])
def Open():
    variables['fileToOpen'] = request.get_json()
    variables['dataFormText'] = FileRead(variables['fileToOpen'])
    return variables['dataFormText']
@app.route('/Save', methods=['POST'])
def Save():
    variables['dataToSave'] = request.get_json()
    FileAppend(variables['dataToSave'], variables['fileToOpen'])
    return "saved"
@app.route('/runcommand', methods=['POST'])
def runcommand():
    variables['command'] = request.get_json()
    variables['var1234565432345654out'] = RunCMD(variables['command'])
    return "done"



@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
