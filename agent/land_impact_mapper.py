"""
Land Impact Mapper - independent module for land valuation under repo shocks.
Not using Cap Rate passthrough logic.

This module handles the transmission of interest rate shocks (Repo/SAIBOR)
to land values through:
- Developer IRR expectations
- Opportunity cost of capital
- Holding period risk
- Highest & Best Use (HBU) viability
- White land tax compounding pressure

All land types are explicitly enumerated. No Cap Rate passthrough is used.
"""

from dataclasses import dataclass
from typing import Optional, Literal, Dict, Tuple

# ============================================================================
# Land Type Enumeration (Literal)
# ============================================================================

LandType = Literal[
    "raw_land_inside_urban_boundary",
    "raw_land_outside_urban_boundary",
    "approved_subdivision_land",
    "residential_development_land",
    "commercial_development_land",
    "industrial_land",
    "special_purpose_land",
    "municipal_usufruct_land",
]

# ============================================================================
# Input and Output Dataclasses
# ============================================================================

@dataclass
class LandImpactInput:
    """
    Inputs for land impact analysis under a repo rate shock.
    """
    land_type: LandType
    valuation_method: Literal["residual", "extraction", "comparables", "cost", "direct_capitalization"]
    repo_shock_bps: float               # positive = repo increase (e.g., +50 = +0.50%)
    base_feasibility_margin_pct: Optional[float] = None   # developer margin before shock, e.g., 0.15 = 15%
    holding_period_years: Optional[float] = None          # expected years to sell/develop
    white_land_tax_rate_pct: Optional[float] = None       # annual tax rate, e.g., 0.025 = 2.5%
    is_inside_white_land_tax_scope: bool = False
    evidence_quality: Literal["HIGH", "MEDIUM", "LOW"] = "MEDIUM"
    notes: Optional[str] = None


@dataclass
class LandImpactResult:
    """
    Results of applying a repo shock to a land asset.
    All adjustments are expressed as downward pressure on land value.
    """
    developer_irr_adjustment_bps: float          # reduction in expected developer IRR (bps)
    opportunity_cost_adjustment_bps: float       # increase in required return (bps)
    holding_risk_adjustment_bps: float           # additional risk premium (bps)
    hbu_risk_flag: str                           # HIGH / MODERATE / LOW / UNKNOWN_REQUIRES_FEASIBILITY_TEST
    hbu_haircut_pct: float                       # value reduction due to HBU risk (0..1)
    white_land_tax_pressure_pct: float           # annualised holding cost from white land tax (0..1)
    uncertainty_band_low: float                  # lower bound of total value pressure (0..1)
    uncertainty_band_high: float                 # upper bound of total value pressure (0..1)
    final_land_value_pressure_score: float       # composite pressure (0 = no impact, 1 = extreme)
    confidence_level: Literal["HIGH", "MEDIUM", "LOW"]
    governance_notes: str


# ============================================================================
# Sensitivity ranges per land type (low, central, high)
# These represent the passthrough of a 100 bps repo shock into land value pressure.
# Central values are engineered judgment based on lease structure analogies and
# market behaviour in GCC.
# ============================================================================

LAND_SENSITIVITY_RANGE: Dict[LandType, Tuple[float, float, float]] = {
    "raw_land_inside_urban_boundary":      (0.60, 0.80, 1.00),
    "raw_land_outside_urban_boundary":     (0.50, 0.70, 0.90),
    "approved_subdivision_land":           (0.55, 0.75, 0.95),
    "residential_development_land":        (0.55, 0.70, 0.90),   # lower central than municipal
    "commercial_development_land":         (0.65, 0.80, 1.00),
    "industrial_land":                     (0.50, 0.70, 0.95),
    "special_purpose_land":                (0.40, 0.75, 1.20),    # wider uncertainty
    "municipal_usufruct_land":             (0.60, 0.95, 1.30),    # higher sensitivity
}


# ============================================================================
# Helper functions
# ============================================================================

def holding_period_multiplier(holding_years: Optional[float]) -> float:
    """Longer holding periods amplify sensitivity to repo shocks."""
    if holding_years is None or holding_years <= 1:
        return 1.0
    elif holding_years <= 3:
        return 1.15
    elif holding_years <= 5:
        return 1.35
    else:
        return 1.60


