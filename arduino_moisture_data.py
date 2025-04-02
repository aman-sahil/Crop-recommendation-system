import serial
import time
import requests

# Set up serial communication with Arduino (Adjust port accordingly)
arduino_port = "COM3"  # Replace with your Arduino's port
baud = 9600
ser = serial.Serial(arduino_port, baud)
time.sleep(2)  # Give some time for the connection to establish

# API endpoint (Your Flask API URL)
url = "http://localhost:5000/predict"

def get_moisture():
    if ser.in_waiting > 0:
        try:
            # Read moisture data from the Arduino (Assume it's a single float value)
            moisture_data = ser.readline().decode('utf-8').strip()
            return float(moisture_data)
        except Exception as e:
            print(f"Error reading moisture: {e}")
            return None

while True:
    # Get moisture data in real-time
    moisture = get_moisture()
    if moisture is not None:
        print(f"Moisture: {moisture}%")

        # Manually input other values
        N = float(input("Enter value for N: "))
        P = float(input("Enter value for P: "))
        K = float(input("Enter value for K: "))
        temperature = float(input("Enter value for temperature: "))
        pH = float(input("Enter value for pH: "))

        # Prepare data to be sent to the API
        data = {
            "N": N,
            "P": P,
            "K": K,
            "temperature": temperature,
            "ph": pH,
            "moisture": moisture,  # Automatically send real-time moisture data
            "model": "random_forest"  # You can change the model name as needed
        }

        try:
            # Make POST request to your Flask API
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("Predicted Crop:", response.json()['predicted_crop'])
            else:
                print(f"Failed to get a prediction. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error making POST request: {e}")
    
    # Wait before getting the next reading
    time.sleep(5)
