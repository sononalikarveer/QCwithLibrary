def generate_explanation(result):
    if result["status"] == "PASS":
        return "Slide is properly chunked. Notes align with slide intent."

    if result["reason_code"] == "TOPIC_DRIFT":
        return "Notes introduce a new instructional concept. Recommend splitting into a separate slide."

    if result["reason_code"] == "MULTI_TOPIC":
        return "Multiple instructional concepts detected. Recommend splitting content."

    if result["reason_code"] == "MISSING_CONTENT":
        return "Slide or notes are missing. Cannot validate chunking."

    return "Chunking issue detected. Review slide."
