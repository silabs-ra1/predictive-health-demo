import random

class HealthDataSimulator:
    def __init__(self):
        self.t = 0
        self.voltage = 4.00
        self.temp = 30.0
        self.latency = 15
        self.retry = 0
        self.bod = 0

    def next_sample(self):
        self.t += 1

        self.voltage -= random.uniform(0.01, 0.03)
        self.temp += random.uniform(0.05, 0.30)
        self.latency += random.randint(1, 3)

        if self.voltage < 3.80:
            self.retry = min(self.retry + random.choice([0, 1]), 6)

        if self.voltage < 3.70:
            self.bod = min(self.bod + random.choice([0, 1]), 4)

        return {
            "time": self.t,
            "voltage": round(self.voltage, 2),
            "temp": round(self.temp, 1),
            "latency": self.latency,
            "retry": self.retry,
            "bod": self.bod
        }