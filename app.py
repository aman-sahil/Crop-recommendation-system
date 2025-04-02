from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import serial
import time

app = Flask(__name__)

# Set up serial communication with Arduino (Adjust port accordingly)
arduino_port = "COM7"  # Replace with your Arduino's port
baud = 9600
ser = serial.Serial(arduino_port, baud)
time.sleep(2)  # Give some time for the connection to establish

# Load pre-trained models
models = {
    "random_forest": joblib.load('random_forest_model.pkl'),
    "gradient_boosting": joblib.load('gradient_boosting_model.pkl'),
    "knn": joblib.load('knn_model.pkl'),
    "decision_tree": joblib.load('decision_tree_model.pkl'),
    "naive_bayes": joblib.load('naive_bayes_model.pkl')
}

# Get real-time moisture data from Arduino
def get_real_time_moisture():
    if ser.in_waiting > 0:
        try:
            # Read moisture data from the Arduino (Assume it's a single float value)
            moisture_data = ser.readline().decode('utf-8').strip()
            return float(moisture_data)
        except Exception as e:
            print(f"Error reading moisture: {e}")
            return None

# Function to make predictions
def predict_crop(model_name, N, P, K, temperature, pH, moisture):
    input_data = pd.DataFrame([[N, P, K, temperature, pH, moisture]],
                              columns=['N', 'P', 'K', 'temperature', 'ph', 'Soil_Moisture'])
    model = models[model_name]
    return model.predict(input_data)[0]

# Home route to enter data manually
@app.route('/')
def home():
    # Get real-time moisture from Arduino
    moisture = get_real_time_moisture()

    # Render the input form with real-time moisture value
    return render_template('index.html', moisture=moisture)

# API endpoint for crop prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the form submission
        data = request.form

        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        pH = float(data['ph'])
        moisture = float(data['moisture'])  # From the form or real-time moisture

        model_name = data['model']  # The model name selected by the user
        
        # Call the prediction function
        prediction = predict_crop(model_name, N, P, K, temperature, pH, moisture)

        # Return the prediction to the frontend
        return jsonify({'predicted_crop': prediction})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
