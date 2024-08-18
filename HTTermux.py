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

def StrReplace(originalString, find, replaceWith):
    # Use the replace method to replace occurrences of 'find' with 'replaceWith'
    return originalString.replace(find, replaceWith)
def StringTrimRight(input, numChars):
    # Convert input to a string if it's not already a string
    if not isinstance(input, str):
        input = str(input)  # Convert input to string
    # Check if the input is long enough to perform trimming
    if len(input) >= numChars:
        return input[:-numChars]  # Trim the string from the right
    else:
        return input  # Return input unchanged if numChars is larger than string length
def Chr(number):
    # Check if the number is None
    if number is None:
        # Return an empty string
        return ""
    # Check if the number is within the valid Unicode range
    if 0 <= number <= 0x10FFFF:
        # Convert the number to a character using chr()
        return chr(number)
    else:
        # Return an empty string for invalid numbers
        return ""

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

@app.route('/command', methods=['POST'])
def command():
    variables['command'] = request.get_json()
    variables['data'] = RunCMD(variables['command'])
    return variables['data']
@app.route('/open', methods=['POST'])
def open():
    variables['fileName'] = request.get_json()

    # Check if the file exists
    if not os.path.exists(variables['fileName']):
        return f"Error: File {variables['fileName']} does not exist", 404

    try:
        variables['data'] = RunCMD(f"cat {variables['fileName']}")
    except Exception as e:
        print(f"Error during open: {e}")
        return str(e), 500

    return variables['data']

@app.route('/save', methods=['POST'])
def save():
    variables['data'] = request.get_json()
    variables['dataOut'] = ""
    items = LoopParseFunc(variables['data'], "\n", "\r")
    for A_Index1, A_LoopField1 in enumerate(items, start=1):
        if A_Index1 == 1:
            variables['fileName'] = A_LoopField1
        else:
            variables['dataOut'] += A_LoopField1 + "\n"

    # Escaping quotes
    variables['dataOut'] = variables['dataOut'].replace('"', '\\"')

    # Trim last newline character
    variables['dataOut'] = StringTrimRight(variables['dataOut'], 1)

    # Check if the file exists before removing it
    if os.path.exists(variables['fileName']):
        RunCMD(f"rm {variables['fileName']}")

    # Simplified printf command
    try:
        command = f'printf "%s" "{variables["dataOut"]}" > {variables["fileName"]}'
        RunCMD(command)
    except Exception as e:
        print(f"Error during save: {e}")
        return str(e), 500

    return "done"



@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
