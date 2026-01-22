import streamlit as st

from src.ppt.ppt_reader import read_ppt
from src.qc.slide_analyzer import analyze_slide
from src.report.excel_report import create_excel

st.set_page_config(
    page_title="PPT Chunking QC",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 PPT Chunking QC Tool")
st.write("Upload a PPT file to validate instructional chunking.")

uploaded_file = st.file_uploader("Upload PPT file", type=["pptx"])

if uploaded_file:
    if st.button("Run QC"):
        with st.spinner("Running QC..."):
            slides = read_ppt(uploaded_file)

            all_rows = []
            summary_rows = []

            for slide_no, slide in enumerate(slides, start=1):
                rows, summary = analyze_slide(slide, slide_no)
                all_rows.extend(rows)
                summary_rows.extend(summary)

            st.success("QC Completed")

            st.subheader("QC Results (Slide Point Analysis)")
            st.dataframe(all_rows, use_container_width=True)

            excel_file = create_excel(all_rows, summary_rows)

            st.download_button(
                label="⬇ Download Excel Report",
                data=excel_file,
                file_name="ppt_chunking_qc_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
