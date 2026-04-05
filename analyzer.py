def analyze_state(sample, voltage_history, latency_history):
    voltage = sample["voltage"]
    temp = sample["temp"]
    latency = sample["latency"]
    retry = sample["retry"]
    bod = sample["bod"]

    risk = 0

    if voltage < 3.4:
        risk += 4
    elif voltage < 3.7:
        risk += 2

    if latency > 60:
        risk += 4
    elif latency > 30:
        risk += 2

    if retry > 3:
        risk += 3
    elif retry > 1:
        risk += 2

    if bod >= 2:
        risk += 4
    elif bod == 1:
        risk += 2

    if temp > 40:
        risk += 2
    elif temp > 35:
        risk += 1

    if len(voltage_history) >= 3:
        if voltage_history[-1] < voltage_history[-2] < voltage_history[-3]:
            risk += 1

    if len(latency_history) >= 3:
        if latency_history[-1] > latency_history[-2] > latency_history[-3]:
            risk += 1

    if risk <= 3:
        return "HEALTHY", risk
    elif risk <= 8:
        return "AGING", risk
    else:
        return "FAILURE LIKELY", risk