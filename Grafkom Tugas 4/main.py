from flask import Flask, render_template, request, jsonify
import json
import os
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    with open('drawing_data.json', 'w') as f:
        json.dump(data, f)
    return jsonify({'status': 'success'})

@app.route('/transform', methods=['POST'])
def transform():
    data = request.json
    shape = data['shape']
    operation = data['operation']
    params = data['params']

    if operation == 'rotate':
        angle_rad = math.radians(params['angle'])
        
        centerX = (shape['x1'] + shape['x2']) / 2
        centerY = (shape['y1'] + shape['y2']) / 2

        temp_x1 = shape['x1'] - centerX
        temp_y1 = shape['y1'] - centerY
        rotated_x1 = temp_x1 * math.cos(angle_rad) - temp_y1 * math.sin(angle_rad) + centerX
        rotated_y1 = temp_x1 * math.sin(angle_rad) + temp_y1 * math.cos(angle_rad) + centerY

        temp_x2 = shape['x2'] - centerX
        temp_y2 = shape['y2'] - centerY
        rotated_x2 = temp_x2 * math.cos(angle_rad) - temp_y2 * math.sin(angle_rad) + centerX
        rotated_y2 = temp_x2 * math.sin(angle_rad) + temp_y2 * math.cos(angle_rad) + centerY
        
        shape['x1'] = rotated_x1
        shape['y1'] = rotated_y1
        shape['x2'] = rotated_x2
        shape['y2'] = rotated_y2

        return jsonify({'status': 'success', 'shape': shape})
    
    return jsonify({'status': 'error', 'message': 'Operation not supported'})

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    with open('templates/index.html', 'w') as f:
        # It's better to ensure this writes the *latest* HTML file
        # In a real setup, you'd just deploy the HTML file.
        # For this example, assuming 'index.html' exists in the same dir as app.py
        f.write(open(os.path.join(os.path.dirname(__file__), 'index.html'), 'r').read())
    app.run(debug=True)