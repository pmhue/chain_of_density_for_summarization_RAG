'''
from flask import Flask, request, render_template
import subprocess
import os
import json

app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])


def index():
    print(os.listdir())
    if request.method == 'POST':
        input_text = request.form['input_text']
        
        # Call chain-of-density code
        result = subprocess.run(['python', 'main.py', input_text], 
                                stdout=subprocess.PIPE).stdout
        
        output = result.decode('utf-8')
        
        return render_template('index.html', input_text=input_text, output=output)

    return render_template('index.html')


if __name__ == '__main__':
    # app.run()
    port = 9090
    app.run(debug=True, port=port)
'''

from flask import Flask, request, render_template
import subprocess
import os
import json

app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        
        # Write input to a temporary file
        with open('temp_input.txt', 'w', encoding='utf-8') as f:
            f.write(input_text)
        
        # Call chain-of-density code
        result = subprocess.run(['python', 'main.py'], 
                                capture_output=True, text=True)
        
        # Remove temporary file
        os.remove('temp_input.txt')
        
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError:
                output = "Error: Unable to parse output"
        else:
            output = f"Error: {result.stderr}"
        
        return render_template('index.html', input_text=input_text, output=output)

    return render_template('index.html')

if __name__ == '__main__':
    port = 9090
    app.run(debug=True, port=port)