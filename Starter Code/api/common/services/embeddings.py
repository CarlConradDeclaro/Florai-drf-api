# embeddings.py
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text):
    return model.encode(text)

def semantic_search(query, documents, top_k=5):
    query_embedding = embed_text(query)
    document_embeddings = model.encode(documents)

    similarities = cosine_similarity([query_embedding], document_embeddings)[0]
    top_indices = similarities.argsort()[::-1][:top_k]

    return top_indices, similarities[top_indices]
 