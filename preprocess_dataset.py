import pandas as pd

# Load raw dataset
df = pd.read_csv("resilience_dataset.csv")

# Remove timestamp because it is not directly useful for the first ML model
df = df.drop(columns=["timestamp"])

# Convert categorical columns to numeric values
categorical_columns = [
    "nf_name",
    "failure_type",
    "failure_injected",
    "restart_policy",
    "pre_failure_status",
    "post_failure_status",
    "connectivity_status",
]

df = pd.get_dummies(
    df,
    columns=categorical_columns,
    dtype=int
)

# Convert target column to numeric
df["resilience_status"] = df["resilience_status"].map({
    "FAIL": 0,
    "PASS": 1
})

# Save ML-ready dataset
df.to_csv("resilience_ml_dataset.csv", index=False)

print("ML dataset created successfully.")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
