"""Tests for agent.land_impact_mapper."""

import pytest

from agent.land_impact_mapper import (
    LAND_SENSITIVITY_RANGE,
    LandImpactInput,
    LandImpactMapper,
    assess_hbu_risk,
    compute_developer_irr_adjustment,
    compute_final_pressure,
    compute_holding_risk_adjustment,
    compute_opportunity_cost_adjustment,
    compute_white_land_pressure,
    holding_period_multiplier,
)


# ---------------------------------------------------------------------------
# holding_period_multiplier
# ---------------------------------------------------------------------------

class TestHoldingPeriodMultiplier:
    def test_none_returns_one(self):
        assert holding_period_multiplier(None) == 1.0

    def test_zero_returns_one(self):
        assert holding_period_multiplier(0) == 1.0

    def test_one_year_returns_one(self):
        assert holding_period_multiplier(1) == 1.0

    def test_two_years_returns_1_15(self):
        assert holding_period_multiplier(2) == 1.15

    def test_three_years_returns_1_15(self):
        assert holding_period_multiplier(3) == 1.15

    def test_four_years_returns_1_35(self):
        assert holding_period_multiplier(4) == 1.35

    def test_five_years_returns_1_35(self):
        assert holding_period_multiplier(5) == 1.35

    def test_six_years_returns_1_60(self):
        assert holding_period_multiplier(6) == 1.60

    def test_twenty_years_returns_1_60(self):
        assert holding_period_multiplier(20) == 1.60


# ---------------------------------------------------------------------------
# compute_white_land_pressure
# ---------------------------------------------------------------------------

class TestComputeWhiteLandPressure:
    def test_outside_scope_returns_zero(self):
        result = compute_white_land_pressure(0.025, is_inside_scope=False, holding_years=5)
        assert result == 0.0

    def test_inside_scope_no_tax_rate_returns_zero(self):
        result = compute_white_land_pressure(None, is_inside_scope=True, holding_years=5)
        assert result == 0.0

    def test_inside_scope_zero_tax_returns_zero(self):
        result = compute_white_land_pressure(0.0, is_inside_scope=True, holding_years=5)
        assert result == 0.0

    def test_one_year_compounding(self):
        # (1 + 0.025)^1 - 1 = 0.025
        result = compute_white_land_pressure(0.025, is_inside_scope=True, holding_years=1)
        assert abs(result - 0.025) < 1e-9

    def test_two_year_compounding(self):
        # (1.025)^2 - 1 = 0.050625
        result = compute_white_land_pressure(0.025, is_inside_scope=True, holding_years=2)
        assert abs(result - ((1.025 ** 2) - 1)) < 1e-9

    def test_none_holding_years_treated_as_one(self):
        result_none = compute_white_land_pressure(0.025, is_inside_scope=True, holding_years=None)
        result_one = compute_white_land_pressure(0.025, is_inside_scope=True, holding_years=1)
        assert result_none == result_one

    def test_capped_at_50_pct(self):
        # High tax rate + long period should be capped at 0.50
        result = compute_white_land_pressure(0.50, is_inside_scope=True, holding_years=10)
        assert result == 0.50

    def test_result_never_exceeds_cap(self):
        result = compute_white_land_pressure(1.0, is_inside_scope=True, holding_years=50)
        assert result <= 0.50


# ---------------------------------------------------------------------------
# assess_hbu_risk
# ---------------------------------------------------------------------------

class TestAssessHbuRisk:
    def test_none_margin_returns_unknown(self):
        flag, haircut = assess_hbu_risk("residential_development_land", 100, None)
        assert flag == "UNKNOWN_REQUIRES_FEASIBILITY_TEST"
        assert haircut == 0.0

    def test_high_risk_when_margin_near_zero(self):
        # repo_shock=100 bps → erosion = 0.25% → margin must drop to ≤2%
        # base_margin = 0.02 → remaining = 0.02 - 0.0025 = 0.0175 ≤ 0.02
        flag, haircut = assess_hbu_risk("commercial_development_land", 100, base_margin_pct=0.02)
        assert flag == "HIGH"
        assert haircut == 0.30

    def test_moderate_risk_when_margin_between_2_and_5(self):
        # repo_shock=100 bps → erosion = 25/10000 = 0.0025 → remaining = 0.04 - 0.0025 = 0.0375
        flag, haircut = assess_hbu_risk("industrial_land", 100, base_margin_pct=0.04)
        assert flag == "MODERATE"
        assert haircut == 0.15

    def test_low_risk_with_healthy_margin(self):
        # repo_shock=50 bps → erosion = 12.5/10000 = 0.00125 → remaining = 0.15 - 0.00125 = 0.14875
        flag, haircut = assess_hbu_risk("raw_land_inside_urban_boundary", 50, base_margin_pct=0.15)
        assert flag == "LOW"
        assert haircut == 0.05

    def test_large_shock_pushes_margin_to_moderate(self):
        # repo_shock=400 bps → erosion = 100/10000 = 0.01 → remaining = 0.06 - 0.01 = 0.05
        # 0.05 satisfies <= 0.05 → MODERATE
        flag, haircut = assess_hbu_risk("approved_subdivision_land", 400, base_margin_pct=0.06)
        assert flag == "MODERATE"
        assert haircut == 0.15


