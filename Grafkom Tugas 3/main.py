from flask import Flask, render_template, request, jsonify
import json
import os

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
    
    # Implementasi transformasi di Python
    if operation == 'rotate':
        # Contoh implementasi rotasi
        angle = params['angle']
        # Logika rotasi bisa ditambahkan di sini
        transformed_shape = {
            **shape,
            'transformed': True,
            'operation': 'rotate',
            'angle': angle
        }
        return jsonify({'status': 'success', 'shape': transformed_shape})
    
    return jsonify({'status': 'error', 'message': 'Operation not supported'})

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    with open('templates/index.html', 'w') as f:
        f.write("""<!-- Isi dari file HTML di atas -->""")
    app.run(debug=True)
