import re
from extractor import FIELD_PATTERNS, UNITS

def _source_values(report: str) -> dict:
    source = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, report)
        if match:
            source[field] = f"{match.group(1)} {UNITS[field]}"
    return source

def _normalize(value: str) -> str:
    return value.strip().lower().replace(" ", "")

def self_check(report: str, draft: dict) -> dict:
    source = _source_values(report)
    checks = []
    final_result = {}
    issues = 0
    corrected = 0

    fields = sorted(set(source) | set(draft))
    for field in fields:
        draft_value = draft.get(field)
        source_value = source.get(field)

        if source_value is None:
            checks.append({
                "field": field,
                "status": "FLAG",
                "draft_value": draft_value,
                "source_value": None,
                "reason": "The draft contains a field that could not be verified in the source."
            })
            issues += 1
            continue

        if draft_value is None:
            checks.append({
                "field": field,
                "status": "FLAG",
                "draft_value": None,
                "source_value": source_value,
                "reason": "The source contains a value that the draft missed."
            })
            final_result[field] = source_value
            issues += 1
            corrected += 1
            continue

        if _normalize(draft_value) == _normalize(source_value):
            checks.append({
                "field": field,
                "status": "MATCH",
                "draft_value": draft_value,
                "source_value": source_value,
                "reason": "Draft matches source."
            })
            final_result[field] = draft_value
        else:
            checks.append({
                "field": field,
                "status": "MISMATCH",
                "draft_value": draft_value,
                "source_value": source_value,
                "reason": "Extracted value does not match the source document."
            })
            final_result[field] = source_value
            issues += 1
            corrected += 1

    status = "PASS" if issues == 0 else "CORRECTED/FLAGGED"
    return {
        "final_result": final_result,
        "checks": checks,
        "self_check": {
            "status": status,
            "fields_checked": len(fields),
            "issues_found": issues,
            "corrected_fields": corrected,
            "failure_type": "fabricated_or_incorrect extracted fact",
        }
    }
