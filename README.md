# SUIMS — Smart UAV Inspection & Monitoring System

An autonomous, risk-aware UAV inspection platform for power infrastructure.

## What is implemented

- Cinematic black / electric-blue / purple mission-control frontend
- Zero-dependency Python backend using the standard library
- SQLite persistence
- REST-style API
- Real-time polling dashboard
- Mission state machine
- Deterministic safety arbitration: Safety > Battery > Mission > Navigation
- Explainable risk scoring
- Adaptive inspection decision engine
- Simulated computer-vision detections
- Telemetry simulation
- Failure injection: low battery, GPS loss, telemetry loss, high wind
- Mission history and event log
- Scenario runner for judge demonstrations
- Automated core tests

## Honest prototype scope

This repository is a software prototype. UAV telemetry, CV detections, weather, and flight behavior are simulated. The architecture is designed so real autopilot telemetry, camera inference, and field data can replace those adapters later.

## Run

Requires Python 3.10+.

```bash
python backend/main.py
```

Open:

`http://localhost:8000`

No npm, pip, Vite, Tailwind, or external services are required.

## Demo flow

1. Start a mission.
2. Watch the UAV transition through TAKEOFF → NAVIGATE → INSPECT → ANALYZE → REPLAN.
3. Open Risk Intelligence and inspect the explainable score.
4. Use Scenario Controls to inject HIGH WIND, GPS LOSS, TELEMETRY LOSS, or LOW BATTERY.
5. Observe the deterministic safety arbiter override mission intent.
6. Inspect the event timeline and mission history.

## Architecture

```text
                  ┌──────────────────────────┐
                  │     Mission Dashboard    │
                  │  Map / Telemetry / Risk  │
                  └────────────┬─────────────┘
                               │ REST / polling
                  ┌────────────▼─────────────┐
                  │       API Controller     │
                  └────────────┬─────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼────────┐   ┌─────────▼────────┐   ┌────────▼────────┐
│ Mission Engine │   │ Safety Arbiter   │   │ Decision Engine │
│ State machine  │   │ deterministic    │   │ risk-aware      │
└───────┬────────┘   └─────────┬────────┘   └────────┬────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Risk + Vision Layer │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ SQLite Data Layer   │
                    └─────────────────────┘
```

## Design principle

**Safety enforced by architecture, not by AI judgment.**

The AI/risk layer can recommend an action. The deterministic safety arbiter has final authority over safety-critical actions.
