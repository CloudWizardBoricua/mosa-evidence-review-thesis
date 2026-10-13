from __future__ import annotations

def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))

def process_event(event: dict, config: dict | None = None) -> dict:
    temp_norm = _clamp((float(event["temperature_c"]) + 50.0) / 200.0)
    risk = 100.0 * (0.70 * float(event["signal_strength"]) + 0.20 * temp_norm + 0.10 * (1.0 - float(event["quality"])))
    risk = round(_clamp(risk / 100.0) * 100.0, 2)
    classification = "nominal" if risk < 35.0 else ("watch" if risk < 70.0 else "alert")
    confidence = round(_clamp(0.5 + 0.5 * float(event["quality"])), 3)
    return {"schema_version": "1.0", "event_id": event["event_id"], "classification": classification, "confidence": confidence, "risk_score": risk, "processor_id": "vendor-a.reference"}
