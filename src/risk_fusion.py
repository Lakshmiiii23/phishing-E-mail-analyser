def calculate_final_risk(
    ml_probability,
    rule_score
):
    """
    ml_probability:
        0 to 1

    rule_score:
        0 to 100
    """

    ml_score = ml_probability * 100

    final_score = (
        0.7 * ml_score
        +
        0.3 * rule_score
    )

    final_score = round(final_score, 2)

    if final_score < 25:
        risk_level = "Low"

    elif final_score < 50:
        risk_level = "Medium"

    elif final_score < 75:
        risk_level = "High"

    else:
        risk_level = "Critical"

    return {
        "ml_score": round(ml_score, 2),
        "rule_score": rule_score,
        "final_score": final_score,
        "risk_level": risk_level
    }