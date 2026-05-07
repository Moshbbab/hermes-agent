"""Core HVOS step implementations for the deterministic valuation pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping, MutableMapping, Optional


@dataclass(frozen=True)
class StepOutcome:
    """Represents the deterministic output of a single pipeline step."""

    status: str
    payload: Dict[str, Any]
    assumptions: List[str]
    error: Optional[Dict[str, Any]] = None


@dataclass
class SharedDataContract:
    """Strict data contract shared across every stage in the HVOS pipeline."""

    structured_dataset: Dict[str, Any] = field(
        default_factory=lambda: {
            "subject": None,
            "comparables": [],
            "quality": {"outlier_indices": [], "usable_count": 0},
        }
    )
    adjusted_comps: List[Dict[str, Any]] = field(default_factory=list)
    valuation_results: Dict[str, Any] = field(
        default_factory=lambda: {
            "market": None,
            "dcf": None,
            "cost": None,
        }
    )
    final_value: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HVOSStepError(Exception):
    """Structured exception type used by step implementations."""

    def __init__(self, code: str, message: str, step: str, details: Optional[Mapping[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.step = step
        self.details = dict(details or {})

    def as_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "step": self.step,
            "details": self.details,
        }


def _require_keys(data: Mapping[str, Any], step: str, required: List[str]) -> None:
    missing = [key for key in required if key not in data or data[key] is None]
    if missing:
        raise HVOSStepError(
            code="MISSING_DATA",
            message=f"Missing required input fields for {step}",
            step=step,
            details={"missing_fields": missing},
        )


def _require_contract(state: MutableMapping[str, Any], step: str) -> SharedDataContract:
    contract = state.get("contract")
    if not isinstance(contract, SharedDataContract):
        raise HVOSStepError(
            code="INVALID_CONTRACT",
            message="Shared data contract is missing or invalid",
            step=step,
        )
    return contract


def _percentile(sorted_values: List[float], percentile: float) -> float:
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = (len(sorted_values) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def file_ingestion(input_payload: MutableMapping[str, Any]) -> StepOutcome:
    step = "file_ingestion"
    _require_contract(input_payload, step)
    _require_keys(input_payload, step, ["files"])
    files = input_payload["files"]
    if not isinstance(files, list) or not files:
        raise HVOSStepError(
            code="MISSING_DATA",
            message="At least one file payload is required",
            step=step,
            details={"field": "files"},
        )

    for index, file_payload in enumerate(files):
        if not isinstance(file_payload, Mapping):
            raise HVOSStepError(
                code="INVALID_INPUT",
                message="Each file payload must be a mapping",
                step=step,
                details={"index": index},
            )
        _require_keys(file_payload, step, ["id", "records"])

    return StepOutcome(status="ok", payload={"ingested_files": files}, assumptions=[])


def data_cleaning(input_payload: MutableMapping[str, Any]) -> StepOutcome:
    step = "data_cleaning"
    _require_contract(input_payload, step)
    _require_keys(input_payload, step, ["ingested_files"])

    cleaned_files: List[Dict[str, Any]] = []
    for file_payload in input_payload["ingested_files"]:
        cleaned_records = []
        for record in file_payload.get("records", []):
            if not isinstance(record, Mapping):
                continue
            cleaned_record = {k: v for k, v in record.items() if v is not None}
            if cleaned_record:
                cleaned_records.append(cleaned_record)
        cleaned_files.append({"id": file_payload["id"], "records": cleaned_records})

    if not cleaned_files:
        raise HVOSStepError(
            code="MISSING_DATA",
            message="No usable records after cleaning",
            step=step,
        )

    return StepOutcome(status="ok", payload={"cleaned_files": cleaned_files}, assumptions=[])


def data_structuring(input_payload: MutableMapping[str, Any]) -> StepOutcome:
    step = "data_structuring"
    contract = _require_contract(input_payload, step)
    _require_keys(input_payload, step, ["cleaned_files", "subject"])

    comps: List[Dict[str, Any]] = []
    for file_payload in input_payload["cleaned_files"]:
        for record in file_payload.get("records", []):
            if record.get("type") == "comp":
                comps.append(dict(record))

    contract.structured_dataset = {
        "subject": dict(input_payload["subject"]),
        "comparables": comps,
        "quality": {"outlier_indices": [], "usable_count": len(comps)},
    }
    return StepOutcome(status="ok", payload={"structured_dataset": contract.structured_dataset}, assumptions=[])


def data_gate(input_payload: MutableMapping[str, Any]) -> StepOutcome:
    step = "data_gate"
    contract = _require_contract(input_payload, step)
    dataset = contract.structured_dataset
    _require_keys(dataset, step, ["subject", "comparables"])

    comparables = dataset["comparables"]
    if not isinstance(comparables, list) or not comparables:
        return StepOutcome(
            status="fail",
            payload={"gate_status": "FAIL", "reasons": ["No comparable set provided"]},
            assumptions=[],
        )

    required_comp_fields = {"price", "metric"}
    reasons = []
    ratios: List[float] = []
    valid_indexes: List[int] = []
    for idx, comp in enumerate(comparables):
        missing = sorted(required_comp_fields - set(comp.keys()))
        if missing:
            reasons.append(f"Comparable {idx} missing fields: {', '.join(missing)}")
            continue

        metric = float(comp["metric"])
        if metric <= 0:
            reasons.append(f"Comparable {idx} metric must be > 0")
            continue
        ratios.append(float(comp["price"]) / metric)
        valid_indexes.append(idx)

    if reasons:
        return StepOutcome(status="fail", payload={"gate_status": "FAIL", "reasons": reasons}, assumptions=[])

    sorted_ratios = sorted(ratios)
    q1 = _percentile(sorted_ratios, 0.25)
    q3 = _percentile(sorted_ratios, 0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outlier_indices: List[int] = []
    usable_count = 0
    for original_idx, ratio in zip(valid_indexes, ratios):
        if ratio < lower or ratio > upper:
            outlier_indices.append(original_idx)
        else:
            usable_count += 1

    dataset["quality"] = {
        "outlier_indices": sorted(outlier_indices),
        "usable_count": usable_count,
        "ratio_bounds": {"lower": lower, "upper": upper},
    }

    if usable_count < 2:
        return StepOutcome(
            status="fail",
            payload={"gate_status": "FAIL", "reasons": ["Insufficient non-outlier comparables"]},
            assumptions=[],
        )

    return StepOutcome(status="ok", payload={"gate_status": "PASS", "reasons": []}, assumptions=[])


def adjustment(input_payload: MutableMapping[str, Any]) -> StepOutcome:
    step = "adjustment"
    contract = _require_contract(input_payload, step)
    _require_keys(input_payload, step, ["adjustment_rules"])

    dataset = contract.structured_dataset
    _require_keys(dataset, step, ["subject", "comparables", "quality"])
    subject_metric = float(dataset["subject"].get("metric"))
    comparables = dataset["comparables"]
    quality = dataset["quality"]
    outlier_indices = set(quality.get("outlier_indices", []))

    rules = input_payload["adjustment_rules"]
    factor = float(rules.get("metric_factor", 0.0))

    adjusted_comps = []
    assumptions: List[str] = []
    for idx, comp in enumerate(comparables):
        if idx in outlier_indices:
            continue

        metric = float(comp["metric"])
        price = float(comp["price"])
        adjustment_pct = (subject_metric - metric) * factor

        evidence_items = comp.get("adjustment_evidence", [])
        assumption_flag = comp.get("assumption_flag")
        has_evidence = isinstance(evidence_items, list) and len(evidence_items) > 0
        has_assumption_flag = isinstance(assumption_flag, str) and bool(assumption_flag.strip())

        if adjustment_pct != 0 and not has_evidence and not has_assumption_flag:
            raise HVOSStepError(
                code="ADJUSTMENT_EVIDENCE_REQUIRED",
                message="Adjustment requires explicit evidence or flagged assumption",
                step=step,
                details={"comparable": comp.get("name", idx)},
            )

        if has_assumption_flag:
            assumptions.append(f"Comparable {comp.get('name', idx)} assumption_flag: {assumption_flag}")

        adjusted_comps.append(
            {
                **comp,
                "adjustment_pct": adjustment_pct,
                "adjusted_price": price * (1 + adjustment_pct),
                "adjustment_basis": {
                    "evidence": evidence_items if has_evidence else [],
                    "assumption_flag": assumption_flag if has_assumption_flag else None,
                    "is_outlier_filtered": False,
                },
            }
        )

    contract.adjusted_comps = adjusted_comps
    return StepOutcome(status="ok", payload={"adjusted_comps": adjusted_comps}, assumptions=assumptions)


def _compute_dcf_value(step: str, dcf_inputs: Mapping[str, Any]) -> float:
    _require_keys(dcf_inputs, step, ["fcf1", "discount_rate", "growth_rate"])
    fcf1 = float(dcf_inputs["fcf1"])
    discount_rate = float(dcf_inputs["discount_rate"])
    growth_rate = float(dcf_inputs["growth_rate"])

    if discount_rate <= growth_rate:
        raise HVOSStepError(
            code="INVALID_INPUT",
            message="discount_rate must be greater than growth_rate for Gordon Growth",
            step=step,
            details={"discount_rate": discount_rate, "growth_rate": growth_rate},
        )
    return fcf1 / (discount_rate - growth_rate)


def valuation(input_payload: MutableMapping[str, Any]) -> StepOutcome:
    step = "valuation"
    contract = _require_contract(input_payload, step)
    _require_keys(input_payload, step, ["enabled_modules"])

    adjusted_comps = contract.adjusted_comps
    if not adjusted_comps:
        raise HVOSStepError(
            code="MISSING_DATA",
            message="No adjusted comparables available for valuation",
            step=step,
        )

    market_values = [float(comp["adjusted_price"]) for comp in adjusted_comps]
    market_method_value = sum(market_values) / len(market_values)

    enabled_modules = input_payload["enabled_modules"]
    dcf_enabled = bool(enabled_modules.get("dcf", False))
    dcf_value = None
    assumptions: List[str] = []

    if dcf_enabled:
        dcf_inputs = input_payload.get("dcf_inputs")
        if not isinstance(dcf_inputs, Mapping):
            raise HVOSStepError(
                code="MISSING_DATA",
                message="dcf_inputs are required when DCF module is enabled",
                step=step,
                details={"missing_fields": ["dcf_inputs"]},
            )
        dcf_value = _compute_dcf_value(step=step, dcf_inputs=dcf_inputs)
        assumptions.append("DCF computed with Gordon Growth perpetuity model")

    contract.valuation_results = {
        "market": {
            "enabled": True,
            "value": market_method_value,
            "input_count": len(market_values),
        },
        "dcf": {
            "enabled": dcf_enabled,
            "value": dcf_value,
        },
        "cost": {
            "enabled": bool(enabled_modules.get("cost", False)),
            "value": None,
        },
    }

    return StepOutcome(status="ok", payload={"valuation_results": contract.valuation_results}, assumptions=assumptions)


def reconciliation(input_payload: MutableMapping[str, Any]) -> StepOutcome:
    step = "reconciliation"
    contract = _require_contract(input_payload, step)
    results = contract.valuation_results

    weighted_components = []
    market_value = results.get("market", {}).get("value") if isinstance(results.get("market"), Mapping) else None
    dcf_value = results.get("dcf", {}).get("value") if isinstance(results.get("dcf"), Mapping) else None

    if market_value is not None:
        weighted_components.append((float(market_value), 0.7))
    if dcf_value is not None:
        weighted_components.append((float(dcf_value), 0.3))

    if not weighted_components:
        raise HVOSStepError(
            code="MISSING_DATA",
            message="No valuation module produced a numeric value",
            step=step,
        )

    numerator = sum(value * weight for value, weight in weighted_components)
    denominator = sum(weight for _, weight in weighted_components)
    final_value = numerator / denominator
    contract.final_value = final_value

    return StepOutcome(status="ok", payload={"final_value": final_value}, assumptions=[])


def run_step(step_name: str, state: MutableMapping[str, Any]) -> StepOutcome:
    """Execute one named step using deterministic step mapping."""

    step_map = {
        "file_ingestion": file_ingestion,
        "data_cleaning": data_cleaning,
        "data_structuring": data_structuring,
        "data_gate": data_gate,
        "adjustment": adjustment,
        "valuation": valuation,
        "reconciliation": reconciliation,
    }
    try:
        handler = step_map[step_name]
    except KeyError as exc:
        raise HVOSStepError(
            code="INVALID_STEP",
            message=f"Unsupported step: {step_name}",
            step=step_name,
        ) from exc
    return handler(state)
