from .text_extractors import get_slide_text, get_vo_text
from .embedding_matcher import compare_point_to_vo, vo_coverage_check

def analyze_slide(slide, slide_no):
    slide_points = get_slide_text(slide)
    vo_lines = get_vo_text(slide)

    rows = []
    summary = []

    chunk_results = []
    copy_flags = []

    for idx, point in enumerate(slide_points, start=1):
        vo, score, mtype, comment = compare_point_to_vo(point, vo_lines)

        if mtype in {"Exact Copy", "Strong"}:
            chunk = "Chunked Properly"
        elif mtype == "Partial":
            chunk = "Partially Chunked"
        else:
            chunk = "Not Chunked Properly"

        rows.append({
            "Slide Number": slide_no,
            "Point Number": idx,
            "Slide Point": point,
            "Matched VO Sentence": vo,
            "Similarity Score": round(score, 2),
            "Match Type": mtype,
            "Exact Copy-Paste": "Yes" if mtype == "Exact Copy" else "No",
            "Comment": comment
        })

        chunk_results.append(chunk)
        copy_flags.append(mtype == "Exact Copy")

    uncovered_vo, vo_ratio = vo_coverage_check(slide_points, vo_lines)
    vo_pct = round(vo_ratio * 100, 2)

    if not slide_points:
        final_status = "No Content"
    elif all(c == "Chunked Properly" for c in chunk_results) and vo_pct >= 90:
        final_status = "Chunked Properly"
    elif vo_pct < 50:
        final_status = "Not Chunked Properly"
    else:
        final_status = "Partially Chunked"

    summary.append({
        "Slide Number": slide_no,
        "Chunking Status": final_status,
        "Direct Match with Note": "Yes" if any(copy_flags) else "No",
        "VO Coverage %": vo_pct,
        "Uncovered VO Lines": " | ".join(uncovered_vo)
    })

    return rows, summary
