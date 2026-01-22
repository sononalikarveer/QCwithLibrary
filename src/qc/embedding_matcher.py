from .embedding_model import model, util

def normalize(text):
    return text.lower().strip()

def compare_point_to_vo(point, vo_lines):
    if not vo_lines:
        return "", 0.0, "Missing", "No VO content"

    p_emb = model.encode(point, convert_to_tensor=True)
    v_emb = model.encode(vo_lines, convert_to_tensor=True)

    scores = util.cos_sim(p_emb, v_emb)[0]
    best_score = float(scores.max())
    best_idx = int(scores.argmax())
    best_vo = vo_lines[best_idx]

    if normalize(point) == normalize(best_vo):
        return best_vo, 1.0, "Exact Copy", "Copied from notes"
    elif best_score >= 0.75:
        return best_vo, best_score, "Strong", "Chunked properly"
    elif best_score >= 0.5:
        return best_vo, best_score, "Partial", "Partially matching"
    else:
        return best_vo, best_score, "Missing", "No strong match"
