from nlp.semantic import semantic_similarity
from nlp.text_utils import clean_text
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_concepts(text):
    if not text:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=10
    )
    tfidf = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out()

def validate_slide(slide, rules):
    slide_text = clean_text(slide["slide_text"])
    notes_text = clean_text(slide["notes_text"])

    # 🔹 Default values (IMPORTANT)
    status = "PASS"
    reason_code = None
    issues = []

    if not slide_text or not notes_text:
        return {
            "slide_number": slide["slide_number"],
            "similarity_score": 0.0,
            "status": "FAIL",
            "reason_code": "MISSING_CONTENT",
            "issues": "Missing slide text or notes"
        }

    # Concept extraction
    slide_concepts = extract_concepts(slide_text)
    notes_concepts = extract_concepts(notes_text)

    # Concept overlap
    overlap = set(slide_concepts).intersection(set(notes_concepts))
    overlap_ratio = len(overlap) / max(len(notes_concepts), 1)

    # Semantic similarity
    semantic_score = semantic_similarity(slide_text, notes_text)

    # RULE 1: Topic drift
    if overlap_ratio < 0.3 and semantic_score < rules["semantic_similarity"]["min_slide_note_similarity"]:
        status = "FAIL"
        reason_code = "TOPIC_DRIFT"
        issues.append("Notes drift to a different instructional concept")

    # RULE 2: Multiple concepts
    if len(notes_concepts) > len(slide_concepts) * 2:
        status = "FAIL"
        reason_code = "MULTI_TOPIC"
        issues.append("Notes cover multiple concepts – possible poor chunking")

    if not issues:
        issues.append("Properly chunked")

    return {
        "slide_number": slide["slide_number"],
        "similarity_score": round(semantic_score, 3),
        "status": status,
        "reason_code": reason_code,
        "issues": "; ".join(issues)
    }
