# AI Medical Report Extraction Self-Checker

## 1. What this project does

This is a small reliability loop for one narrow task: extracting selected laboratory values from a medical-report text.

The first pass creates a structured extraction. A second, independent checking pass compares every extracted value with the source report. If a value is wrong, it is corrected from the source; if the source does not support a drafted field, it is flagged.

**Failure type targeted:** fabricated or incorrect extracted facts.

> This is a technical demonstration, not a medical diagnostic or clinical decision-support tool.

## 2. Why this failure matters

A plausible-looking numeric value can be dangerous if it is silently copied into a structured record. The demo therefore focuses on a concrete, observable failure: a confident wrong lab value.

## 3. Architecture

```text
Report text
   |
   v
First-pass extraction
   |
   v
Draft JSON
   |
   v
Independent source verification
   |
   +---- match ----> accept
   |
   +---- mismatch -> correct from source
   |
   +---- unsupported -> flag
   |
   v
Final JSON + check report
```

## 4. Required confident-error demonstration

Source report:

- Hemoglobin: 10.2 g/dL
- Glucose: 96 mg/dL
- Total Cholesterol: 185 mg/dL
- Creatinine: 0.9 mg/dL

First-pass draft is intentionally made confidently wrong for the demo:

```json
{"total_cholesterol": "285 mg/dL"}
```

The checker compares it with the source, detects the mismatch, and returns:

```text
Before: 285 mg/dL
After:  185 mg/dL
Reason: Extracted value does not match the source document.
```

This is the key before/after evidence for the assignment.

## 5. Run locally

### Windows / macOS / Linux

```bash
python -m venv .venv
```

Activate it:

Windows PowerShell:
```bash
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Start UI:
```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## 6. Run tests

```bash
pytest -q
```

The five tests cover clean extraction, a confident plausible wrong answer, another numeric mismatch, a missed field, and an unsupported field.

## 7. Files

- `app.py` — Streamlit UI
- `extractor.py` — first-pass extraction
- `checker.py` — second-pass verification and correction
- `tests/` — five test cases
- `results/` — recorded test results and before/after evidence
- `docs/` — write-up

## 8. Limitations

The demonstration uses deterministic local extraction/checking rules so the reliability behavior is reproducible. It does not claim clinical accuracy, OCR robustness, medical interpretation, or suitability for real patient data. A production system would need validated document parsing, model/version controls, privacy/security controls, audit logs, human review, and clinical validation.

## 9. What I learned

The important lesson is that a fluent first answer is not evidence that the answer is correct. The second pass needs a concrete verification target. Here, the target is simple: every extracted numeric value must be supported by the source text. The loop also makes failure visible instead of silently returning the first answer.
