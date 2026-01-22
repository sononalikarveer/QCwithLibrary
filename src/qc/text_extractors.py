import re
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.dml.color import RGBColor

def clean_text(text):
    return re.sub(r"\s+", " ", text.strip())

def get_slide_text(slide):
    points = []

    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue

        for para in shape.text_frame.paragraphs:
            text = "".join(run.text for run in para.runs).strip()
            if not text:
                continue

            font_color = None

            if para.runs:
                color = para.runs[0].font.color

                # ✅ SAFE COLOR CHECK
                if color is not None and hasattr(color, "rgb"):
                    font_color = color.rgb
                else:
                    font_color = None   # Theme / Auto color

            # ❗ Exclude only if explicitly orange
            if font_color == RGBColor(242, 103, 34):
                continue

            points.append(clean_text(text))

    return points


def get_vo_text(slide):
    if not slide.has_notes_slide:
        return []

    notes = slide.notes_slide.notes_text_frame.text

    match = re.search(
        r'(?i)vo:\s*(.*?)(Image Link:|Instructions to GD:|$)',
        notes,
        re.DOTALL
    )

    if not match:
        return []

    return [
        clean_text(line.strip("-• "))
        for line in match.group(1).split("\n")
        if line.strip()
    ]
