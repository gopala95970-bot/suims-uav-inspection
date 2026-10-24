# SUIMS System Architecture

## Closed-loop control

`Inspect → Detect → Assess Risk → Decide → Act → Update Condition History → Replan`

## Safety boundary

The adaptive decision engine proposes mission actions. The deterministic safety arbiter has final authority over safety-critical actions.

`AI recommendation → Safety arbitration → UAV command`

The AI cannot bypass:
- GPS integrity checks
- telemetry link checks
- wind thresholds
- battery reserve thresholds

## Data model

Missions
- mission lifecycle and timestamps

Events
- safety, mission, simulator, operator events

Detections
- asset, defect, confidence, severity, recurrence, risk

Decisions
- proposed action, final action, reason, priority, risk

## Prototype vs future

Implemented:
- simulation
- deterministic safety rules
- explainable risk score
- adaptive decision rules
- dashboard
- persistence

Simulated:
- UAV telemetry
- camera/CV detections
- weather/wind
- flight movement

Future integration:
- PX4/ArduPilot
- real camera inference
- real GIS/asset database
- field telemetry
- production authentication
- cloud deployment
