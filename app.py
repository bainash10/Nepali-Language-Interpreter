from flask import Flask, request, render_template

app = Flask(__name__)

# Function to handle different commands
def parse_command(input_command):
    # Mapping Nepali commands to Python equivalents
    commands = {
        'dekhau': 'print',
        'manau': '=',
        'joda': '+',
        'ghatau': '-',
        'guna': '*',
        'bhaglagau': '/',
    }
    
    # Convert Nepali commands to Python syntax
    input_command = input_command.strip()

    # Convert Nepali function names and operations
    for nepali_op, python_op in commands.items():
        input_command = input_command.replace(nepali_op, python_op)
    
    # Convert 'manau' for assignments
    if 'manau' in input_command:
        input_command = input_command.replace('manau', '=')
    
    # Convert 'dekhau' to 'print' function syntax
    if 'dekhau' in input_command:
        input_command = input_command.replace('dekhau', 'print')
        input_command = f'{input_command}'

    return input_command

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        input_command = request.form['command']
        if input_command == 'madat':
            result = show_help()
        else:
            python_command = parse_command(input_command)
            try:
                # Execute the command
                exec_locals = {}
                exec(python_command, {}, exec_locals)
                result = exec_locals.get('result', 'No result returned')
            except Exception as e:
                result = str(e)
    return render_template('index.html', result=result)

def show_help():
    return """
    <h3>Usage Instructions:</h3>
    <ul>
        <li><strong>dekhau "message"</strong>: Print a message.</li>
        <li><strong>manau a = 10</strong>: Assign a value to a variable.</li>
        <li><strong>joda(a, b)</strong>: Add two numbers.</li>
        <li><strong>ghatau(a, b)</strong>: Subtract two numbers.</li>
        <li><strong>guna(a, b)</strong>: Multiply two numbers.</li>
        <li><strong>bhaglagau(a, b)</strong>: Divide two numbers.</li>
        <li><strong>madat</strong>: Show help information.</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True)
