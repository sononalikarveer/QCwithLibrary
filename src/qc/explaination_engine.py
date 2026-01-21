def generate_explanation(result):
    if result["status"] == "PASS":
        return "Slide is properly chunked. Notes elaborate on the same instructional concept."

    issues = result["issues"].lower()

    if "different instructional concept" in issues:
        return (
            "Notes introduce a new instructional concept that is not reflected on the slide. "
            "This causes cognitive overload. Recommendation: split content into a separate slide."
        )

    if "multiple concepts" in issues:
        return (
            "Slide covers multiple instructional ideas in a single chunk. "
            "Instructional design best practice recommends one concept per slide."
        )

    return (
        "Slide content and narration are misaligned. "
        "Recommendation: review chunk boundaries and align narration with slide intent."
    )
