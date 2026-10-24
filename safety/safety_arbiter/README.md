# Safety Arbiter

The production boundary for safety-critical action arbitration.

Current prototype implementation lives in `backend/services/safety_arbiter.py` and is deterministic.

Priority:
1. SAFETY
2. BATTERY
3. MISSION
4. NAVIGATION
