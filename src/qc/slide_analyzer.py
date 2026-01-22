from .text_extractors import get_slide_text, get_vo_text
from .embedding_matcher import compare_point_to_vo

def analyze_slide(slide, slide_no):
    slide_points = get_slide_text(slide)
    vo_lines = get_vo_text(slide)

    rows = []

    for idx, point in enumerate(slide_points, start=1):
        vo, score, mtype, comment = compare_point_to_vo(point, vo_lines)

        rows.append({
            "Slide Number": slide_no,
            "Point Number": idx,
            "Slide Point": point,
            "Matched VO Sentence": vo,
            "Similarity Score": round(score, 2),
            "Match Type": mtype,
            "Comment": comment
        })

    if not slide_points:
        rows.append({
            "Slide Number": slide_no,
            "Point Number": "-",
            "Slide Point": "No content",
            "Matched VO Sentence": "",
            "Similarity Score": 0,
            "Match Type": "No Content",
            "Comment": "Empty slide"
        })

    return rows
