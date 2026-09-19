from extractor import extract_report
from checker import self_check

REPORT = """Hemoglobin: 10.2 g/dL
Glucose: 96 mg/dL
Total Cholesterol: 185 mg/dL
Creatinine: 0.9 mg/dL
"""

def test_1_clean_extraction_passes():
    draft = extract_report(REPORT)
    result = self_check(REPORT, draft)
    assert result["self_check"]["status"] == "PASS"
    assert result["self_check"]["issues_found"] == 0

def test_2_confident_plausible_cholesterol_error_is_caught():
    draft = extract_report(REPORT, force_demo_error=True)
    result = self_check(REPORT, draft)
    assert draft["total_cholesterol"] == "285 mg/dL"
    assert result["final_result"]["total_cholesterol"] == "185 mg/dL"
    assert result["self_check"]["issues_found"] == 1

def test_3_wrong_hemoglobin_is_caught():
    draft = extract_report(REPORT)
    draft["hemoglobin"] = "11.2 g/dL"
    result = self_check(REPORT, draft)
    assert result["final_result"]["hemoglobin"] == "10.2 g/dL"
    assert result["self_check"]["issues_found"] == 1

def test_4_missing_source_value_is_flagged():
    report = """Hemoglobin: 10.2 g/dL
Glucose: 96 mg/dL
"""
    draft = {"hemoglobin": "10.2 g/dL", "glucose": "96 mg/dL", "creatinine": "0.9 mg/dL"}
    result = self_check(report, draft)
    item = next(x for x in result["checks"] if x["field"] == "creatinine")
    assert item["status"] == "FLAG"

def test_5_missed_extraction_is_corrected_from_source():
    draft = extract_report(REPORT)
    draft.pop("glucose")
    result = self_check(REPORT, draft)
    assert result["final_result"]["glucose"] == "96 mg/dL"
    assert result["self_check"]["issues_found"] == 1
