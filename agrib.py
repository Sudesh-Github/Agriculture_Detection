from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration
db_config = { 
    'host': '127.0.0.1',
    'user': 'root',  # Replace with your MySQL username
    'password': 'your_password',  # Replace with your MySQL password
    'database': 'irrigation'
}

# Initialize MySQL Database
def init_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SensorData (
            id INT AUTO_INCREMENT PRIMARY KEY,
            soilMoisture INT NOT NULL,
            lightIntensity INT NOT NULL,
            motor BOOLEAN NOT NULL,
            daylight BOOLEAN NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()

# Function to simulate irrigation control (triggering the water pump based on conditions)
def control_irrigation(soil_moisture, light_intensity, daylight, motor):
    if soil_moisture <= 30  and light_intensity <= 25000 and daylight and motor:  # Soil is dry, it's day, and solar power is available
        return "Irrigation started"
    else:
        return "Irrigation stopped"

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    soil_moisture = data.get('soilMoisture')
    light_intensity = data.get('lightIntensity')
    motor = data.get('motor')
    daylight = data.get('daylight')

    # Save data to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO SensorData (soilMoisture, lightIntensity, motor, daylight)
        VALUES (%s, %s, %s, %s)
    ''', (soil_moisture, light_intensity, motor, daylight))
    conn.commit()
    conn.close()

    # Control irrigation based on received data
    irrigation_status = control_irrigation(soil_moisture, light_intensity, daylight, motor)

    return jsonify({
        "message": "Data received successfully",
        "irrigationStatus": irrigation_status
    }), 201

@app.route('/api/status', methods=['GET'])
def get_status():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM SensorData ORDER BY timestamp DESC LIMIT 1")
    data = cursor.fetchone()
    conn.close()

    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "No data available"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
