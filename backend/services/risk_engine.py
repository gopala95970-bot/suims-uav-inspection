SEVERITY_BASE = {"minor": 20, "moderate": 45, "major": 70, "critical": 90}

def calculate_risk(defect_type, confidence, severity, recurring=False, weather_risk=0):
    base = SEVERITY_BASE.get(severity.lower(), 30)
    confidence_component = round(max(0.0, min(1.0, confidence)) * 20, 1)
    recurrence_component = 10 if recurring else 0
    weather_component = round(max(0, min(20, weather_risk * 0.2)), 1)
    score = min(100, round(base + confidence_component + recurrence_component + weather_component, 1))
    if score >= 80:
        level = "CRITICAL"
    elif score >= 60:
        level = "HIGH"
    elif score >= 35:
        level = "MEDIUM"
    else:
        level = "LOW"
    return {
        "score": score,
        "level": level,
        "components": {
            "base_severity": base,
            "confidence": confidence_component,
            "recurrence": recurrence_component,
            "weather": weather_component
        },
        "explanation": f"{defect_type}: severity={severity}, confidence={confidence:.2f}, recurring={recurring}, weather={weather_risk:.0f}"
    }
