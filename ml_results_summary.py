import pandas as pd

df = pd.read_csv("resilience_dataset.csv")

print("=" * 60)
print("5G CORE RESILIENCE - EXPERIMENT RESULTS")
print("=" * 60)

print(f"\nTotal experiments: {len(df)}")

print("\n===== FAILURE DISTRIBUTION =====")
print(df["failure_type"].value_counts().to_string())

print("\n===== FAILURE TYPE PERFORMANCE =====")

summary = df.groupby("failure_type").agg(
    Samples=("failure_type", "size"),
    Avg_Recovery_Time=("recovery_time_sec", "mean"),
    Avg_Packet_Loss=("packet_loss_percent", "mean"),
    Avg_RTT=("avg_rtt_ms", "mean"),
    Pass_Rate=("resilience_status", lambda x: (x == "PASS").mean() * 100)
)

print(summary.round(3).to_string())

print("\n===== OVERALL PERFORMANCE =====")

print(
    f"Average recovery time : "
    f"{df['recovery_time_sec'].mean():.3f} s"
)

print(
    f"Average packet loss   : "
    f"{df['packet_loss_percent'].mean():.2f}%"
)

print(
    f"Average RTT           : "
    f"{df['avg_rtt_ms'].mean():.3f} ms"
)

print(
    f"Overall resilience    : "
    f"{(df['resilience_status'] == 'PASS').mean() * 100:.1f}% PASS"
)

print("\n===== REPORT COMPLETE =====")
