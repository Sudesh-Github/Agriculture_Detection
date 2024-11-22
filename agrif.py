import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:5000/api/status"

def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return {"message": "No data available"}
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

# Streamlit UI
st.title("Automated Irrigation System Dashboard")

data = fetch_data()

if "message" in data:
    st.error(data["message"])
else:
    st.metric("Soil Moisture Level", f"{data['soilMoisture']}")
    st.metric("Light Intensity", f"{data['lightIntensity']}")
    st.write(f"Last Updated: {data['timestamp']}")

st.sidebar.title("Manual Controls")
if st.sidebar.button("Turn ON Pump"):
    st.sidebar.success("Pump turned ON!")
if st.sidebar.button("Turn OFF Pump"):
    st.sidebar.warning("Pump turned OFF!")
