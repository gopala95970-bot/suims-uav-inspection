STATES = ["IDLE", "TAKEOFF", "NAVIGATE", "INSPECT", "ANALYZE", "REPLAN", "RETURN_HOME", "COMPLETE"]

class MissionStateMachine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = "IDLE"
        self.running = False
        self.cycles = 0

    def start(self):
        self.running = True
        if self.state == "IDLE":
            self.state = "TAKEOFF"

    def stop(self):
        self.running = False
        self.state = "COMPLETE"

    def tick(self):
        if not self.running:
            return
        self.cycles += 1
        transitions = {
            "TAKEOFF": "NAVIGATE",
            "NAVIGATE": "INSPECT",
            "INSPECT": "ANALYZE",
            "ANALYZE": "REPLAN",
            "REPLAN": "NAVIGATE",
        }
        self.state = transitions.get(self.state, self.state)

    def apply_safety_action(self, action):
        if action == "RETURN_HOME":
            self.state = "RETURN_HOME"
        elif action == "HOLD":
            self.state = "INSPECT"

    def snapshot(self):
        return {"state": self.state, "running": self.running, "cycle": self.cycles}
