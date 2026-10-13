
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
import random
import statistics
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from .schemas import INPUT_SCHEMA, OUTPUT_SCHEMA, MANIFEST_SCHEMA

FORBIDDEN_IMPORTS = {"socket", "requests", "urllib", "http", "ftplib", "paramiko"}
ALLOWED_STDLIB = {"__future__", "math", "typing", "time", "random"}

@dataclass
class Finding:
    code: str
    category: str
    severity: str
    message: str

@dataclass
class BaselineResult:
    candidate: str
    passed: bool
    duration_ms: float
    checks_executed: int
    findings: list[dict[str, Any]]
    actionable_diagnosis: str | None
    evidence_completeness: float

@dataclass
class HarnessResult:
    candidate: str
    passed: bool
    duration_ms: float
    tests_executed: int
    findings: list[dict[str, Any]]
    structural_score: float
    operational_score: float
    competition_readiness_score: float
    security_score: float
    composite_score: float
    evidence_confidence: float
    gate_failure: bool
    evidence_completeness: float
    actionable_diagnosis: str | None
    evidence_digest: str


def _load_callable(candidate_dir: Path):
    module_path = candidate_dir / "processor.py"
    module_name = f"candidate_{candidate_dir.name}_{time.time_ns()}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    fn = getattr(module, "process_event")
    return fn


def expected_output(event: dict[str, Any]) -> dict[str, Any]:
    temp_norm = max(0.0, min(1.0, (float(event["temperature_c"]) + 50.0) / 200.0))
    risk = round(max(0.0, min(100.0, 100.0 * (0.70 * float(event["signal_strength"]) + 0.20 * temp_norm + 0.10 * (1.0 - float(event["quality"]))))), 2)
    cls = "nominal" if risk < 35.0 else ("watch" if risk < 70.0 else "alert")
    conf = round(max(0.0, min(1.0, 0.5 + 0.5 * float(event["quality"]))), 3)
    return {"schema_version":"1.0","event_id":event["event_id"],"classification":cls,"confidence":conf,"risk_score":risk}


def baseline_evaluate(candidate_dir: Path, vector: dict[str, Any]) -> BaselineResult:
    started = time.perf_counter_ns()
    findings: list[Finding] = []
    checks = 0
    evidence_count = 0
    try:
        checks += 1
        if not (candidate_dir / "manifest.json").exists():
            findings.append(Finding("B-MANIFEST", "missing_manifest", "high", "Manifest is missing"))
            raise FileNotFoundError("manifest missing")
        manifest = json.loads((candidate_dir / "manifest.json").read_text(encoding="utf-8"))
        evidence_count += 1
        checks += 1
        if manifest.get("interface_version") != "1.0":
            findings.append(Finding("B-INTERFACE-VERSION", "wrong_interface_version", "high", "Documented interface version is not 1.0"))
        evidence_count += 1
        checks += 1
        fn = _load_callable(candidate_dir)
        evidence_count += 1
        checks += 1
        out = fn(vector, {"vendor_secret": "baseline-default"})
        evidence_count += 1
        checks += 1
        if not isinstance(out, dict):
            findings.append(Finding("B-OUTPUT", "wrong_output_type", "high", "Output is not a mapping"))
        else:
            required = ("schema_version", "event_id", "classification", "confidence", "risk_score", "processor_id")
            for key in required:
                checks += 1
                if key not in out:
                    findings.append(Finding("B-KEY", "missing_output_field", "high", f"Required key {key} is missing"))
            if all(k in out for k in required):
                checks += 1
                if out.get("schema_version") != "1.0":
                    findings.append(Finding("B-SCHEMA-VERSION", "wrong_schema_version", "high", "Output schema version is not 1.0"))
                checks += 1
                if not isinstance(out.get("risk_score"), (int, float)) or not isinstance(out.get("confidence"), (int, float)):
                    findings.append(Finding("B-TYPE", "wrong_output_type", "high", "Numeric output fields have invalid types"))
                checks += 1
                if out.get("classification") not in {"nominal", "watch", "alert"}:
                    findings.append(Finding("B-ENUM", "wrong_output_type", "high", "Classification is outside the documented enumeration"))
                evidence_count += 1
    except Exception as exc:
        if not findings:
            findings.append(Finding("B-RUNTIME", "runtime", "high", f"Happy-path integration failed: {type(exc).__name__}: {exc}"))
    passed = not findings
    duration_ms = (time.perf_counter_ns() - started) / 1_000_000
    diagnosis = findings[0].category if findings else None
    return BaselineResult(candidate_dir.name, passed, duration_ms, checks, [asdict(f) for f in findings], diagnosis, round(evidence_count / 10.0, 3))


def _random_vectors(seed: int, n: int = 48) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    vectors = []
    for i in range(n):
        vectors.append({
            "schema_version":"1.0", "event_id":f"R-{seed}-{i}", "timestamp_ms":1000+i,
            "sensor_id":f"S-{rng.randrange(1,8)}", "temperature_c":rng.uniform(-50,150),
            "signal_strength":rng.random(), "quality":rng.random(),
        })
    return vectors