def compute_white_land_pressure(tax_rate_pct: Optional[float],
                                is_inside_scope: bool,
                                holding_years: Optional[float]) -> float:
    """
    White land tax creates a compounding holding cost that erodes land value.
    This pressure is independent of repo shock magnitude (tax does not change
    with interest rates). However, it interacts with opportunity cost.
    Returns the total erosion as a fraction of land value over the holding period.
    """
    if not is_inside_scope or tax_rate_pct is None or tax_rate_pct <= 0:
        return 0.0
    years = holding_years if holding_years is not None and holding_years > 0 else 1.0
    # Compounded erosion: (1 + tax)^years - 1
    compounded = (1 + tax_rate_pct) ** years - 1
    return min(compounded, 0.50)   # cap at 50%


def assess_hbu_risk(land_type: LandType,
                    repo_shock_bps: float,
                    base_margin_pct: Optional[float]) -> Tuple[str, float]:
    """
    Determines whether the Highest & Best Use becomes unviable after a repo shock.
    Returns (risk_flag, haircut_pct) where haircut is additional value reduction.
    """
    if base_margin_pct is None:
        return ("UNKNOWN_REQUIRES_FEASIBILITY_TEST", 0.0)

    # Each 100 bps repo shock erodes developer margin by ~25 bps (0.25%)
    margin_erosion_bps = repo_shock_bps * 0.25
    margin_erosion_pct = margin_erosion_bps / 100.0
    remaining_margin = base_margin_pct - margin_erosion_pct

    if remaining_margin <= 0.02:       # <= 2% → HBU at risk
        return ("HIGH", 0.30)
    elif remaining_margin <= 0.05:     # 2%-5% → moderate risk
        return ("MODERATE", 0.15)
    else:
        return ("LOW", 0.05)


def compute_developer_irr_adjustment(land_type: LandType,
                                     repo_shock_bps: float,
                                     holding_years: Optional[float]) -> Tuple[float, float, float]:
    """
    Returns (low, central, high) downward adjustment in developer IRR expectations (bps).
    """
    sens_low, sens_central, sens_high = LAND_SENSITIVITY_RANGE[land_type]
    hold_mult = holding_period_multiplier(holding_years)

    adj_low = repo_shock_bps * sens_low * hold_mult
    adj_central = repo_shock_bps * sens_central * hold_mult
    adj_high = repo_shock_bps * sens_high * hold_mult
    return (adj_low, adj_central, adj_high)


def compute_opportunity_cost_adjustment(repo_shock_bps: float,
                                        land_type: LandType) -> Tuple[float, float, float]:
    """
    Higher repo rates increase the required return (opportunity cost) for holding land.
    Returns (low, central, high) adjustment in bps.
    """
    if land_type in ("special_purpose_land", "municipal_usufruct_land"):
        low, high = 0.60, 0.95
    elif "development" in land_type:
        low, high = 0.65, 0.90
    else:
        low, high = 0.55, 0.85
    central = (low + high) / 2
    return (repo_shock_bps * low, repo_shock_bps * central, repo_shock_bps * high)


def compute_holding_risk_adjustment(holding_years: Optional[float],
                                    repo_shock_bps: float) -> Tuple[float, float, float]:
    """
    Longer holding periods increase the uncertainty and cost of carry.
    Returns (low, central, high) adjustment in bps.
    """
    if holding_years is None or holding_years <= 1:
        mult = 0.2
    elif holding_years <= 3:
        mult = 0.4
    elif holding_years <= 5:
        mult = 0.6
    else:
        mult = 0.8

    low = repo_shock_bps * mult * 0.8
    central = repo_shock_bps * mult
    high = repo_shock_bps * mult * 1.2
    return (low, central, high)


def compute_final_pressure(hbu_haircut: float,
                           white_land_pressure: float,
                           irr_adj_central: float,
                           opp_cost_central: float,
                           holding_risk_central: float,
                           repo_shock_bps: float) -> float:
    """
    Combines all pressures into a single score between 0 and 1.
    Methodology: weighted sum of normalised effects.
    """
    severe_shock = 200.0   # 200 bps = 2% repo increase considered severe
    norm_repo = min(repo_shock_bps / severe_shock, 1.0)

    # Financial pressure from IRR, opportunity cost and holding risk:
    # each 100 bps adjustment translates roughly to 0.1 pressure.
    financial_pressure = (irr_adj_central + opp_cost_central + holding_risk_central) / 100.0 / 3.0
    financial_pressure = min(financial_pressure * norm_repo, 0.4)

    # HBU haircut adds directly (max 0.3)
    hbu_pressure = min(hbu_haircut, 0.3)

    # White land tax pressure (already a fraction, cap at 0.3)
    tax_pressure = min(white_land_pressure, 0.3)

    total = financial_pressure + hbu_pressure + tax_pressure
    return min(total, 1.0)


