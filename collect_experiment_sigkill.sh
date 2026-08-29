#!/bin/bash

CSV="$HOME/5g-core-resilience/dataset/resilience_dataset.csv"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
NF_NAME="SMF"

# Failure scenario
FAILURE_TYPE="SIGKILL"
FAILURE_INJECTED="Yes"
FAILURE_SIGNAL="9"

RESTART_POLICY=$(docker inspect smf --format '{{.HostConfig.RestartPolicy.Name}}')
PRE_STATUS=$(docker inspect smf --format '{{.State.Status}}')

START_TIME=$(date +%s.%3N)

# Inject SIGTERM
docker exec smf sh -c 'kill -9 1'

# Wait for SMF to recover
while true; do
    STATUS=$(docker inspect smf --format '{{.State.Status}}' 2>/dev/null)

    if [ "$STATUS" = "running" ]; then
        break
    fi

    sleep 0.1
done

END_TIME=$(date +%s.%3N)

RECOVERY_TIME=$(awk "BEGIN {printf \"%.3f\", $END_TIME-$START_TIME}")

POST_STATUS=$(docker inspect smf --format '{{.State.Status}}')

# SIGTERM normally produces exit code 143 (128 + 15)
EXIT_CODE=137

RESTART_COUNT=$(docker inspect smf --format '{{.RestartCount}}')

PING_RESULT=$(ping -c 20 8.8.8.8 2>/dev/null)

PACKET_LOSS=$(echo "$PING_RESULT" | grep -oP '[0-9.]+(?=% packet loss)' | head -1)

AVG_RTT=$(echo "$PING_RESULT" | grep 'rtt' | awk -F'=' '{print $2}' | awk -F'/' '{print $2}')

if [ -z "$PACKET_LOSS" ]; then
    PACKET_LOSS="NA"
fi

if [ -z "$AVG_RTT" ]; then
    AVG_RTT="NA"
fi

if [ "$POST_STATUS" = "running" ] && [ "$PACKET_LOSS" != "NA" ]; then
    CONNECTIVITY_STATUS="PASS"
    RESILIENCE_STATUS="PASS"
else
    CONNECTIVITY_STATUS="FAIL"
    RESILIENCE_STATUS="FAIL"
fi

echo "$TIMESTAMP,$NF_NAME,$FAILURE_TYPE,$FAILURE_INJECTED,$FAILURE_SIGNAL,$EXIT_CODE,$RESTART_POLICY,$RESTART_COUNT,$PRE_STATUS,$POST_STATUS,$RECOVERY_TIME,$CONNECTIVITY_STATUS,$PACKET_LOSS,$AVG_RTT,$RESILIENCE_STATUS" >> "$CSV"

echo
echo "Experiment completed."
echo "Failure type: ${FAILURE_TYPE}"
echo "Recovery time: ${RECOVERY_TIME}s"
echo "Packet loss: ${PACKET_LOSS}%"
echo "Average RTT: ${AVG_RTT} ms"
echo "Final status: ${POST_STATUS}"
echo "Resilience: ${RESILIENCE_STATUS}"
