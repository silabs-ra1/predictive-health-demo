def analyze_state(sample, voltage_history, latency_history):
    voltage = sample["voltage"]
    temp = sample["temp"]
    latency = sample["latency"]
    retry = sample["retry"]
    bod = sample["bod"]

    risk = 0
    reasons = []

    if voltage < 3.4:
        risk += 4
        reasons.append("Low voltage detected")
    elif voltage < 3.7:
        risk += 2
        reasons.append("Voltage droop observed")

    if latency > 60:
        risk += 4
        reasons.append("High latency detected")
    elif latency > 30:
        risk += 2
        reasons.append("Latency increasing")

    if retry > 3:
        risk += 3
        reasons.append("High communication retries")
    elif retry > 1:
        risk += 2
        reasons.append("Retries rising")

    if bod >= 2:
        risk += 4
        reasons.append("Frequent BOD warnings")
    elif bod == 1:
        risk += 2
        reasons.append("BOD warning observed")

    if temp > 40:
        risk += 2
        reasons.append("High temperature stress")
    elif temp > 35:
        risk += 1
        reasons.append("Temperature above nominal")

    if len(voltage_history) >= 3 and voltage_history[-1] < voltage_history[-2] < voltage_history[-3]:
        risk += 1
        reasons.append("Voltage trend is downward")

    if len(latency_history) >= 3 and latency_history[-1] > latency_history[-2] > latency_history[-3]:
        risk += 1
        reasons.append("Latency trend is upward")

    if risk <= 3:
        state = "HEALTHY"
        color = "#16a34a"
        badge = "NORMAL"
        recommendation = "System stable. Continue monitoring."
    elif risk <= 8:
        state = "AGING"
        color = "#f59e0b"
        badge = "WARNING"
        recommendation = "Progressive degradation detected. Inspect power path and battery."
    else:
        state = "FAILURE LIKELY"
        color = "#dc2626"
        badge = "CRITICAL"
        recommendation = "Immediate maintenance recommended. Failure risk is high."

    explanation = " | ".join(reasons[:4]) if reasons else "No anomalies detected"

    return {
        "state": state,
        "risk": risk,
        "reasons": reasons,
        "recommendation": recommendation,
        "color": color,
        "badge": badge,
        "explanation": explanation
    }