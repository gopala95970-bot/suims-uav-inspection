import unittest
from backend.services.risk_engine import calculate_risk
from backend.services.safety_arbiter import arbitrate
from backend.services.decision_engine import decide
from simulation.mission.state_machine import MissionStateMachine

class TestSUIMS(unittest.TestCase):
    def test_critical_wind_overrides(self):
        out = arbitrate({"battery": 80, "wind_risk": 95, "gps_ok": True, "telemetry_link": True}, "RE-INSPECT")
        self.assertEqual(out["action"], "RETURN_HOME")
        self.assertTrue(out["blocked"])

    def test_gps_loss_holds(self):
        out = arbitrate({"battery": 80, "wind_risk": 10, "gps_ok": False, "telemetry_link": True}, "CONTINUE")
        self.assertEqual(out["action"], "HOLD")

    def test_risk_is_bounded(self):
        out = calculate_risk("insulator_crack", 1.0, "critical", True, 100)
        self.assertEqual(out["score"], 100)
        self.assertEqual(out["level"], "CRITICAL")

    def test_adaptive_reinspect(self):
        risk = calculate_risk("insulator_crack", .94, "major", True, 10)
        out = decide(risk, .31, 70, 142)
        self.assertEqual(out["action"], "RE-INSPECT")

    def test_state_machine(self):
        sm = MissionStateMachine()
        sm.start()
        self.assertEqual(sm.state, "TAKEOFF")
        sm.tick()
        self.assertEqual(sm.state, "NAVIGATE")

if __name__ == "__main__":
    unittest.main()
