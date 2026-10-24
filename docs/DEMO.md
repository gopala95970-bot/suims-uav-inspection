# Judge Demo Script

### Scenario A — Normal mission
Start mission and press simulation ticks. Show:
- UAV state
- battery
- GPS
- T04 detection
- risk score
- RE-INSPECT recommendation

### Scenario B — High wind
Enable HIGH WIND.
Expected:
`RETURN_HOME`
Priority:
`SAFETY`
Reason:
`Wind risk above safety threshold`

### Scenario C — GPS loss
Enable GPS LOSS.
Expected:
`HOLD`
Priority:
`SAFETY`

### Scenario D — Low battery
Enable LOW BATTERY.
Expected:
`RETURN_HOME`
Priority:
`BATTERY`

### Key statement

“SUIMS does not allow the AI recommendation to directly control the aircraft. The recommendation is evaluated by a deterministic safety layer, and safety-critical constraints have final authority.”
