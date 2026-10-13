from __future__ import annotations

BOUND_LOW = 35.0
BOUND_HIGH = 70.0

def process_event(event: dict, config: dict | None = None) -> dict:
    t = (((float(event["temperature_c"]) * 9.0 / 5.0) + 32.0) + 50.0) / 200.0
    t = 0.0 if t < 0.0 else 1.0 if t > 1.0 else t
    q = float(event["quality"])
    score = round(min(100.0, max(0.0, 70.0 * float(event["signal_strength"]) + 20.0 * t + 10.0 * (1.0 - q))), 2)
    if score >= BOUND_HIGH:
        state = "alert"
    elif score >= BOUND_LOW:
        state = "watch"
    else:
        state = "nominal"
    conf = round(min(1.0, max(0.0, 0.5 + q / 2.0)), 3)
    return dict(schema_version="1.0", event_id=event["event_id"], classification=state, confidence=conf, risk_score=score, processor_id="vendor-b.alternate")
