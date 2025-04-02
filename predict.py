import joblib
import pandas as pd

def predict_crop(model_name, N, P, K, temperature, pH, moisture):
    input_data = pd.DataFrame([[N, P, K, temperature, pH, moisture]],
                              columns=['N', 'P', 'K', 'temperature', 'ph', 'Soil_Moisture'])

    model = joblib.load(f'{model_name}_model.pkl')
    return model.predict(input_data)[0]

# Example usage
if __name__ == "__main__":
    # Example input
    N, P, K, temperature, pH, moisture = 90, 40, 50, 30, 6.5, 15
    model_name = 'random_forest'  # Change to desired model
    predicted_crop = predict_crop(model_name, N, P, K, temperature, pH, moisture)
    print(f'Predicted Crop: {predicted_crop}')
