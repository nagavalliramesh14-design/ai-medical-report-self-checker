# Before and After

## Confidently wrong first draft

### Source

```text
Total Cholesterol: 185 mg/dL
```

### First-pass draft

```json
{
  "total_cholesterol": "285 mg/dL"
}
```

### Second-pass finding

```json
{
  "field": "total_cholesterol",
  "status": "MISMATCH",
  "draft_value": "285 mg/dL",
  "source_value": "185 mg/dL",
  "reason": "Extracted value does not match the source document."
}
```

### Corrected final result

```json
{
  "total_cholesterol": "185 mg/dL"
}
```

## Why this is a real self-check

The first pass is allowed to be wrong. The second pass does not evaluate whether the answer "sounds medical"; it checks a specific observable property: whether the value is supported by the source text.