# ============================================================================
# Main Mapper Class
# ============================================================================

class LandImpactMapper:
    """
    Analyzes the impact of a repo rate shock on land assets.
    Completely independent of income-producing property logic (no Cap Rate passthrough).
    """

    @staticmethod
    def analyze(inputs: LandImpactInput) -> LandImpactResult:
        """Main entry point for land impact analysis."""

        # Guard against unrecognised land types
        if inputs.land_type not in LAND_SENSITIVITY_RANGE:
            raise ValueError(f"Unknown land_type: {inputs.land_type}. "
                             f"Valid types: {list(LAND_SENSITIVITY_RANGE.keys())}")

        # 1. Developer IRR adjustment (range)
        irr_low, irr_central, irr_high = compute_developer_irr_adjustment(
            inputs.land_type, inputs.repo_shock_bps, inputs.holding_period_years
        )

        # 2. Opportunity cost adjustment
        opp_low, opp_central, opp_high = compute_opportunity_cost_adjustment(
            inputs.repo_shock_bps, inputs.land_type
        )

        # 3. Holding risk adjustment
        hold_low, hold_central, hold_high = compute_holding_risk_adjustment(
            inputs.holding_period_years, inputs.repo_shock_bps
        )

        # 4. HBU risk
        hbu_flag, hbu_haircut = assess_hbu_risk(
            inputs.land_type, inputs.repo_shock_bps, inputs.base_feasibility_margin_pct
        )

        # 5. White land tax pressure (independent of repo shock)
        white_tax_pressure = compute_white_land_pressure(
            inputs.white_land_tax_rate_pct,
            inputs.is_inside_white_land_tax_scope,
            inputs.holding_period_years
        )

        # 6. Final pressure score
        final_pressure = compute_final_pressure(
            hbu_haircut=hbu_haircut,
            white_land_pressure=white_tax_pressure,
            irr_adj_central=irr_central,
            opp_cost_central=opp_central,
            holding_risk_central=hold_central,
            repo_shock_bps=inputs.repo_shock_bps,
        )

        # 7. Confidence level
        if inputs.evidence_quality == "HIGH" and inputs.base_feasibility_margin_pct is not None:
            confidence = "HIGH"
        elif inputs.evidence_quality == "HIGH" or inputs.base_feasibility_margin_pct is not None:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        # 8. Uncertainty bands (combine low/high from components)
        total_low = (irr_low + opp_low + hold_low) / 100.0 + hbu_haircut + white_tax_pressure - 0.05
        total_high = (irr_high + opp_high + hold_high) / 100.0 + hbu_haircut + white_tax_pressure + 0.05
        total_low = max(0.0, min(total_low, 1.0))
        total_high = max(0.0, min(total_high, 1.0))
        if total_low > total_high:
            total_low, total_high = total_high, total_low

        # 9. Governance notes – explicitly explain that Cap Rate is NOT used
        governance_notes = (
            f"Land type '{inputs.land_type}' analyzed WITHOUT Cap Rate passthrough. "
            "Impact transmitted via developer IRR, opportunity cost, holding risk, "
            "HBU viability, and white land tax (independent of repo). "
            f"Repo shock: +{inputs.repo_shock_bps} bps. "
        )
        if inputs.base_feasibility_margin_pct is None:
            governance_notes += "Base feasibility margin missing → HBU risk is UNKNOWN. Recommend feasibility study."
        else:
            governance_notes += f"Base margin: {inputs.base_feasibility_margin_pct:.1%}. "
        if inputs.is_inside_white_land_tax_scope:
            governance_notes += f"White land tax applied at {inputs.white_land_tax_rate_pct:.1%} annual, compounding."
        else:
            governance_notes += "White land tax not applicable."

        return LandImpactResult(
            developer_irr_adjustment_bps=irr_central,
            opportunity_cost_adjustment_bps=opp_central,
            holding_risk_adjustment_bps=hold_central,
            hbu_risk_flag=hbu_flag,
            hbu_haircut_pct=hbu_haircut,
            white_land_tax_pressure_pct=white_tax_pressure,
            uncertainty_band_low=total_low,
            uncertainty_band_high=total_high,
            final_land_value_pressure_score=final_pressure,
            confidence_level=confidence,
            governance_notes=governance_notes,
        )
