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
    tfidf = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out()

def word_count(text):
    return len(text.split())

def validate_slide(slide, rules):
    slide_text = clean_text(slide["slide_text"])
    notes_text = clean_text(slide["notes_text"])

    status = "PASS"
    reason_code = None
    issues = []


    #First Rule: Check for missing content
    
    if not slide_text or not notes_text:
        return {
            "Slide": slide["slide_number"],
            "Status": "FAIL",
            "Reason": "Missing Content",
            "Explanation": "Slide or notes are empty"
        }

    slide_concepts = extract_concepts(slide_text)
    notes_concepts = extract_concepts(notes_text)
    overlap = set(slide_concepts).intersection(set(notes_concepts))
    overlap_ratio = len(overlap) / max(len(notes_concepts), 1)

    sim_score = semantic_similarity(slide_text, notes_text)

    if overlap_ratio < 0.3 and sim_score < rules["semantic_similarity"]["min_slide_note_similarity"]:
        status = "FAIL"
        reason_code = "Topic Drift"
        issues.append("Notes introduce a different instructional concept")

    if len(notes_concepts) > len(slide_concepts) * 2:
        status = "FAIL"
        reason_code = "Multiple Concepts"
        issues.append("Multiple instructional ideas in one slide")
        
     # --- Rule 1: Meaning / Context Change ---
    meaning_score = semantic_similarity(slide_text, notes_text)

    if meaning_score < rules["semantic_similarity"]["meaning_match_threshold"]:
        status = "FAIL"
        reason_code = "MEANING_MISMATCH"
        issues.append("Slide content and video context do not match")   
        
        
     # --- Rule 2: Word Limit ---
    slide_words = word_count(slide_text)
    max_words = rules["word_limits"]["avg_slide_word_limit"]

    if slide_words > max_words:
        status = "FAIL"
        reason_code = "WORD_LIMIT_EXCEEDED"
        issues.append(
            f"Slide has {slide_words} words (limit: {max_words})"
        )
        
    
     # --- Rule 3: Missing Key Content ---
    slide_concepts = extract_concepts(slide_text)
    notes_concepts = extract_concepts(notes_text)

    overlap = set(slide_concepts).intersection(set(notes_concepts))
    overlap_ratio = len(overlap) / max(len(notes_concepts), 1)

    if overlap_ratio < rules["content_coverage"]["min_concept_overlap_ratio"]:
        status = "FAIL"
        reason_code = "MISSING_CONTENT"
        issues.append("Important concepts in notes are missing from slide")
        

    return {
        "slide_number": slide["slide_number"],
        "status": status,
        "reason_code": reason_code,
        "issues": "; ".join(issues) if issues else "Properly chunked",
        "similarity_score": round(meaning_score, 3)
    }
