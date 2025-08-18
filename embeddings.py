from sentence_transformers import SentenceTransformer
import numpy as np
import os
import faiss
import pickle

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

texts = []
for fname in os.listdir("docs"):
        with open(os.path.join("docs", fname), "r",encoding="utf8") as f:
            texts.append(f.read().strip())

#simple chuking
chunks = []
for text in texts:
    for i in range(0, len(text), 500):
         chunks.append(text[i:i+500])
         
#encode chunks
emb = model.encode(chunks,normalize_embeddings=True)
emb = np.array(emb, dtype=np.float32)  

sentences = [
    "That is a happy person",
    "That is a happy dog",
    "That is a very happy person",
    "Today is a sunny day"
]
embeddings = model.encode(sentences)

similarities = model.similarity(embeddings, embeddings)
print(similarities.shape)
# [4, 4]