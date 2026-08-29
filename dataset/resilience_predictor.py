import pandas as pd
import joblib

# Load trained model
model = joblib.load("recovery_time_model.pkl")

# Load dataset to get exact feature columns
df = pd.read_csv("resilience_ml_dataset.csv")

X = df.drop(columns=["recovery_time_sec", "resilience_status"])

print("=" * 55)
print("5G CORE RESILIENCE - LIVE PREDICTOR")
print("=" * 55)

# Get new experiment values
failure_signal = int(input("\nFailure signal (2/3/9/15): "))
exit_code = int(input("Exit code (130/131/137/143): "))
restart_count = int(input("Restart count: "))
packet_loss = float(input("Packet loss (%): "))
avg_rtt = float(input("Average RTT (ms): "))

# Create input using zeros for all encoded features
sample = pd.DataFrame(0, index=[0], columns=X.columns)

# Numerical features
sample["failure_signal"] = failure_signal
sample["exit_code"] = exit_code
sample["restart_count"] = restart_count
sample["packet_loss_percent"] = packet_loss
sample["avg_rtt_ms"] = avg_rtt

# Fixed values for the current Open5GS experiment
sample["nf_name_SMF"] = 1
sample["restart_policy_always"] = 1
sample["pre_failure_status_running"] = 1
sample["post_failure_status_running"] = 1
sample["connectivity_status_PASS"] = 1
sample["failure_injected_Yes"] = 1

# Set failure type encoding
if failure_signal == 2:
    sample["failure_type_SIGINT"] = 1
elif failure_signal == 3:
    sample["failure_type_SIGQUIT"] = 1
elif failure_signal == 9:
    sample["failure_type_SIGKILL"] = 1
elif failure_signal == 15:
    sample["failure_type_SIGTERM"] = 1

# Predict
predicted_recovery = model.predict(sample)[0]

print("\n===== PREDICTION RESULT =====")
print(f"Predicted Recovery Time : {predicted_recovery:.3f} seconds")

# Decision
if predicted_recovery <= 0.2:
    decision = "PASS"
elif predicted_recovery <= 0.6:
    decision = "WARNING"
else:
    decision = "CRITICAL"

print(f"Resilience Decision     : {decision}")

print("\nThresholds:")
print("<= 0.2 s   : PASS")
print("0.2 - 0.6 s: WARNING")
print("> 0.6 s    : CRITICAL")

print("\nPrediction completed.")
