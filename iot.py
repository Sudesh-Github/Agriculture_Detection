import requests
import random
import time

API_URL = "http://127.0.0.1:5000/api/data"

def send_data():
    while True:
        soil_moisture = random.randint(300, 700)  # Simulate soil moisture levels
        light_intensity = random.randint(200, 1000)  # Simulate light intensity

        data = {
            "soilMoisture": soil_moisture,
            "lightIntensity": light_intensity
        }

        try:
            response = requests.post(API_URL, json=data)
            if response.status_code == 201:
                print("Data sent successfully:", data)
            else:
                print("Failed to send data:", response.text)
        except Exception as e:
            print(f"Error: {str(e)}")
        
        time.sleep(5)  # Send data every 5 seconds

send_data()
