import streamlit as st
import requests
import json

# Set page title and layout
st.set_page_config(page_title="Automated Irrigation System", layout="wide")

# Display a header
st.title("Automated Irrigation System Dashboard")

# Form for entering sensor data
with st.form(key="sensor_data_form"):
    # Soil Moisture input
    soil_moisture_input = st.slider("Soil Moisture (%)", 0, 100, 30)  # Default value set to 30%

    # Light Intensity input
    light_intensity_input = st.slider("Light Intensity (Lux)", 400, 100000, 25000)  # Default value set to 10,000 Lux

    # Solar Power Availability input
    motor_input = st.radio("Is Motor On ?", ("Yes", "No"), index=0)  # Default is "Yes"
    motor_input = True if motor_input == "Yes" else False  # Convert to boolean

    # Daylight input
    daylight_input = st.radio("Daylight?", ("Yes", "No"), index=0)  # Default is "Yes"
    daylight_input = True if daylight_input == "Yes" else False  # Convert to boolean

    # Submit button
    submit_button = st.form_submit_button(label="Send Data")

# If the form is submitted, send the data to the Flask backend
if submit_button:
    # API endpoint URL (Flask backend running on localhost)
    api_url = "http://127.0.0.1:5000/api/data"
    
    # Prepare the payload to be sent
    payload = {
        "soilMoisture": soil_moisture_input,
        "lightIntensity": light_intensity_input,
        "motor": motor_input,
        "daylight": daylight_input
    }
    
    # Send the POST request to the Flask backend
    response = requests.post(api_url, json=payload)

    # Handle the response
    if response.status_code == 201:
        st.success(f"Data received successfully. Irrigation Status: {response.json()['irrigationStatus']}")
    else:
        st.error("Failed to send data to the server.")

# Fetch the latest sensor data and irrigation status
status_response = requests.get("http://127.0.0.1:5000/api/status")
if status_response.status_code == 200:
    data = status_response.json()
    
    # Display the most recent data in a dashboard
    st.subheader("Latest Sensor Data")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Soil Moisture", f"{data['soilMoisture']}%", delta_color="inverse")
        st.metric("Light Intensity", f"{data['lightIntensity']} Lux")
        st.metric("Motor Available", "Yes" if data['Motor'] else "No")
    
    with col2:
        st.metric("Daylight", "Yes" if data['daylight'] else "No")
        st.metric("Timestamp", data['timestamp'])

    # Display the irrigation status
    st.subheader("Irrigation Status")
    irrigation_status = "Irrigation Started" if data['soilMoisture'] < 40 and data['daylight'] and data['Motor'] else "Irrigation Stopped"
    st.write(irrigation_status)

else:
    st.error("Unable to fetch the latest data.")
