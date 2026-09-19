import re

FIELD_PATTERNS = {
    "hemoglobin": r"(?i)\b(?:hemoglobin|hb)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)\s*(g/dL)?",
    "glucose": r"(?i)\b(?:glucose|blood sugar)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)\s*(mg/dL)?",
    "total_cholesterol": r"(?i)\b(?:total cholesterol|cholesterol)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)\s*(mg/dL)?",
    "creatinine": r"(?i)\bcreatinine\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)\s*(mg/dL)?",
}

UNITS = {
    "hemoglobin": "g/dL",
    "glucose": "mg/dL",
    "total_cholesterol": "mg/dL",
    "creatinine": "mg/dL",
}

def extract_report(report: str, force_demo_error: bool = False) -> dict:
    result = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, report)
        if match:
            value = match.group(1)
            result[field] = f"{value} {UNITS[field]}"
    # Simulates the assignment's required confident first-pass failure.
    # The source still contains 185 mg/dL, but the draft confidently says 285 mg/dL.
    if force_demo_error and "total_cholesterol" in result:
        result["total_cholesterol"] = "285 mg/dL"
    return result
