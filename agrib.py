from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect('irrigation.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS SensorData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        soilMoisture INTEGER,
        lightIntensity INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.close()

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    soil_moisture = data.get('soilMoisture')
    light_intensity = data.get('lightIntensity')

    conn = sqlite3.connect('irrigation.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SensorData (soilMoisture, lightIntensity) VALUES (?, ?)",
                   (soil_moisture, light_intensity))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data received successfully"}), 201

@app.route('/api/status', methods=['GET'])
def get_status():
    conn = sqlite3.connect('irrigation.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SensorData ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()

    if data:
        return jsonify({
            "soilMoisture": data[1],
            "lightIntensity": data[2],
            "timestamp": data[3]
        })
    else:
        return jsonify({"message": "No data available"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
