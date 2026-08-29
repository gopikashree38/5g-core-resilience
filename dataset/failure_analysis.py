import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("resilience_dataset.csv")

summary = df.groupby("failure_type")["recovery_time_sec"].mean().sort_values()

plt.figure(figsize=(9, 5))
summary.plot(kind="bar")

plt.xlabel("Failure Type")
plt.ylabel("Average Recovery Time (seconds)")
plt.title("Average Recovery Time by Failure Type")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("failure_recovery_comparison.png", dpi=300)
plt.show()

print("\n===== FAILURE RECOVERY SUMMARY =====")
print(summary.round(3))

print("\nGraph saved as failure_recovery_comparison.png")
