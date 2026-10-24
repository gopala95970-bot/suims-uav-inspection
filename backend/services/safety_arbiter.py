# Deterministic safety authority. AI recommendations cannot override these rules.
PRIORITY_ORDER = {"SAFETY": 4, "BATTERY": 3, "MISSION": 2, "NAVIGATION": 1}

def arbitrate(telemetry, proposed_action):
    if telemetry.get("telemetry_link") is False:
        return {"action": "RETURN_HOME", "reason": "Telemetry link lost", "priority": "SAFETY", "blocked": True}
    if telemetry.get("gps_ok") is False:
        return {"action": "HOLD", "reason": "GPS integrity unavailable", "priority": "SAFETY", "blocked": True}
    if telemetry.get("wind_risk", 0) >= 85:
        return {"action": "RETURN_HOME", "reason": "Wind risk above safety threshold", "priority": "SAFETY", "blocked": True}
    if telemetry.get("battery", 100) <= 18:
        return {"action": "RETURN_HOME", "reason": "Battery critical", "priority": "BATTERY", "blocked": True}
    if telemetry.get("battery", 100) <= 25:
        return {"action": "RETURN_HOME", "reason": "Battery reserve threshold reached", "priority": "BATTERY", "blocked": True}
    return {"action": proposed_action, "reason": "No safety constraint blocked mission intent", "priority": "MISSION", "blocked": False}
