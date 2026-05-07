"""HVOS deterministic valuation pipeline controller.

Pipeline order:
file_ingestion -> data_cleaning -> data_structuring -> data_gate ->
adjustment -> valuation -> reconciliation
"""

from __future__ import annotations

import logging
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, MutableMapping, Optional

from agent.hvos_steps import HVOSStepError, SharedDataContract, StepOutcome, run_step

logger = logging.getLogger(__name__)

PIPELINE_SEQUENCE = [
    "file_ingestion",
    "data_cleaning",
    "data_structuring",
    "data_gate",
    "adjustment",
    "valuation",
    "reconciliation",
]

DATA_CONTRACT_VERSION = "hvos.contract.v1"


@dataclass
class StepLog:
    step: str
    status: str
    timestamp: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    assumptions: List[str]
    error: Optional[Dict[str, Any]] = None


@dataclass
class PipelineResult:
    status: str
    halted_step: Optional[str]
    contract: SharedDataContract
    logs: List[StepLog] = field(default_factory=list)
    error: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "halted_step": self.halted_step,
            "data_contract_version": DATA_CONTRACT_VERSION,
            **self.contract.to_dict(),
            "logs": [asdict(log_entry) for log_entry in self.logs],
            "error": self.error,
        }


class HermesHVOSPipeline:
    """Deterministic pipeline with strict gate controls and structured output."""

    def __init__(self) -> None:
        self.sequence = PIPELINE_SEQUENCE

    def run(self, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        contract = SharedDataContract()
        state: MutableMapping[str, Any] = deepcopy(input_payload)
        state["contract"] = contract
        result = PipelineResult(status="ok", halted_step=None, contract=contract)

        for step_name in self.sequence:
            inputs = deepcopy(dict(state))
            if "contract" in inputs:
                inputs["contract"] = contract.to_dict()
            timestamp = datetime.now(timezone.utc).isoformat()
            try:
                outcome = run_step(step_name, state)
                state.update(outcome.payload)
                self._record_step(result=result, step_name=step_name, inputs=inputs, outcome=outcome, timestamp=timestamp)

                if step_name == "data_gate" and outcome.payload.get("gate_status") != "PASS":
                    gate_error = {
                        "code": "DATA_GATE_FAILED",
                        "message": "Data gate failed; valuation and reconciliation were blocked",
                        "step": "data_gate",
                        "details": {"reasons": outcome.payload.get("reasons", [])},
                    }
                    result.status = "error"
                    result.halted_step = "data_gate"
                    result.error = gate_error
                    return result.to_dict()
            except HVOSStepError as exc:
                error_payload = exc.as_dict()
                self._record_step_error(
                    result=result,
                    step_name=step_name,
                    inputs=inputs,
                    error_payload=error_payload,
                    timestamp=timestamp,
                )
                logger.error("HVOS step=%s failed code=%s", step_name, exc.code)
                result.status = "error"
                result.halted_step = step_name
                result.error = error_payload
                return result.to_dict()

        result.status = "ok"
        result.halted_step = None
        return result.to_dict()

    @staticmethod
    def _record_step(result: PipelineResult, step_name: str, inputs: Dict[str, Any], outcome: StepOutcome, timestamp: str) -> None:
        result.logs.append(
            StepLog(
                step=step_name,
                status=outcome.status,
                timestamp=timestamp,
                inputs=inputs,
                outputs=deepcopy(outcome.payload),
                assumptions=list(outcome.assumptions),
                error=outcome.error,
            )
        )
        logger.info("HVOS step=%s status=%s", step_name, outcome.status)

    @staticmethod
    def _record_step_error(
        result: PipelineResult,
        step_name: str,
        inputs: Dict[str, Any],
        error_payload: Dict[str, Any],
        timestamp: str,
    ) -> None:
        result.logs.append(
            StepLog(
                step=step_name,
                status="error",
                timestamp=timestamp,
                inputs=inputs,
                outputs={},
                assumptions=[],
                error=error_payload,
            )
        )
