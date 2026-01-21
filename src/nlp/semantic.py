from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

_model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0

   
    emb1 = _model.encode(text1, convert_to_tensor=True)
    emb2 = _model.encode(text2, convert_to_tensor=True)

    return float(util.cos_sim(emb1, emb2)[0][0])
