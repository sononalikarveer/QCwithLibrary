import streamlit as st

from src.ppt.ppt_reader import read_ppt # Read PPT slides (i/p)
from src.qc.slide_analyzer import analyze_slide # The brain of QC logic
from src.report.excel_report import create_excel # Create Excel report (o/p)

st.set_page_config(
    page_title="PPT Chunking QC",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 PPT Chunking QC Tool")
st.write("Upload Your PPT file here to validate instructional chunking.")

uploaded_file = st.file_uploader("Upload PPT ", type=["pptx"])

if uploaded_file and st.button("Run QC"):
    with st.spinner("Running QC..."):

        slides = read_ppt(uploaded_file)

        results = []

        for slide_no, slide in enumerate(slides, start=1):
            rows = analyze_slide(slide, slide_no)
            results.extend(rows)

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