# ---------------------------------------------------------------------------
# compute_developer_irr_adjustment
# ---------------------------------------------------------------------------

class TestComputeDeveloperIrrAdjustment:
    def test_returns_tuple_of_three(self):
        result = compute_developer_irr_adjustment("industrial_land", 100, None)
        assert len(result) == 3

    def test_low_le_central_le_high(self):
        low, central, high = compute_developer_irr_adjustment("commercial_development_land", 100, 3)
        assert low <= central <= high

    def test_holding_multiplier_applied(self):
        low1, central1, _ = compute_developer_irr_adjustment("industrial_land", 100, 1)
        low6, central6, _ = compute_developer_irr_adjustment("industrial_land", 100, 6)
        # 6-year holding multiplier (1.60) > 1-year (1.0)
        assert central6 > central1

    def test_sensitivity_range_used(self):
        # municipal_usufruct_land has higher central sensitivity (0.95) vs industrial (0.70)
        _, central_muni, _ = compute_developer_irr_adjustment("municipal_usufruct_land", 100, None)
        _, central_ind, _ = compute_developer_irr_adjustment("industrial_land", 100, None)
        assert central_muni > central_ind

    def test_all_land_types_work(self):
        for land_type in LAND_SENSITIVITY_RANGE:
            low, central, high = compute_developer_irr_adjustment(land_type, 50, 2)
            assert low > 0
            assert high >= central >= low


# ---------------------------------------------------------------------------
# compute_opportunity_cost_adjustment
# ---------------------------------------------------------------------------

class TestComputeOpportunityCostAdjustment:
    def test_returns_tuple_of_three(self):
        result = compute_opportunity_cost_adjustment(100, "industrial_land")
        assert len(result) == 3

    def test_low_le_central_le_high(self):
        low, central, high = compute_opportunity_cost_adjustment(100, "raw_land_inside_urban_boundary")
        assert low <= central <= high

    def test_special_purpose_uses_special_range(self):
        low, _, high = compute_opportunity_cost_adjustment(100, "special_purpose_land")
        assert abs(low - 60.0) < 1e-9
        assert abs(high - 95.0) < 1e-9

    def test_municipal_usufruct_uses_special_range(self):
        low, _, high = compute_opportunity_cost_adjustment(100, "municipal_usufruct_land")
        assert abs(low - 60.0) < 1e-9
        assert abs(high - 95.0) < 1e-9

    def test_development_land_uses_dev_range(self):
        low, _, high = compute_opportunity_cost_adjustment(100, "residential_development_land")
        assert abs(low - 65.0) < 1e-9
        assert abs(high - 90.0) < 1e-9

    def test_raw_land_uses_default_range(self):
        low, _, high = compute_opportunity_cost_adjustment(100, "raw_land_outside_urban_boundary")
        assert abs(low - 55.0) < 1e-9
        assert abs(high - 85.0) < 1e-9

    def test_scales_with_shock(self):
        _, central_100, _ = compute_opportunity_cost_adjustment(100, "industrial_land")
        _, central_200, _ = compute_opportunity_cost_adjustment(200, "industrial_land")
        assert abs(central_200 - 2 * central_100) < 1e-9


# ---------------------------------------------------------------------------
# compute_holding_risk_adjustment
# ---------------------------------------------------------------------------

