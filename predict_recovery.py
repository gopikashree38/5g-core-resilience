import pandas as pd
import joblib

# Load trained model
model = joblib.load("recovery_time_model.pkl")

# Load dataset to get the exact feature structure
df = pd.read_csv("resilience_ml_dataset.csv")

# Remove target and resilience label
X = df.drop(columns=["recovery_time_sec", "resilience_status"])

# Use the latest experiment as an example
sample = X.iloc[[-1]]

# Predict recovery time
prediction = model.predict(sample)[0]

print("===== RECOVERY TIME PREDICTION =====")
print(f"Predicted recovery time: {prediction:.3f} seconds")
