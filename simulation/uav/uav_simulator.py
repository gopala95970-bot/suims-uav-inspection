class UAVSimulator:
    """Adapter boundary for a future PX4/ArduPilot or real telemetry integration."""
    def command(self, action):
        return {"accepted": True, "action": action, "mode": "SIMULATION"}
