from sklearn.feature_extraction.text import TfidfVectorizer
from src.nlp.semantic import semantic_similarity
from src.nlp.text_utils import clean_text


def extract_concepts(text):
    if not text:
        return []
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=12
    )
    vectorizer.fit([text])
    return vectorizer.get_feature_names_out()


def word_count(text):
    return len(text.split())


def validate_slide(slide, rules):
    slide_text = clean_text(slide["slide_text"])
    notes_text = clean_text(slide["notes_text"])

    issues = []
    reason_codes = []

    # Rule 0: Missing content
    if not slide_text or not notes_text:
        return {
            "Slide": slide["slide_number"],
            "Status": "FAIL",
            "Reason Code": "Missing Content",
            "Issues": "Slide or notes are empty",
            "Similarity Score": 0.0
        }

    # Pre-compute once
    similarity = semantic_similarity(slide_text, notes_text)
    slide_concepts = extract_concepts(slide_text)
    notes_concepts = extract_concepts(notes_text)

    overlap = set(slide_concepts).intersection(set(notes_concepts))
    overlap_ratio = len(overlap) / max(len(notes_concepts), 1)

    # Rule 1: Topic drift
    if overlap_ratio < 0.3 and similarity < rules["semantic_similarity"]["min_slide_note_similarity"]:
        issues.append("Notes drift away from slide topic")
        reason_codes.append("Topic Drift")

    # Rule 2: Multiple concepts
    if len(notes_concepts) > len(slide_concepts) * 2:
        issues.append("Too many concepts in narration")
        reason_codes.append("Multiple Concepts")

    # Rule 3: Meaning mismatch
    if similarity < rules["semantic_similarity"]["meaning_match_threshold"]:
        issues.append("Slide and narration meaning mismatch")
        reason_codes.append("MEANING_MISMATCH")

    # Rule 4: Word limit
    if word_count(slide_text) > rules["word_limits"]["avg_slide_word_limit"]:
        issues.append("Slide text exceeds word limit")
        reason_codes.append("WORD_LIMIT_EXCEEDED")

    # Rule 5: Missing content coverage
    if overlap_ratio < rules["content_coverage"]["min_concept_overlap_ratio"]:
        issues.append("Important narration concepts missing in slide")
        reason_codes.append("MISSING_CONTENT")

    status = "FAIL" if issues else "PASS"

    return {
        "Slide": slide["slide_number"],
        "Status": status,
        "Reason Code": ", ".join(reason_codes) if reason_codes else None,
        "Issues": "; ".join(issues) if issues else "Properly chunked",
        "Similarity Score": round(similarity, 3)
    }
