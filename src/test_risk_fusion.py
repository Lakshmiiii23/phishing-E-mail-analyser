from risk_fusion import calculate_final_risk

result = calculate_final_risk(
    ml_probability=0.92,
    rule_score=45
)

print(result)