def inspect_frame(asset_id="T04"):
    # Illustrative CV adapter. Replace with a real detector later.
    return {
        "asset_id": asset_id,
        "defect_type": "insulator_crack",
        "confidence": 0.94,
        "severity": "major",
        "recurring": True,
        "source": "SIMULATED_FRAME",
        "implementation_status": "SIMULATED"
    }
