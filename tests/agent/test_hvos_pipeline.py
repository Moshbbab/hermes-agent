from agent.hvos_pipeline import HermesHVOSPipeline


def _base_payload():
    return {
        "files": [
            {
                "id": "comps.csv",
                "records": [
                    {
                        "type": "comp",
                        "price": 1_000_000,
                        "metric": 1000,
                        "name": "Comp A",
                        "adjustment_evidence": [{"type": "paired_sale", "source": "MLS-001"}],
                    },
                    {
                        "type": "comp",
                        "price": 1_100_000,
                        "metric": 1100,
                        "name": "Comp B",
                        "adjustment_evidence": [{"type": "paired_sale", "source": "MLS-002"}],
                    },
                    {
                        "type": "comp",
                        "price": 1_050_000,
                        "metric": 1050,
                        "name": "Comp C",
                        "adjustment_evidence": [{"type": "paired_sale", "source": "MLS-003"}],
                    },
                ],
            }
        ],
        "subject": {"metric": 1080, "name": "Subject"},
        "adjustment_rules": {"metric_factor": 0.0004},
        "enabled_modules": {"dcf": False, "cost": False},
    }


def test_pipeline_pass_flow_returns_contract_and_final_value():
    pipeline = HermesHVOSPipeline()
    result = pipeline.run(_base_payload())

    assert result["status"] == "ok"
    assert result["halted_step"] is None
    assert result["data_contract_version"] == "hvos.contract.v1"
    assert isinstance(result["structured_dataset"], dict)
    assert isinstance(result["adjusted_comps"], list)
    assert isinstance(result["valuation_results"], dict)
    assert isinstance(result["final_value"], float)


def test_pipeline_fail_flow_stops_on_data_gate():
    payload = _base_payload()
    payload["files"][0]["records"] = []

    pipeline = HermesHVOSPipeline()
    result = pipeline.run(payload)

    assert result["status"] == "error"
    assert result["halted_step"] == "data_gate"
    assert result["error"]["code"] == "DATA_GATE_FAILED"
    executed_steps = [entry["step"] for entry in result["logs"]]
    assert "adjustment" not in executed_steps
    assert "valuation" not in executed_steps


def test_pipeline_missing_data_returns_structured_error():
    payload = _base_payload()
    payload.pop("subject")

    pipeline = HermesHVOSPipeline()
    result = pipeline.run(payload)

    assert result["status"] == "error"
    assert result["halted_step"] == "data_structuring"
    assert result["error"]["code"] == "MISSING_DATA"
    assert "missing_fields" in result["error"]["details"]


def test_pipeline_outlier_flow_filters_outlier_before_adjustment():
    payload = _base_payload()
    payload["files"][0]["records"].append(
        {
            "type": "comp",
            "price": 8_000_000,
            "metric": 900,
            "name": "Comp Outlier",
            "adjustment_evidence": [{"type": "paired_sale", "source": "MLS-999"}],
        }
    )

    pipeline = HermesHVOSPipeline()
    result = pipeline.run(payload)

    assert result["status"] == "ok"
    outliers = result["structured_dataset"]["quality"]["outlier_indices"]
    assert len(outliers) == 1
    adjusted_names = {comp["name"] for comp in result["adjusted_comps"]}
    assert "Comp Outlier" not in adjusted_names


def test_pipeline_dcf_flow_includes_dcf_value_when_enabled():
    payload = _base_payload()
    payload["enabled_modules"]["dcf"] = True
    payload["dcf_inputs"] = {
        "fcf1": 350_000,
        "discount_rate": 0.11,
        "growth_rate": 0.03,
    }

    pipeline = HermesHVOSPipeline()
    result = pipeline.run(payload)

    assert result["status"] == "ok"
    assert result["valuation_results"]["dcf"]["enabled"] is True
    assert result["valuation_results"]["dcf"]["value"] is not None
    assert result["final_value"] is not None