class TestComputeHoldingRiskAdjustment:
    def test_returns_tuple_of_three(self):
        result = compute_holding_risk_adjustment(3, 100)
        assert len(result) == 3

    def test_low_le_central_le_high(self):
        low, central, high = compute_holding_risk_adjustment(4, 100)
        assert low <= central <= high

    def test_none_holding_uses_lowest_mult(self):
        low, central, high = compute_holding_risk_adjustment(None, 100)
        # mult=0.2 → central = 100*0.2 = 20
        assert abs(central - 20.0) < 1e-9

    def test_one_year_holding_uses_lowest_mult(self):
        _, central, _ = compute_holding_risk_adjustment(1, 100)
        assert abs(central - 20.0) < 1e-9

    def test_two_year_uses_0_4(self):
        _, central, _ = compute_holding_risk_adjustment(2, 100)
        assert abs(central - 40.0) < 1e-9

    def test_four_year_uses_0_6(self):
        _, central, _ = compute_holding_risk_adjustment(4, 100)
        assert abs(central - 60.0) < 1e-9

    def test_six_year_uses_0_8(self):
        _, central, _ = compute_holding_risk_adjustment(6, 100)
        assert abs(central - 80.0) < 1e-9

    def test_low_is_80_pct_of_central(self):
        low, central, _ = compute_holding_risk_adjustment(3, 100)
        assert abs(low - central * 0.8) < 1e-9

    def test_high_is_120_pct_of_central(self):
        _, central, high = compute_holding_risk_adjustment(3, 100)
        assert abs(high - central * 1.2) < 1e-9


# ---------------------------------------------------------------------------
# compute_final_pressure
# ---------------------------------------------------------------------------

class TestComputeFinalPressure:
    def test_zero_shock_produces_zero_financial_pressure(self):
        result = compute_final_pressure(
            hbu_haircut=0.0,
            white_land_pressure=0.0,
            irr_adj_central=0.0,
            opp_cost_central=0.0,
            holding_risk_central=0.0,
            repo_shock_bps=0.0,
        )
        assert result == 0.0

    def test_result_bounded_between_0_and_1(self):
        result = compute_final_pressure(
            hbu_haircut=0.30,
            white_land_pressure=0.50,
            irr_adj_central=500.0,
            opp_cost_central=500.0,
            holding_risk_central=500.0,
            repo_shock_bps=500.0,
        )
        assert 0.0 <= result <= 1.0

    def test_higher_shock_increases_pressure(self):
        low = compute_final_pressure(0.0, 0.0, 50.0, 50.0, 20.0, repo_shock_bps=50)
        high = compute_final_pressure(0.0, 0.0, 200.0, 200.0, 80.0, repo_shock_bps=200)
        assert high >= low

    def test_hbu_haircut_adds_to_pressure(self):
        base = compute_final_pressure(0.0, 0.0, 100.0, 75.0, 40.0, repo_shock_bps=100)
        with_hbu = compute_final_pressure(0.30, 0.0, 100.0, 75.0, 40.0, repo_shock_bps=100)
        assert with_hbu > base

    def test_white_land_tax_adds_to_pressure(self):
        base = compute_final_pressure(0.0, 0.0, 100.0, 75.0, 40.0, repo_shock_bps=100)
        with_tax = compute_final_pressure(0.0, 0.30, 100.0, 75.0, 40.0, repo_shock_bps=100)
        assert with_tax > base


# ---------------------------------------------------------------------------
# LandImpactMapper.analyze — integration tests
# ---------------------------------------------------------------------------

