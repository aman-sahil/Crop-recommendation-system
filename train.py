import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import joblib

# Load the dataset
file_path = 'Crop_recommendation.csv'
data = pd.read_csv(file_path)

# Define coefficients for converting humidity to soil moisture
a = 0.75
b = 10

# Convert humidity to soil moisture
data['Soil_Moisture'] = a * data['humidity'] + b

# Assuming you have a column for the crop label, replace 'Crop' with the actual column name
X = data[['N', 'P', 'K', 'temperature', 'ph', 'Soil_Moisture']]
y = data['label']  # Use the actual column name for the crop type

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and save models
models = {
    'random_forest': RandomForestClassifier(random_state=1),
    'gradient_boosting': GradientBoostingClassifier(random_state=1),
    'decision_tree': DecisionTreeClassifier(random_state=1),
    'knn': KNeighborsClassifier(),
    'naive_bayes': GaussianNB()
}

for model_name, model in models.items():
    model.fit(x_train, y_train)
    joblib.dump(model, f'{model_name}_model.pkl')
    print(f"{model_name} trained and saved!")
