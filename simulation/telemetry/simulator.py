import random

class TelemetrySimulator:
    def __init__(self):
        self.battery = 78.0
        self.tick_count = 0

    def read(self):
        self.tick_count += 1
        self.battery = max(8.0, self.battery - 0.25)
        return {
            "battery": round(self.battery, 1),
            "altitude_m": round(42 + random.uniform(-1.5, 1.5), 1),
            "speed_mps": round(8.4 + random.uniform(-0.8, 0.8), 1),
            "satellites": random.randint(11, 15),
            "wind_risk": random.randint(8, 28),
            "gps_ok": True,
            "telemetry_link": True,
            "lat": 30.2458 + random.uniform(-0.0005, 0.0005),
            "lon": 75.8421 + random.uniform(-0.0005, 0.0005)
        }
