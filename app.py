import streamlit as st
import yaml

from src.ppt.ppt_reader import read_ppt
from src.qc.chunking_validator import validate_slide
from src.qc.explanation_engine import generate_explanation
from src.report.excel_report import create_excel

st.set_page_config(page_title="PPT Chunking QC", layout="wide", initial_sidebar_state="expanded")

st.title("📊 PPT Chunking QC Tool")
st.write("Upload a PPT file to validate instructional chunking.")

uploaded_file = st.file_uploader("Upload PPT file", type=["pptx"])

if uploaded_file:
    if st.button("Run QC"):
        with st.spinner("Running QC..."):
            with open("config/qc_rules.yaml") as f:
                rules = yaml.safe_load(f)

            slides = read_ppt(uploaded_file)
            results = []

            for slide in slides:
                res = validate_slide(slide, rules)
                res["Recommendation"] = generate_explanation(res.get("Reason Code"))
                results.append(res)

            st.success("QC Completed")

            st.subheader("QC Results")
            st.dataframe(results, use_container_width=True)

            excel_file = create_excel(results)

            st.download_button(
                label="⬇ Download Excel Report",
                data=excel_file,
                file_name="ppt_chunking_qc_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
