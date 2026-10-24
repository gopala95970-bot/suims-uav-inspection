from datetime import datetime, timezone
from backend.database import insert, fetch_all
from backend.services.event_logger import log_event
from simulation.mission.state_machine import MissionStateMachine
from simulation.telemetry.simulator import TelemetrySimulator
from ai.vision.detector import inspect_frame
from backend.services.risk_engine import calculate_risk
from backend.services.decision_engine import decide
from backend.services.safety_arbiter import arbitrate

class MissionController:
    def __init__(self):
        self.mission = MissionStateMachine()
        self.telemetry = TelemetrySimulator()
        self.mission_id = None
        self.last = None
        self.failures = {"low_battery": False, "gps_loss": False, "telemetry_loss": False, "high_wind": False}

    def start(self):
        if self.mission_id is None:
            now = datetime.now(timezone.utc).isoformat()
            self.mission_id = insert("missions", {"name": "SUIMS DEMO MISSION", "status": "RUNNING", "started_at": now, "completed_at": None, "created_at": now})
            log_event("INFO", "MISSION", "MISSION_STARTED", "Autonomous inspection mission started", self.mission_id)
        self.mission.start()
        return self.snapshot()

    def stop(self):
        self.mission.stop()
        if self.mission_id:
            now = datetime.now(timezone.utc).isoformat()
            insert("events", {"timestamp": now, "level": "INFO", "source": "MISSION", "event": "MISSION_STOPPED", "detail": "Mission stopped by operator", "mission_id": self.mission_id})
        return self.snapshot()

    def set_failures(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.failures:
                self.failures[k] = bool(v)
        log_event("WARNING", "SIMULATOR", "FAILURE_INJECTION", str(self.failures), self.mission_id)
        return self.tick()

    def tick(self):
        t = self.telemetry.read()
        if self.failures["low_battery"]:
            t["battery"] = min(t["battery"], 16)
        if self.failures["gps_loss"]:
            t["gps_ok"] = False
        if self.failures["telemetry_loss"]:
            t["telemetry_link"] = False
        if self.failures["high_wind"]:
            t["wind_risk"] = 92

        if self.mission.running:
            self.mission.tick()

        detection = inspect_frame("T04")
        risk = calculate_risk(
            detection["defect_type"], detection["confidence"], detection["severity"],
            detection["recurring"], t["wind_risk"]
        )
        proposed = decide(risk, uncertainty=0.31, battery=t["battery"], distance_m=142)
        safety = arbitrate(t, proposed["action"])
        final = safety["action"]

        if self.mission.state in {"RETURN_HOME", "COMPLETE"}:
            final = self.mission.state

        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "proposed_action": proposed["action"],
            "final_action": final,
            "reason": safety["reason"] if safety["blocked"] else proposed["reason"],
            "priority": safety["priority"],
            "risk_score": risk["score"],
            "mission_id": self.mission_id
        }
        if self.mission_id:
            insert("decisions", row)
            insert("detections", {
                "timestamp": row["timestamp"], "asset_id": detection["asset_id"],
                "defect_type": detection["defect_type"], "confidence": detection["confidence"],
                "severity": detection["severity"], "recurring": int(detection["recurring"]),
                "source": detection["source"], "risk_score": risk["score"], "mission_id": self.mission_id
            })

        if safety["blocked"]:
            self.mission.apply_safety_action(final)
            log_event("CRITICAL" if safety["priority"] == "SAFETY" else "WARNING", "SAFETY", final, safety["reason"], self.mission_id)

        self.last = {
            "telemetry": t, "detection": detection, "risk": risk,
            "proposed": proposed, "safety": safety, "final_action": final,
            "mission": self.mission.snapshot()
        }
        return self.snapshot()

    def snapshot(self):
        base = self.last or {
            "telemetry": self.telemetry.read(),
            "detection": inspect_frame("T04"),
            "risk": calculate_risk("insulator_crack", .94, "major", True, 15),
            "proposed": {"action": "RE-INSPECT", "reason": "Awaiting mission tick", "priority": "MISSION"},
            "safety": {"action": "RE-INSPECT", "reason": "Awaiting mission tick", "priority": "MISSION", "blocked": False},
            "final_action": "RE-INSPECT",
            "mission": self.mission.snapshot()
        }
        base["failures"] = self.failures.copy()
        return base

controller = MissionController()
