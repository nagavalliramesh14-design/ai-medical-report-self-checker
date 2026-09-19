# Applied AI Engineering Intern — Self-Check Loop Write-up

## Project
**AI Medical Report Extraction Self-Checker**

## 1. Problem selected

I chose one narrow task: extracting a small set of laboratory values from a medical-report text.

The failure I chose to catch is **fabricated or incorrect extracted facts**, specifically a numeric lab value that is plausible but does not match the source report.

I selected this failure because a structured extraction can look trustworthy even when one number is wrong. A checker can verify the exact source evidence instead of relying on the fluency of the first answer.

## 2. System design

The project has two passes.

### Pass 1 — Draft

The first pass extracts:

- Hemoglobin
- Glucose
- Total Cholesterol
- Creatinine

It returns structured JSON.

### Pass 2 — Self-check

The second pass independently obtains the values supported by the source report and compares them with the draft.

Three outcomes are possible:

1. **MATCH** — accept the drafted value.
2. **MISMATCH** — replace it with the source-supported value.
3. **FLAG** — do not silently accept a field that cannot be supported by the source.

## 3. Confidently wrong example

Source:

```text
Total Cholesterol: 185 mg/dL
```

First draft:

```text
Total Cholesterol: 285 mg/dL
```

The wrong value is intentionally plausible. It is not an obviously impossible value.

The checker detects:

```text
Before: 285 mg/dL
After:  185 mg/dL
Finding: Extracted value does not match the source document.
```

This demonstrates the complete reliability loop:

**draft → mistake → independent check → correction → structured final result**

## 4. Test cases

### Test 1 — Correct extraction

All four values in the draft match the source.

Expected: no issues.

### Test 2 — Confident plausible wrong cholesterol

Source: 185 mg/dL.

Draft: 285 mg/dL.

Expected: mismatch and correction to 185 mg/dL.

### Test 3 — Wrong hemoglobin

Source: 10.2 g/dL.

Draft: 11.2 g/dL.

Expected: mismatch and correction to 10.2 g/dL.

### Test 4 — Unsupported field

The draft contains creatinine even though the source does not contain a creatinine result.

Expected: flag the field rather than accepting it.

### Test 5 — Missed source field

The draft omits glucose even though the source contains 96 mg/dL.

Expected: flag/correct the missing field using the source.

## 5. Results

The test suite contains five tests. The expected local run is:

```text
5 passed
```

Tests 2–5 deliberately exercise failure handling. Test 1 demonstrates the non-error path.

## 6. Where the model/system failed

The important failure is that a first-pass system can produce a plausible number that is not grounded in the source. If the application simply returned the first result, the incorrect cholesterol value could reach the user.

The project therefore treats the first pass as untrusted and adds a source-grounded verification step.

## 7. What I did about the failure

I made the second pass check a concrete property rather than asking another generic question such as "Is this answer correct?"

The checker:

- extracts source-supported values,
- compares each draft value,
- identifies mismatches,
- replaces mismatched values with source-supported values,
- flags unsupported values,
- returns both the final structured result and the check report.

## 8. Limitations

This is an engineering demonstration, not a clinical system.

The current implementation:

- works on text rather than scanned medical PDFs/images,
- checks a small predefined set of fields,
- does not interpret diagnoses,
- does not determine whether a lab value is medically normal,
- does not replace clinician review,
- does not claim production-level medical accuracy,
- uses deterministic parsing/checking to make the failure demonstration reproducible.

A production system would need validated OCR/document parsing, robust model evaluation, privacy/security controls, audit logging, model/version tracking, human review, and clinical validation.

## 9. Why the loop is useful

The project deliberately avoids trying to solve every medical-report problem. It focuses on one failure mode and makes that failure visible.

The key design principle is:

> A confident first answer should be treated as a draft, not as evidence.

The second pass checks the draft against a concrete source-grounding requirement before the result is shown as final.

## 10. Repository contents

```text
app.py
extractor.py
checker.py
requirements.txt
README.md
tests/
results/
docs/WRITEUP.md
```
