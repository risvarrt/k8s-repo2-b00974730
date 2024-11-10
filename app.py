from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    
    file_name = data['file']
    product = data.get('product', '')
    
    filepath = '/shared_data/' + file_name

    # Check if the file extension is '.csv'
    if not file_name.endswith('.csv'):
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 404

    # Check if the file is a valid CSV
    try:
        with open(filepath, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            headers = next(reader)
            num_columns = len(headers)

            for row in reader:
                if len(row) != num_columns:
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 404
    except Exception as e:
        return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 404
# test
    # Process the file
    try:
        total = 0
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['product'] == product:
                    total += int(row['amount'])
        return jsonify({"file": file_name, "sum": total})
    except Exception as e:
        return jsonify({"file": file_name, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002)
