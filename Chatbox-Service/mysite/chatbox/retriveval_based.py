import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

qa_index_path = os.getenv("QA_INDEX_PATH")
qa_meta_path = os.getenv("QA_META_PATH")

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(qa_index_path)

with open(qa_meta_path, "r", encoding="utf-8") as f:
    qa_pairs = json.load(f)

def search(query, top_k=1):
    q_emb = model.encode([query])
    distances, indices = index.search(np.array(q_emb, dtype="float32"), top_k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        item = qa_pairs[idx]
        distance = distances[0][i]
        logging.info(f"Distance = {distance}")
        if distance >= 1:
            return [{"message": "Your question is beyond the system's understanding!"}]
        
        results.append({
            "rank": i+1,
            "question": item["text"],
            "answer": item["answer"],
            "distance": float(distances[0][i]),
        })
    return results
