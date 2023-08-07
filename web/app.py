from simulator import *
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    sk_data = [{}]

    if 'file' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['file']
    content = file.read().decode('utf-8')

    start_date = request.form.get('startDate')  # Get the value of the 'startDate' field from the form
    end_date = request.form.get('endDate')      # Get the value of the 'endDate' field from the form

    sankey_data, account_state = simulate_contract(content,start_date,end_date)
    
    full_data = {'sankey_data': sankey_data, 'account_state': account_state }

    return jsonify(full_data)


if __name__ == '__main__':
    app.run()