def harness_evaluate(candidate_dir: Path, fixed_vectors: list[dict[str, Any]], seed: int = 20260623) -> HarnessResult:
    started = time.perf_counter_ns()
    findings: list[Finding] = []
    tests = 0
    structural_items = []
    operational_items = []
    competition_items = []
    security_items = []
    evidence_items = []

    # Structural and evidence checks.
    manifest = None
    manifest_path = candidate_dir / "manifest.json"
    tests += 1
    if not manifest_path.exists():
        findings.append(Finding("H-MANIFEST-MISSING", "missing_manifest", "critical", "Machine-readable manifest is missing"))
        structural_items.append(0); evidence_items.append(0)
    else:
        evidence_items.append(1)
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            errors = list(Draft202012Validator(MANIFEST_SCHEMA).iter_errors(manifest))
            tests += 1
            if errors:
                code = "wrong_interface_version" if any("1.0" in e.message or "const" in e.message for e in errors) else "manifest_schema"
                findings.append(Finding("H-MANIFEST-SCHEMA", code, "critical", "; ".join(e.message for e in errors)))
                structural_items.append(0)
            else:
                structural_items.append(1)
        except Exception as exc:
            findings.append(Finding("H-MANIFEST-PARSE", "manifest_schema", "critical", str(exc)))
            structural_items.append(0)

    source_path = candidate_dir / "processor.py"
    tests += 1
    source = source_path.read_text(encoding="utf-8")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if manifest and manifest.get("source_sha256") == digest:
        structural_items.append(1); evidence_items.append(1)
    else:
        findings.append(Finding("H-PROVENANCE", "provenance_hash_mismatch", "critical", "Source digest does not match the manifest"))
        structural_items.append(0); evidence_items.append(0)

    tests += 1
    sbom_ok = bool(manifest and (candidate_dir / str(manifest.get("sbom", ""))).exists())
    if sbom_ok:
        evidence_items.append(1); competition_items.append(1)
    else:
        findings.append(Finding("H-SBOM", "missing_sbom", "high", "SBOM artifact is missing"))
        evidence_items.append(0); competition_items.append(0)

    # Static dependency and security checks.
    tests += 1
    tree = ast.parse(source)
    imports = set()
    file_calls = []
    global_statements = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split('.')[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'open':
            file_calls.append(node.lineno)
        elif isinstance(node, ast.Global):
            global_statements.extend(node.names)
    declared = set(manifest.get("declared_dependencies", [])) if manifest else set()
    undeclared = imports - ALLOWED_STDLIB - declared
    if undeclared:
        findings.append(Finding("H-DEPENDENCY", "undeclared_dependency", "high", f"Undeclared dependencies: {sorted(undeclared)}"))
        competition_items.append(0)
    else:
        competition_items.append(1)
    forbidden = imports & FORBIDDEN_IMPORTS
    if forbidden:
        findings.append(Finding("H-NETWORK", "forbidden_network_import", "critical", f"Forbidden network imports: {sorted(forbidden)}"))
        security_items.append(0)
    else:
        security_items.append(1)
    if file_calls:
        findings.append(Finding("H-FILE-DEPENDENCY", "hidden_file_dependency", "critical", f"Runtime file access at lines {file_calls}"))
        competition_items.append(0)
    else:
        competition_items.append(1)
    if global_statements:
        findings.append(Finding("H-MUTABLE-GLOBAL", "state_leakage", "critical", f"Mutable global state referenced: {sorted(set(global_statements))}"))
        operational_items.append(0)

    fn = None
    tests += 1
    try:
        fn = _load_callable(candidate_dir)
        structural_items.append(1)
    except Exception as exc:
        findings.append(Finding("H-LOAD", "runtime", "critical", f"Module load failed: {type(exc).__name__}: {exc}"))
        structural_items.append(0)

    vectors = fixed_vectors + _random_vectors(seed)
    outputs = []
    latencies = []
    if fn:
        for idx, event in enumerate(vectors):
            tests += 1
            in_errors = list(Draft202012Validator(INPUT_SCHEMA).iter_errors(event))
            if in_errors:
                findings.append(Finding("H-TEST-DATA", "test_data", "critical", in_errors[0].message))
                operational_items.append(0)
                continue
            try:
                t0 = time.perf_counter_ns()
                out = fn(dict(event), {})
                latencies.append((time.perf_counter_ns() - t0) / 1_000_000)
                outputs.append(out)
            except Exception as exc:
                cat = "configuration_coupling" if "vendor_secret" in str(exc) else ("edge_case_exception" if event.get("quality") == 0 else "runtime")
                findings.append(Finding("H-EXECUTION", cat, "critical", f"Vector {event['event_id']} failed: {type(exc).__name__}: {exc}"))
                operational_items.append(0)
                continue
            tests += 1
            out_errors = list(Draft202012Validator(OUTPUT_SCHEMA).iter_errors(out))
            if out_errors:
                msg = "; ".join(e.message for e in out_errors[:3])
                if "confidence" in msg and "required" in msg:
                    cat = "missing_output_field"
                elif "not of type 'number'" in msg:
                    cat = "wrong_output_type"
                elif "0.9" in msg or "1.0" in msg:
                    cat = "wrong_schema_version"
                else:
                    cat = "output_schema"
                findings.append(Finding("H-OUTPUT-SCHEMA", cat, "critical", f"Vector {event['event_id']}: {msg}"))
                operational_items.append(0)
                continue
            expected = expected_output(event)
            tests += 1
            semantic_ok = (
                out["event_id"] == expected["event_id"] and
                out["classification"] == expected["classification"] and
                math.isclose(float(out["risk_score"]), expected["risk_score"], abs_tol=0.01) and
                math.isclose(float(out["confidence"]), expected["confidence"], abs_tol=0.001)
            )
            if not semantic_ok:
                if out.get("event_id") != expected["event_id"]:
                    cat = "event_id_not_preserved"
                elif not math.isclose(float(out.get("risk_score", -9999)), expected["risk_score"], abs_tol=0.01):
                    cat = "units_error"
                elif out.get("classification") != expected["classification"]:
                    cat = "semantic_threshold_shift"
                else:
                    cat = "semantic_behavior"
                findings.append(Finding("H-SEMANTICS", cat, "critical", f"Observable behavior differs for {event['event_id']}"))
                operational_items.append(0)
            else:
                operational_items.append(1)

        # Determinism test on a mid-range vector.
        tests += 1
        try:
            event = dict(fixed_vectors[2])
            a = fn(dict(event), {})
            b = fn(dict(event), {})
            if a != b:
                findings.append(Finding("H-DETERMINISM", "nondeterministic_output", "critical", "Repeated execution produced different output"))
                operational_items.append(0)
            else:
                operational_items.append(1)
        except Exception:
            operational_items.append(0)

        # Latency criterion.
        tests += 1
        p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else (max(latencies) if latencies else float('inf'))
        if p95 > 10.0:
            findings.append(Finding("H-LATENCY", "latency_violation", "high", f"95th percentile event latency {p95:.3f} ms exceeds 10 ms"))
            operational_items.append(0)
        else:
            operational_items.append(1)

    # Data-rights and onboarding proxies.
    tests += 1
    if manifest and manifest.get("data_rights") in {"government-purpose-rights", "unlimited-rights", "open-source"}:
        competition_items.append(1)
    else:
        findings.append(Finding("H-DATA-RIGHTS", "data_rights", "high", "Data-rights posture is absent or insufficient"))
        competition_items.append(0)
    evidence_items.extend([1 if (candidate_dir / "README.md").exists() else 0, 1 if (candidate_dir / "processor.py").exists() else 0])

    def pct(items: list[int]) -> float:
        return round(100.0 * sum(items) / len(items), 2) if items else 0.0

    structural = pct(structural_items)
    operational = pct(operational_items)
    competition = pct(competition_items)
    security = pct(security_items)
    evidence_completeness = round(sum(evidence_items) / max(1, len(evidence_items)), 3)
    evidence_confidence = round(evidence_completeness * (1.0 if len(vectors) >= 50 else 0.8), 3)
    composite = round(0.35 * structural + 0.40 * operational + 0.15 * competition + 0.10 * security, 2)
    critical = any(f.severity in {"critical", "high"} for f in findings)
    passed = composite >= 80.0 and not critical
    diagnosis = None
    if findings:
        severity_priority = {"critical":0,"high":1,"medium":2,"low":3}
        root_priority = {
            "missing_manifest": 0, "wrong_interface_version": 1, "provenance_hash_mismatch": 2,
            "missing_sbom": 3, "forbidden_network_import": 4, "undeclared_dependency": 5,
            "hidden_file_dependency": 6, "state_leakage": 7, "configuration_coupling": 8,
            "edge_case_exception": 9, "latency_violation": 10, "nondeterministic_output": 11,
            "event_id_not_preserved": 12, "missing_output_field": 13, "wrong_output_type": 14,
            "wrong_schema_version": 15, "semantic_threshold_shift": 16, "units_error": 17,
        }
        diagnosis = sorted(findings, key=lambda f: (root_priority.get(f.category, 99), severity_priority[f.severity], f.code))[0].category
    canonical = {
        "candidate": candidate_dir.name,
        "passed": passed,
        "findings": [asdict(f) for f in sorted(findings, key=lambda x: (x.code, x.message))],
        "scores": {"structural":structural,"operational":operational,"competition_readiness":competition,"security":security,"composite":composite},
        "evidence_confidence": evidence_confidence,
    }
    evidence_digest = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    duration_ms = (time.perf_counter_ns() - started) / 1_000_000
    return HarnessResult(candidate_dir.name, passed, duration_ms, tests, [asdict(f) for f in findings], structural, operational, competition, security, composite, evidence_confidence, critical, evidence_completeness, diagnosis, evidence_digest)


def evaluate_candidate(candidate_dir: Path, fixed_vectors: list[dict[str, Any]], seed: int = 20260623):
    return baseline_evaluate(candidate_dir, fixed_vectors[0]), harness_evaluate(candidate_dir, fixed_vectors, seed)
