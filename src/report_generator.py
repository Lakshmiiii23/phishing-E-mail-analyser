import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY must be set in the environment")
genai.configure(
    api_key=api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_report(
    email_text,
    ml_score,
    rule_score,
    risk_level,
    indicators,
    retrieved_context
):

    prompt = f"""
You are a professional cybersecurity analyst.

Analyze the phishing email.

EMAIL CONTENT:
{email_text}

ML SCORE:
{ml_score}

RULE SCORE:
{rule_score}

RISK LEVEL:
{risk_level}

INDICATORS:
{indicators}

RETRIEVED CYBERSECURITY KNOWLEDGE:
{retrieved_context}

Generate:

1. Threat Summary

2. Risk Explanation

3. Indicators Found

4. Mitigation Recommendations

5. Security Awareness Tips

Keep response professional.
"""

    response = model.generate_content(
        prompt
    )

    return response.text


if __name__ == "__main__":

    report = generate_report(
        email_text="""
URGENT

Verify your account immediately.

Click here now.

http://192.168.1.1/login
""",
        ml_score=92,
        rule_score=45,
        risk_level="Critical",
        indicators=[
            "Urgent keyword",
            "IP URL"
        ],
        retrieved_context=[
            "Phishing emails often use urgency.",
            "IP URLs are common phishing indicators."
        ]
    )

    print(report)