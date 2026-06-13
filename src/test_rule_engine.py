from rule_engine import calculate_rule_score

sample_email = """
URGENT!

Your account has been suspended.

Click now:

http://192.168.1.1/login

Download invoice.exe

Verify immediately.
"""

score, indicators = calculate_rule_score(
    sample_email
)

print("Rule Score:", score)

print("\nIndicators:")

for item in indicators:
    print("-", item)