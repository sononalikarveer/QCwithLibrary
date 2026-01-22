from .embedding_model import get_embedding_model

def normalize(text):
    return text.lower().strip()

def compare_point_to_vo(point, vo_lines):
    if not vo_lines:
        return ("", 0.0, "Missing", "No VO content")

    model, util = get_embedding_model()

    p_emb = model.encode(point, convert_to_tensor=True)
    v_emb = model.encode(vo_lines, convert_to_tensor=True)

    scores = util.cos_sim(p_emb, v_emb)[0]
    best_score = float(scores.max())
    best_idx = int(scores.argmax())
    best_vo = vo_lines[best_idx]

    if normalize(point) == normalize(best_vo):
        return best_vo, 1.0, "Exact Copy", "Perfect match (copied)"
    elif best_score >= 0.75:
        return best_vo, best_score, "Strong", "Chunked properly"
    elif best_score >= 0.5:
        return best_vo, best_score, "Partial", "Partially matching"
    else:
        return best_vo, best_score, "Missing", "No strong match"

def vo_coverage_check(slide_points, vo_lines, threshold=0.75):
    if not vo_lines:
        return [], 1.0

    if not slide_points:
        return vo_lines, 0.0

    model, util = get_embedding_model()

    sp_emb = model.encode(slide_points, convert_to_tensor=True)
    vo_emb = model.encode(vo_lines, convert_to_tensor=True)

    sim = util.cos_sim(vo_emb, sp_emb)
    best_scores = sim.max(dim=1).values.tolist()

    uncovered = []
    covered = 0

    for vo, score in zip(vo_lines, best_scores):
        if score >= threshold:
            covered += 1
        else:
            uncovered.append(vo)

    return uncovered, covered / len(vo_lines)
