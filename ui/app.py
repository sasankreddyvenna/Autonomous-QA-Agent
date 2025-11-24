import streamlit as st
import requests
import pandas as pd
import re

BACKEND_URL = "http://127.0.0.1:8000"

st.title("Autonomous QA Agent")

# ----------------------------------
# SESSION STATE (PERSIST TEST CASES)
# ----------------------------------
if "testcases" not in st.session_state:
    st.session_state.testcases = []

if "last_output" not in st.session_state:
    st.session_state.last_output = ""

# ----------------------------------
# DOCUMENT UPLOAD SECTION
# ----------------------------------

st.header("Upload Documents for Ingestion")

uploaded_files = st.file_uploader(
    "Upload one or more documents",
    type=["pdf", "html", "txt", "md", "json"],
    accept_multiple_files=True
)

if st.button("Upload and Ingest"):
    if uploaded_files:
        files = [
            ("files", (file.name, file, file.type or "application/octet-stream"))
            for file in uploaded_files
        ]

        response = requests.post(f"{BACKEND_URL}/ingest/upload", files=files)

        if response.ok:
            st.success(f"Uploaded {len(uploaded_files)} files successfully.")
            st.json(response.json())
        else:
            st.error(f"Upload failed: {response.text}")
    else:
        st.warning("Please select at least one file.")

# ----------------------------------
# TESTCASE GENERATION SECTION
# ----------------------------------

st.header("Generate Test Cases")

with st.form("testcase_form"):
    testcase_query = st.text_input("Enter query for test case generation:")
    submitted = st.form_submit_button("Generate Test Cases")

if submitted:
    if testcase_query.strip():
        payload = {"query": testcase_query.strip(), "top_k": 5}
        try:
            response = requests.post(
                f"{BACKEND_URL}/testcases/generate",
                json=payload,
                timeout=300
            )
            response.raise_for_status()

            raw_output = response.json().get("testcases", "")
            st.session_state.last_output = raw_output  # Save output

            st.subheader("📋 Generated Test Cases (Table Output)")
            st.markdown(raw_output)

            # ✅ Parse rows
            rows = []
            for line in raw_output.split("\n"):
                cells = [c.strip() for c in re.split(r"\s*\|\s*", line) if c.strip()]
                if len(cells) >= 4 and "Test" not in cells[0]:
                    rows.append({
                        "id": cells[0],
                        "scenario": cells[1],
                        "steps": cells[2],
                        "expected_result": cells[3]
                    })

            if not rows:
                st.error("❌ Unable to parse table. LLM output may not be tabular.")
            else:
                st.session_state.testcases = rows  # ✅ Persist
                df = pd.DataFrame(rows)
                st.dataframe(df)

        except requests.exceptions.RequestException as e:
            st.error(f"Failed: {e}")
    else:
        st.warning("Please enter a query.")

# ----------------------------------
# PHASE 3: SELENIUM SCRIPT GENERATION
# ----------------------------------

if st.session_state.testcases:
    st.subheader("🔧 Selenium Script Generator")

    selected = st.selectbox(
        "Select a Test Case",
        st.session_state.testcases,
        format_func=lambda x: f"{x['id']} - {x['scenario']}"
    )

    if st.button("Generate Selenium Script"):
        script_payload = {
            "test_id": selected["id"],
            "scenario": selected["scenario"],
            "steps": selected["steps"],
            "expected_result": selected["expected_result"]
        }

        script_response = requests.post(
            f"{BACKEND_URL}/script/generate",
            json=script_payload,
            timeout=300
        )

        if script_response.status_code == 200:
            script = script_response.json().get("selenium_script", "")
            st.subheader("✅ Generated Selenium Script")
            st.code(script, language="python")

            st.download_button(
                label="⬇️ Download Script",
                data=script,
                file_name=f"{selected['id']}.py",
                mime="text/plain"
            )
        else:
            st.error("❌ Script generation failed.")
