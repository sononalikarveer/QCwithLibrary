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

def generate_explanation(reason_code):
    """
    Converts machine-level reason codes into
    human-readable QC explanations + recommendations
    """

    explanations = {
        # Existing + earlier rules
        "Missing Content": (
            "Slide text or notes are missing. "
            "Recommendation: Ensure both slide content and narration notes are present."
        ),

        "Topic Drift": (
            "The narration discusses a different instructional concept than the slide. "
            "Recommendation: Align the slide topic with the video explanation or split the content."
        ),

        "Multiple Concepts": (
            "The slide covers too many instructional ideas at once. "
            "Recommendation: Split the slide into smaller, focused chunks."
        ),

        # New rules you added
        "MEANING_MISMATCH": (
            "The slide content and video narration do not convey the same meaning. "
            "Recommendation: Review the instructional intent and align slide content with narration."
        ),

        "WORD_LIMIT_EXCEEDED": (
            "The slide contains more text than recommended for effective learning. "
            "Recommendation: Reduce slide text and move detailed explanations to narration notes."
        ),

        "MISSING_CONTENT": (
            "Important concepts mentioned in the narration are missing from the slide. "
            "Recommendation: Add the missing key points to the slide for better learner clarity."
        ),

        # Default fallback
        None: "No QC issues detected. Slide is properly chunked."
    }

    return explanations.get(reason_code, "QC issue detected. Please review the slide content.")
