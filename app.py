import streamlit as st
import yaml

from src.ppt.ppt_reader import read_ppt_from_file
from src.qc.chunking_validator import validate_slide
from src.qc.explaination_engine import generate_explanation
from src.report.excel_report import generate_excel_report
st.set_page_config(page_title="PPT Chunking QC", layout="wide")

st.title("📊 PPT Chunking QC System")

uploaded_file = st.file_uploader("Upload PPT file", type=["pptx"])

if uploaded_file:
    if st.button("🚀 Run QC"):
        with st.spinner("Running QC..."):
            with open("config/qc_rules.yaml") as f:
                rules = yaml.safe_load(f)

            slides = read_ppt_from_file(uploaded_file)

            results = []
            for slide in slides:
                res = validate_slide(slide, rules)
                res["explanation"] = generate_explanation(res)
                results.append(res)

            st.success("QC Completed")

            st.subheader("QC Results")
            st.dataframe(results)

            excel_file = generate_excel_report(results)

            st.download_button(
                label="⬇ Download QC Excel Report",
                data=excel_file,
                file_name="ppt_chunking_qc_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
