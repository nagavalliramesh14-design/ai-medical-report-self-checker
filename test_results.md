# Recorded Test Results

These are the five project test cases included in `tests/test_self_checker.py`.

| Test | Input condition | First-pass behavior | Checker result | Outcome |
|---|---|---|---|---|
| 1 | Correct report | All values match | PASS | No issue |
| 2 | Cholesterol draft changed to 285 mg/dL while source says 185 mg/dL | Confident, plausible wrong value | MISMATCH; corrected to 185 mg/dL | TRIPPED CHECK |
| 3 | Hemoglobin draft changed to 11.2 g/dL while source says 10.2 g/dL | Wrong numeric value | MISMATCH; corrected to 10.2 g/dL | TRIPPED CHECK |
| 4 | Draft contains creatinine although source has no creatinine | Unsupported value | FLAG | TRIPPED CHECK |
| 5 | Draft misses glucose although source contains it | Missing value | FLAG/CORRECT; restored to 96 mg/dL | TRIPPED CHECK |

## Expected test command

```bash
pytest -q
```

Expected result:

```text
5 passed
```

## Key demonstration

The most important test is Test 2:

```text
SOURCE:  Total Cholesterol: 185 mg/dL
DRAFT:   Total Cholesterol: 285 mg/dL
CHECK:   MISMATCH
FINAL:   Total Cholesterol: 185 mg/dL
```

The value 285 mg/dL is intentionally plausible-looking and is used to demonstrate that the second pass does not simply trust a confident first answer.
