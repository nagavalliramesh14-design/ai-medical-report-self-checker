import streamlit as st
from extractor import extract_report
from checker import self_check

st.set_page_config(page_title="Medical Report Self-Checker", page_icon="🩺", layout="wide")

st.title("🩺 AI Medical Report Extraction Self-Checker")
st.caption("A narrow AI reliability demo: extract key lab values, then independently verify every value against the source report.")

DEFAULT_REPORT = """Patient: Demo Patient
Hemoglobin: 10.2 g/dL
Glucose: 96 mg/dL
Total Cholesterol: 185 mg/dL
Creatinine: 0.9 mg/dL
"""

with st.sidebar:
    st.header("How it works")
    st.markdown("1. Enter a short medical report.\n2. The first pass extracts lab values.\n3. The second pass verifies each value against the source.\n4. Mismatches are corrected or flagged.")
    st.warning("Demo only. This tool is not a medical diagnostic system.")

report = st.text_area("Medical report text", value=DEFAULT_REPORT, height=220)

col1, col2 = st.columns(2)
with col1:
    if st.button("Run Self-Check", type="primary", use_container_width=True):
        draft = extract_report(report)
        checked = self_check(report, draft)
        st.session_state["draft"] = draft
        st.session_state["checked"] = checked

with col2:
    if st.button("Load Confidently Wrong Demo", use_container_width=True):
        report = DEFAULT_REPORT
        draft = extract_report(report, force_demo_error=True)
        checked = self_check(report, draft)
        st.session_state["draft"] = draft
        st.session_state["checked"] = checked

if "checked" in st.session_state:
    draft = st.session_state["draft"]
    checked = st.session_state["checked"]

    st.subheader("1. First-pass draft")
    st.json(draft)

    st.subheader("2. Self-check result")
    status = checked["self_check"]["status"]
    if status == "PASS":
        st.success("PASS — no extraction mismatch was found.")
    else:
        st.error(f"{status} — the second pass found an issue.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Fields checked", checked["self_check"]["fields_checked"])
    c2.metric("Issues found", checked["self_check"]["issues_found"])
    c3.metric("Corrected", checked["self_check"]["corrected_fields"])

    st.subheader("3. Before → After")
    for item in checked["checks"]:
        if item["status"] == "MATCH":
            st.write(f"✅ **{item['field']}**: {item['draft_value']}")
        else:
            st.error(
                f"⚠️ **{item['field']}** — Before: `{item['draft_value']}` → "
                f"After: `{item['source_value']}` | {item['reason']}"
            )

    st.subheader("4. Final structured result")
    st.json(checked["final_result"])

    st.subheader("5. What the check found")
    st.json(checked["self_check"])
else:
    st.info("Enter a report and click **Run Self-Check**. For the required confident-error demonstration, click **Load Confidently Wrong Demo**.")
