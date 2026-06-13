import re
from urllib.parse import urlparse


URGENT_WORDS = [
    "urgent",
    "verify",
    "password",
    "click now",
    "immediately",
    "account suspended",
    "account locked",
    "update account",
    "login now"
]

SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "t.co"
]

SUSPICIOUS_EXTENSIONS = [
    ".exe",
    ".bat",
    ".js",
    ".scr",
    ".docm"
]


def calculate_rule_score(email_text):

    score = 0
    indicators = []

    text = email_text.lower()

    # --------------------------------
    # Urgent Keywords
    # --------------------------------

    for word in URGENT_WORDS:
        if word in text:
            score += 10
            indicators.append(
                f"Urgent keyword detected: {word}"
            )
            break

    # --------------------------------
    # URLs
    # --------------------------------

    urls = re.findall(
        r'https?://\S+',
        email_text
    )

    if len(urls) > 3:
        score += 10
        indicators.append(
            "More than 3 URLs detected"
        )

    for url in urls:

        parsed = urlparse(url)

        domain = parsed.netloc

        if any(
            short in domain
            for short in SHORTENERS
        ):
            score += 10
            indicators.append(
                f"Shortened URL detected: {domain}"
            )

        ip_pattern = r"\d+\.\d+\.\d+\.\d+"

        if re.search(ip_pattern, domain):
            score += 15
            indicators.append(
                f"IP URL detected: {domain}"
            )

    # --------------------------------
    # Capital Letters
    # --------------------------------

    capital_count = sum(
        1 for c in email_text
        if c.isupper()
    )

    if capital_count > 30:
        score += 5
        indicators.append(
            "Excessive capitalization"
        )

    # --------------------------------
    # Attachments Mention
    # --------------------------------

    for ext in SUSPICIOUS_EXTENSIONS:
        if ext in text:
            score += 20
            indicators.append(
                f"Suspicious attachment: {ext}"
            )

    score = min(score, 100)

    return score, indicators