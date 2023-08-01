from simulator import *
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['file']
    content = file.read().decode('utf-8')

    start_date = request.form.get('startDate')  # Get the value of the 'startDate' field from the form
    end_date = request.form.get('endDate')      # Get the value of the 'endDate' field from the form

    simulate_contract(file,start_date,end_date)
    
    result = f'Start Date: {start_date}\nEnd Date: {end_date}\n\n{content}'
    return f'<pre>{result}</pre>'

if __name__ == '__main__':
    app.run()
