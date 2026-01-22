from pptx import Presentation

def read_ppt(uploaded_file):
    prs = Presentation(uploaded_file)
    return list(prs.slides)   # ✅ RETURN REAL SLIDES
