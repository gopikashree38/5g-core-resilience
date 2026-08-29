import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load ML dataset
df = pd.read_csv("resilience_ml_dataset.csv")

# Separate features and target
X = df.drop(columns=["recovery_time_sec", "resilience_status"])
y = df["recovery_time_sec"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print("===== RECOVERY TIME PREDICTION =====")
print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")
print(f"MAE              : {mae:.4f} sec")
print(f"RMSE             : {rmse:.4f} sec")
print(f"R² Score         : {r2:.4f}")

print("\nActual vs Predicted:")
for actual, predicted in zip(y_test, y_pred):
    print(f"Actual: {actual:.3f}s  Predicted: {predicted:.3f}s")

# Feature importance
importance = pd.Series(
    model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\n===== FEATURE IMPORTANCE =====")
print(importance)
import joblib

joblib.dump(model, "recovery_time_model.pkl")
print("\nModel saved as recovery_time_model.pkl")
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))
plt.plot(range(len(y_test)), y_test.values, marker='o', label='Actual')
plt.plot(range(len(y_pred)), y_pred, marker='x', label='Predicted')

plt.xlabel("Test Sample")
plt.ylabel("Recovery Time (seconds)")
plt.title("Actual vs Predicted Recovery Time")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("actual_vs_predicted.png", dpi=300)
plt.show()

print("Graph saved as actual_vs_predicted.png")
# Feature importance graph

plt.figure(figsize=(10, 6))

importance.sort_values().plot(kind="barh")

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Random Forest Feature Importance")
plt.tight_layout()

plt.savefig("feature_importance.png", dpi=300)
plt.show()

print("Graph saved as feature_importance.png")
