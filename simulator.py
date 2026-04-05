import random

class HealthDataSimulator:
    def __init__(self):
        self.t = 0

        # Si917 nominal operating rail for demo
        self.voltage = 3.30
        self.temp = 30.0
        self.latency = 15
        self.retry = 0
        self.bod = 0

        # realistic limits
        self.max_voltage = 3.30
        self.min_voltage = 2.95
        self.max_temp = 45.0
        self.max_latency = 120
        self.max_retry = 6
        self.max_bod = 4

    def next_sample(self):
        self.t += 1

        # Phase 1: Healthy
        if self.t <= 10:
            voltage_drop = random.uniform(0.000, 0.004)
            temp_rise = random.uniform(0.02, 0.08)
            latency_rise = random.randint(0, 1)

        # Phase 2: Aging
        elif self.t <= 20:
            voltage_drop = random.uniform(0.006, 0.012)
            temp_rise = random.uniform(0.08, 0.18)
            latency_rise = random.randint(1, 3)

        # Phase 3: Failure likely
        else:
            voltage_drop = random.uniform(0.012, 0.020)
            temp_rise = random.uniform(0.12, 0.25)
            latency_rise = random.randint(2, 5)

        self.voltage = max(self.min_voltage, self.voltage - voltage_drop)
        self.temp = min(self.max_temp, self.temp + temp_rise)
        self.latency = min(self.max_latency, self.latency + latency_rise)

        # retries begin as rail droops
        if self.voltage < 3.22:
            self.retry = min(self.max_retry, self.retry + random.choice([0, 1]))

        # BOD warnings begin later
        if self.voltage < 3.15:
            self.bod = min(self.max_bod, self.bod + random.choice([0, 1]))

        return {
            "time": self.t,
            "voltage": round(self.voltage, 3),
            "temp": round(self.temp, 1),
            "latency": self.latency,
            "retry": self.retry,
            "bod": self.bod
        }