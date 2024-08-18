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
def Asc(char):
    if char is None or len(char) == 0:
        return None
    return ord(char[0])

@app.route('/command', methods=['POST'])
def command():
    variables['command'] = request.get_json()
    variables['data'] = RunCMD(variables['command'])
    return variables['data']
@app.route('/open', methods=['POST'])
def open():
    variables['fileName'] = request.get_json()
    variables['data'] = RunCMD("cat " + variables['fileName'])
    return variables['data']
@app.route('/save', methods=['POST'])
def save():
    variables['data'] = request.get_json()
    # Initialize variables
    variables['dataOut'] = ""
    # Convert text to ASCII representation
    items = LoopParseFunc(variables['data'], "\n", "\r")
    for A_Index1, A_LoopField1 in enumerate(items, start=1):
        variables['A_Index1'] = A_Index1
        variables['A_LoopField1'] = A_LoopField1
        if (variables['A_Index1'] == 1):
            variables['fileName'] = variables['A_LoopField1'] ; variables['First'] variables['line'] variables['is'] variables['the'] variables['filename']
        else:
            # Convert each character to its ASCII value
            items = LoopParseFunc(variables['A_LoopField1'])
            for A_Index2, A_LoopField2 in enumerate(items, start=1):
                variables['A_Index2'] = A_Index2
                variables['A_LoopField2'] = A_LoopField2
                variables['asciiChar'] = Asc(variables['A_LoopField2'])
                variables['dataOut'] += variables['asciiChar'] + "\n"
    # Remove trailing newline
    variables['dataOut'] = StringTrimRight(variables['dataOut'], 1)
    # Save ASCII data to temporary file
    variables['tempFile'] = "temp_ascii.txt"
    RunCMD("echo " + Chr(34) + variables['dataOut'] + Chr(34) + " > " + variables['tempFile'])
    # Reformat ASCII data to text
    RunCMD("cat " + variables['tempFile'] + " | awk '{printf " + Chr(34) + "%c" + Chr(34) + ", $1}' > " + variables['fileName'])
    # Clean up temporary file
    RunCMD("rm " + variables['tempFile'])
    return "done"


@app.errorhandler(404)
def not_found(e):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
