import pandas as pd
import joblib

from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("resilience_ml_dataset.csv")

# Remove rows with missing recovery time
df = df.dropna(subset=["recovery_time_sec"])

# Features and target
X = df.drop(columns=["recovery_time_sec", "resilience_status"])
y = df["recovery_time_sec"]

# Random Forest
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# 5-fold cross-validation
kf = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

mae_scores = -cross_val_score(
    model,
    X,
    y,
    cv=kf,
    scoring="neg_mean_absolute_error"
)

r2_scores = cross_val_score(
    model,
    X,
    y,
    cv=kf,
    scoring="r2"
)

print("=" * 55)
print("5G CORE RESILIENCE - CROSS VALIDATION")
print("=" * 55)

print(f"\nSamples used : {len(df)}")
print(f"Folds        : 5")

print("\n===== MAE =====")
for i, score in enumerate(mae_scores, 1):
    print(f"Fold {i}: {score:.4f} sec")

print(f"Average MAE: {mae_scores.mean():.4f} sec")

print("\n===== R² SCORE =====")
for i, score in enumerate(r2_scores, 1):
    print(f"Fold {i}: {score:.4f}")

print(f"Average R²: {r2_scores.mean():.4f}")

print("\n===== FINAL MODEL =====")

# Train on complete dataset
model.fit(X, y)

joblib.dump(model, "recovery_time_model_cv.pkl")

print("Model saved as recovery_time_model_cv.pkl")
print("\nEvaluation completed.")
