from pptx import Presentation

def read_ppt(file_path):
    prs = Presentation(file_path)
    slides = []

    for idx, slide in enumerate(prs.slides, start=1):
        slide_text = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                slide_text.append(shape.text)

        notes_text = ""
        if slide.has_notes_slide:
            notes_text = slide.notes_slide.notes_text_frame.text

        slides.append({
            "slide_number": idx,
            "slide_text": " ".join(slide_text),
            "notes_text": notes_text
        })

    return slides
