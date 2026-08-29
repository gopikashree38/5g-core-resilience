import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("resilience_ml_dataset.csv")

# Load trained model
model = joblib.load("recovery_time_model.pkl")

# Features used during training
X = df.drop(columns=["recovery_time_sec", "resilience_status"])

# Predict recovery time for every sample
df["predicted_recovery"] = model.predict(X)

# Convert one-hot failure types back into failure labels
failure_columns = [
    "failure_type_NONE",
    "failure_type_SIGINT",
    "failure_type_SIGKILL",
    "failure_type_SIGQUIT",
    "failure_type_SIGTERM"
]

def get_failure_type(row):
    for col in failure_columns:
        if row[col] == 1:
            return col.replace("failure_type_", "")
    return "UNKNOWN"

df["failure_type"] = df.apply(get_failure_type, axis=1)

# Calculate actual and predicted averages
comparison = df.groupby("failure_type").agg(
    Actual=("recovery_time_sec", "mean"),
    Predicted=("predicted_recovery", "mean")
)

print("===== ACTUAL vs ML PREDICTED =====")
print(comparison.round(3).to_string())

# Plot
plt.figure(figsize=(9, 5))

x = range(len(comparison))

plt.plot(
    x,
    comparison["Actual"],
    marker="o",
    label="Actual"
)

plt.plot(
    x,
    comparison["Predicted"],
    marker="x",
    label="ML Predicted"
)

plt.xticks(x, comparison.index)
plt.xlabel("Failure Type")
plt.ylabel("Average Recovery Time (seconds)")
plt.title("Actual vs ML Predicted Recovery Time")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("actual_vs_ml_comparison.png", dpi=300)

print("\nGraph saved as actual_vs_ml_comparison.png")
