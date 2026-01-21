# def generate_recommendation(row):
#     if row["Status"] == "PASS":
#         return "No action required"

#     if row["Reason"] == "Topic Drift":
#         return "Split content into a separate slide"

#     if row["Reason"] == "Multiple Concepts":
#         return "Divide slide into multiple instructional chunks"

#     return "Review slide structure"

# def generate_explanation(reason_code):
#     explanations = {
        
        
#         "MEANING_MISMATCH": (
#             "The slide and video explain different concepts. "
#             "Recommendation: Check instructional context and align slide with narration."
#         ),

#         "WORD_LIMIT_EXCEEDED": (
#             "The slide contains too much text. "
#             "Recommendation: Reduce on-slide text and move explanation to notes."
#         ),

#         "MISSING_CONTENT": (
#             "Key concepts mentioned in the narration are missing on the slide. "
#             "Recommendation: Add the missing concepts to the slide."
#         ),

#         "MISSING_TEXT": (
#             "Slide or notes are empty. "
#             "Recommendation: Ensure both slide content and narration are present."
#         )
#     }

#     return explanations.get(reason_code, "No issues detected.")

def generate_explanation(reason_codes):
    if not reason_codes:
        return "No action needed."

    if isinstance(reason_codes, str):
        reason_codes = [r.strip() for r in reason_codes.split(",")]

    explanations = {
        "Missing Content": "Add slide text and narration notes.",
        "Topic Drift": "Align slide topic with narration.",
        "Multiple Concepts": "Split content into smaller slides.",
        "MEANING_MISMATCH": "Ensure slide meaning matches narration.",
        "WORD_LIMIT_EXCEEDED": "Reduce slide text.",
        "MISSING_CONTENT": "Add missing key concepts to slide."
    }

    recs = [explanations.get(code, "Review slide.") for code in reason_codes]
    return " ".join(recs)

