def decide(risk, uncertainty, battery, distance_m, mission_priority="NORMAL"):
    score = risk.get("score", 0)
    if score >= 75 and uncertainty >= 0.25 and battery >= 35 and distance_m <= 500:
        return {"action": "RE-INSPECT", "reason": "High risk plus material uncertainty justifies a closer inspection", "priority": "MISSION"}
    if score >= 75 and battery < 35:
        return {"action": "DEFER", "reason": "High-risk asset detected but battery reserve limits safe inspection", "priority": "MISSION"}
    if score >= 55:
        return {"action": "PRIORITIZE", "reason": "Risk exceeds prioritization threshold", "priority": "MISSION"}
    if mission_priority == "HIGH":
        return {"action": "INSPECT", "reason": "Mission priority is high and no safety constraint blocks inspection", "priority": "MISSION"}
    return {"action": "CONTINUE", "reason": "Risk is below adaptive intervention threshold", "priority": "NAVIGATION"}
