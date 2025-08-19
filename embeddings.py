#!/usr/bin/env python3
"""
Index Builder Script - Run this ONCE to create your vector database
This script uses sentence-transformers to create embeddings and build FAISS index
"""

import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime

# Configuration
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DOCS_FOLDER = "docs"
OUTPUT_FOLDER = "vectorstore"

# Output files
FAISS_INDEX_FILE = os.path.join(OUTPUT_FOLDER, "faiss_index.idx")
CHUNKS_FILE = os.path.join(OUTPUT_FOLDER, "chunks.pkl")
METADATA_FILE = os.path.join(OUTPUT_FOLDER, "metadata.json")

class IndexBuilder:
    def __init__(self):
        print("🔧 Initializing Index Builder...")
        print(f"📥 Loading {MODEL_NAME}...")
        self.model = SentenceTransformer(MODEL_NAME)
        print("✅ Model loaded successfully!")
        
        # Create output directory
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    def read_documents(self):
        """Read all documents from docs folder"""
        if not os.path.exists(DOCS_FOLDER):
            print(f"❌ '{DOCS_FOLDER}' folder not found!")
            print(f"📁 Please create '{DOCS_FOLDER}' folder and add your documents (.md, .txt, .py files)")
            return [], []
        
        documents = []
        sources = []
        
        print(f"📖 Reading documents from '{DOCS_FOLDER}'...")
        
        for filename in os.listdir(DOCS_FOLDER):
            if filename.endswith(('.md', '.txt', '.py', '.json', '.rst')):
                filepath = os.path.join(DOCS_FOLDER, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            documents.append(content)
                            sources.append(filename)
                            print(f"  ✓ {filename} ({len(content)} chars)")
                except Exception as e:
                    print(f"  ❌ Error reading {filename}: {e}")
        
        print(f"📚 Loaded {len(documents)} documents")
        return documents, sources
    
    def chunk_document(self, text, chunk_size=800, overlap=150):
        """Split document into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            
            # Try to end at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for delimiter in ['. ', '\n\n', '\n', '. ']:
                    last_delim = chunk.rfind(delimiter)
                    if last_delim > start + chunk_size // 2:
                        chunk = text[start:start + last_delim + len(delimiter)]
                        end = start + last_delim + len(delimiter)
                        break
            
            chunks.append(chunk.strip())
            start = max(end - overlap, end) if end < len(text) else end
            
            if start >= len(text):
                break
                
        return chunks
    
    def build_index(self, chunk_size=800, overlap=150):
        """Build the complete FAISS index"""
        
        # Read documents
        documents, sources = self.read_documents()
        if not documents:
            return False
        
        print(f"\n🔪 Chunking documents (size={chunk_size}, overlap={overlap})...")
        
        all_chunks = []
        chunk_metadata = []
        
        for doc_idx, (document, source) in enumerate(zip(documents, sources)):
            chunks = self.chunk_document(document, chunk_size, overlap)
            print(f"  📄 {source}: {len(chunks)} chunks")
            
            for chunk_idx, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                chunk_metadata.append({
                    'source_file': source,
                    'doc_index': doc_idx,
                    'chunk_index': chunk_idx,
                    'chunk_id': f"{source}_chunk_{chunk_idx + 1}",
                    'content': chunk,
                    'char_count': len(chunk)
                })
        
        total_chunks = len(all_chunks)
        print(f"📊 Total chunks created: {total_chunks}")
        
        if total_chunks == 0:
            print("❌ No chunks created!")
            return False
        
        # Generate embeddings
        print(f"\n🧮 Generating embeddings...")
        print("This may take a few minutes for large document sets...")
        
        embeddings = self.model.encode(
            all_chunks, 
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        print(f"✅ Generated {len(embeddings)} embeddings (dim: {embeddings.shape[1]})")
        
        # Create FAISS index
        print(f"🔍 Building FAISS index...")
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        
        # Convert to float32 (FAISS requirement)
        embeddings = embeddings.astype('float32')
        index.add(embeddings)
        
        # Save everything
        print(f"💾 Saving index and metadata...")
        
        # Save FAISS index
        faiss.write_index(index, FAISS_INDEX_FILE)
        print(f"  ✓ FAISS index: {FAISS_INDEX_FILE}")
        
        # Save chunk data
        with open(CHUNKS_FILE, 'wb') as f:
            pickle.dump(chunk_metadata, f)
        print(f"  ✓ Chunks data: {CHUNKS_FILE}")
        
        # Save metadata
        metadata = {
            'created_at': datetime.now().isoformat(),
            'model_name': MODEL_NAME,
            'total_documents': len(documents),
            'total_chunks': total_chunks,
            'embedding_dimension': dimension,
            'chunk_size': chunk_size,
            'chunk_overlap': overlap,
            'source_files': sources,
            'index_stats': {
                'ntotal': index.ntotal,
                'dimension': index.d
            }
        }
        
        with open(METADATA_FILE, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"  ✓ Metadata: {METADATA_FILE}")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"🎉 INDEX BUILT SUCCESSFULLY!")
        print(f"{'='*60}")
        print(f"📊 Summary:")
        print(f"  • Documents processed: {len(documents)}")
        print(f"  • Total chunks: {total_chunks}")
        print(f"  • Embedding dimension: {dimension}")
        print(f"  • Index size: {index.ntotal} vectors")
        print(f"  • Output folder: {OUTPUT_FOLDER}/")
        print(f"\n💡 Next steps:")
        print(f"  1. Your vector database is ready in '{OUTPUT_FOLDER}/' folder")
        print(f"  2. You can now run the Streamlit app without the embedding model")
        print(f"  3. The app will only load the pre-built index for queries")
        print(f"\n🗑️  Optional: You can now uninstall sentence-transformers if desired:")
        print(f"     pip uninstall sentence-transformers")
        
        return True

def main():
    """Main function"""
    print("🚀 VECTOR DATABASE BUILDER")
    print("=" * 50)
    print("This script will create a vector database from your documents.")
    print("Run this ONCE, then use the lightweight Streamlit app for queries.\n")
    
    builder = IndexBuilder()
    
    # Check if index already exists
    if os.path.exists(FAISS_INDEX_FILE):
        response = input(f"⚠️  Index already exists. Rebuild? (y/N): ").strip().lower()
        if response != 'y':
            print("👍 Using existing index. You can run the Streamlit app now!")
            return
    
    # Build index
    success = builder.build_index(chunk_size=800, overlap=150)
    
    if success:
        print(f"\n🎯 Ready! You can now run: streamlit run streamlit_app.py")
    else:
        print(f"\n❌ Failed to build index. Please check your documents in '{DOCS_FOLDER}' folder.")

if __name__ == "__main__":
    main()