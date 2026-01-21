def generate_recommendation(row):
    if row["Status"] == "PASS":
        return "No action required"

    if row["Reason"] == "Topic Drift":
        return "Split content into a separate slide"

    if row["Reason"] == "Multiple Concepts":
        return "Divide slide into multiple instructional chunks"

    return "Review slide structure"
