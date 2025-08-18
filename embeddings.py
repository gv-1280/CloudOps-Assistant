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

#build FAISS index
index = faiss.IndexFlatIP(emb.shape[1])
index.add(emb)

os.makedirs("vectorstore", exist_ok=True)
faiss.write_index(index,"vectorstore/faiss_index.idx")
with open("vectorstore/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("FAISS index saved with {len(chunks)} chunks")