class TestLandImpactMapperAnalyze:
    def _minimal_input(self, **overrides):
        defaults = dict(
            land_type="industrial_land",
            valuation_method="residual",
            repo_shock_bps=100.0,
        )
        defaults.update(overrides)
        return LandImpactInput(**defaults)

    def test_invalid_land_type_raises(self):
        inp = self._minimal_input(land_type="fantasy_land")
        with pytest.raises(ValueError, match="Unknown land_type"):
            LandImpactMapper.analyze(inp)

    def test_all_valid_land_types_succeed(self):
        for lt in LAND_SENSITIVITY_RANGE:
            inp = self._minimal_input(land_type=lt)
            result = LandImpactMapper.analyze(inp)
            assert 0.0 <= result.final_land_value_pressure_score <= 1.0

    def test_confidence_high_when_evidence_high_and_margin_given(self):
        inp = self._minimal_input(
            evidence_quality="HIGH",
            base_feasibility_margin_pct=0.15,
        )
        result = LandImpactMapper.analyze(inp)
        assert result.confidence_level == "HIGH"

    def test_confidence_medium_when_evidence_high_no_margin(self):
        inp = self._minimal_input(evidence_quality="HIGH")
        result = LandImpactMapper.analyze(inp)
        assert result.confidence_level == "MEDIUM"

    def test_confidence_medium_when_evidence_medium_margin_given(self):
        inp = self._minimal_input(
            evidence_quality="MEDIUM",
            base_feasibility_margin_pct=0.10,
        )
        result = LandImpactMapper.analyze(inp)
        assert result.confidence_level == "MEDIUM"

    def test_confidence_low_when_evidence_low_no_margin(self):
        inp = self._minimal_input(evidence_quality="LOW")
        result = LandImpactMapper.analyze(inp)
        assert result.confidence_level == "LOW"

    def test_uncertainty_band_low_le_high(self):
        inp = self._minimal_input(base_feasibility_margin_pct=0.12, holding_period_years=3)
        result = LandImpactMapper.analyze(inp)
        assert result.uncertainty_band_low <= result.uncertainty_band_high

    def test_uncertainty_band_within_0_1(self):
        inp = self._minimal_input(base_feasibility_margin_pct=0.05, holding_period_years=7)
        result = LandImpactMapper.analyze(inp)
        assert 0.0 <= result.uncertainty_band_low <= 1.0
        assert 0.0 <= result.uncertainty_band_high <= 1.0

    def test_hbu_unknown_when_no_margin(self):
        inp = self._minimal_input()
        result = LandImpactMapper.analyze(inp)
        assert result.hbu_risk_flag == "UNKNOWN_REQUIRES_FEASIBILITY_TEST"
        assert result.hbu_haircut_pct == 0.0

    def test_white_land_tax_zero_when_outside_scope(self):
        inp = self._minimal_input(
            is_inside_white_land_tax_scope=False,
            white_land_tax_rate_pct=0.025,
            holding_period_years=3,
        )
        result = LandImpactMapper.analyze(inp)
        assert result.white_land_tax_pressure_pct == 0.0

    def test_white_land_tax_positive_when_inside_scope(self):
        inp = self._minimal_input(
            is_inside_white_land_tax_scope=True,
            white_land_tax_rate_pct=0.025,
            holding_period_years=3,
        )
        result = LandImpactMapper.analyze(inp)
        assert result.white_land_tax_pressure_pct > 0.0

    def test_governance_notes_mention_land_type(self):
        inp = self._minimal_input(land_type="commercial_development_land")
        result = LandImpactMapper.analyze(inp)
        assert "commercial_development_land" in result.governance_notes

    def test_governance_notes_mention_no_cap_rate(self):
        inp = self._minimal_input()
        result = LandImpactMapper.analyze(inp)
        assert "Cap Rate" in result.governance_notes

    def test_governance_notes_mention_shock_magnitude(self):
        inp = self._minimal_input(repo_shock_bps=75)
        result = LandImpactMapper.analyze(inp)
        assert "75" in result.governance_notes

    def test_governance_notes_warn_missing_margin(self):
        inp = self._minimal_input()
        result = LandImpactMapper.analyze(inp)
        assert "UNKNOWN" in result.governance_notes

    def test_governance_notes_include_margin_when_provided(self):
        inp = self._minimal_input(base_feasibility_margin_pct=0.18)
        result = LandImpactMapper.analyze(inp)
        assert "18.0%" in result.governance_notes

    def test_governance_notes_mention_white_land_tax_when_applicable(self):
        inp = self._minimal_input(
            is_inside_white_land_tax_scope=True,
            white_land_tax_rate_pct=0.025,
        )
        result = LandImpactMapper.analyze(inp)
        assert "compounding" in result.governance_notes

    def test_higher_shock_generally_higher_pressure(self):
        inp_low = self._minimal_input(repo_shock_bps=25, base_feasibility_margin_pct=0.20)
        inp_high = self._minimal_input(repo_shock_bps=200, base_feasibility_margin_pct=0.20)
        r_low = LandImpactMapper.analyze(inp_low)
        r_high = LandImpactMapper.analyze(inp_high)
        assert r_high.final_land_value_pressure_score >= r_low.final_land_value_pressure_score

    def test_longer_holding_amplifies_irr_adjustment(self):
        inp_short = self._minimal_input(holding_period_years=1)
        inp_long = self._minimal_input(holding_period_years=10)
        r_short = LandImpactMapper.analyze(inp_short)
        r_long = LandImpactMapper.analyze(inp_long)
        assert r_long.developer_irr_adjustment_bps > r_short.developer_irr_adjustment_bps

    def test_municipal_usufruct_higher_irr_than_industrial(self):
        inp_muni = self._minimal_input(land_type="municipal_usufruct_land")
        inp_ind = self._minimal_input(land_type="industrial_land")
        r_muni = LandImpactMapper.analyze(inp_muni)
        r_ind = LandImpactMapper.analyze(inp_ind)
        assert r_muni.developer_irr_adjustment_bps > r_ind.developer_irr_adjustment_bps

    def test_final_pressure_is_float_in_range(self):
        inp = self._minimal_input(
            base_feasibility_margin_pct=0.10,
            holding_period_years=4,
            is_inside_white_land_tax_scope=True,
            white_land_tax_rate_pct=0.025,
            evidence_quality="MEDIUM",
        )
        result = LandImpactMapper.analyze(inp)
        assert isinstance(result.final_land_value_pressure_score, float)
        assert 0.0 <= result.final_land_value_pressure_score <= 1.0
