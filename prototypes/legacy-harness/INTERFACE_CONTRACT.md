# Mission-thread interface contract

The candidate module exposes `process_event(event, config=None) -> dict` from `processor.py`.
The input and output must conform to the JSON schemas in `schemas/`. Observable semantics are:

1. Preserve `event_id`.
2. Compute `risk_score = round(clamp(100 * (0.70*signal_strength + 0.20*temperature_norm + 0.10*(1-quality))), 2)`, where `temperature_norm = clamp((temperature_c + 50)/200)`.
3. Classify scores below 35 as `nominal`, 35 through below 70 as `watch`, and 70 or above as `alert`.
4. Set confidence to `round(clamp(0.5 + 0.5*quality), 3)`.
5. Produce deterministic output for the same input and configuration.
6. Complete each event within 10 ms in the evaluation environment.
7. Do not require network access, undisclosed dependencies, vendor-only files, or secret configuration.
