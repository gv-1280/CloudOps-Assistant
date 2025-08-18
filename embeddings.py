# embeddings.py

import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# Paths
DOCS_DIR = "docs"
INDEX_FILE = "faiss_index.idx"
MAPPING_FILE = "doc_mapping.pkl"

# Load embedding model
print("[INFO] Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def read_documents():
    texts, sources = [], []
    for file in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, file)
        if os.path.isfile(path) and file.endswith(".md"):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    texts.append(content)
                    sources.append(file)
    return texts, sources

def create_faiss_index(texts, sources):
    print(f"[INFO] Creating embeddings for {len(texts)} documents...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # FAISS index (L2 distance)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index + mapping
    faiss.write_index(index, INDEX_FILE)
    with open(MAPPING_FILE, "wb") as f:
        pickle.dump(sources, f)

    print(f"[INFO] FAISS index saved to {INDEX_FILE}")
    print(f"[INFO] Document mapping saved to {MAPPING_FILE}")

if __name__ == "__main__":
    docs, files = read_documents()
    if not docs:
        print("[WARN] No documents found in 'docs/' folder.")
    else:
        create_faiss_index(docs, files)
