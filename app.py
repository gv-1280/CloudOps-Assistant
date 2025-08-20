#!/usr/bin/env python3

import streamlit as st
import faiss
import pickle
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
VECTOR_DB_FOLDER = "vectorstore"
FAISS_INDEX_FILE = os.path.join(VECTOR_DB_FOLDER, "faiss_index.idx")
CHUNKS_FILE = os.path.join(VECTOR_DB_FOLDER, "chunks.pkl")
METADATA_FILE = os.path.join(VECTOR_DB_FOLDER, "metadata.json")

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("API_KEY")
OPENROUTER_MODEL = "openai/gpt-oss-20b:free"  
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are a helpful CloudOps Assistant specializing in Cloud & DevOps engineering. 
You help engineers with Kubernetes, Docker, Cloud infrastructure, Git/Github, CI/CD, and DevOps best practices.

Instructions:
- Answer based on the provided context documents
- Focus on practical, actionable advice
- Include code examples when relevant
- If context is insufficient, provide general CloudOps guidance
- Keep responses clear and concise
- Mention specific tools, commands, or configurations when applicable"""

class CloudOpsAssistant:
    def __init__(self):
        self.index = None
        self.chunks = None
        self.metadata = None
        self._load_database()
    
    def _load_database(self):
        """Load vector database silently"""
        try:
            if all(os.path.exists(f) for f in [FAISS_INDEX_FILE, CHUNKS_FILE, METADATA_FILE]):
                self.index = faiss.read_index(FAISS_INDEX_FILE)
                with open(CHUNKS_FILE, 'rb') as f:
                    self.chunks = pickle.load(f)
                with open(METADATA_FILE, 'r') as f:
                    self.metadata = json.load(f)
                return True
            return False
        except:
            return False
    
    def search_knowledge_base(self, query, top_k=3):
        """Search using keyword matching"""
        if not self.chunks:
            return []
        
        query_lower = query.lower()
        query_words = set(query_lower.split())
        scored_chunks = []
        
        for chunk in self.chunks:
            content_lower = chunk['content'].lower()
            content_words = set(content_lower.split())
            common_words = query_words.intersection(content_words)
            
            if common_words:
                score = len(common_words) / len(query_words) * (1 + content_lower.count(query_lower) * 0.1)
                scored_chunks.append({
                    'source_file': chunk['source_file'],
                    'content': chunk['content'],
                    'similarity_score': min(score, 1.0)
                })
        
        scored_chunks.sort(key=lambda x: x['similarity_score'], reverse=True)
        return scored_chunks[:top_k]
    
    def generate_answer(self, query, context_chunks):
        """Generate comprehensive answer using OpenRouter API + Vectorstore"""
        if not OPENROUTER_API_KEY:
            return "API key not configured. Please add API_KEY to your environment variables."
        
        try:
            context_parts = []
            if context_chunks:
                for chunk in context_chunks:
                    context_parts.append(f"📄 {chunk['source_file']}:\n{chunk['content']}\n")
                context = "\n".join(context_parts)
            else:
                context = "No direct matches found in vectorstore, but I'll provide general CloudOps guidance."
            
            user_prompt = f"""You are answering as a CloudOps Assistant using both your AI knowledge and the provided vectorstore context.

VECTORSTORE CONTEXT:
{context}

CLOUDOPS QUESTION: {query}

INSTRUCTIONS:
1. Use the vectorstore context as your primary source when available
2. Combine it with your AI knowledge of CloudOps best practices  
3. Provide practical, actionable advice with code examples
4. If vectorstore context is limited, supplement with your general CloudOps expertise
5. Focus on Kubernetes, Docker, Cloud infrastructure, Git/GitHub, CI/CD, DevOps tools

Please provide a comprehensive answer combining both sources:"""
            
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 1200,
                "temperature": 0.1
            }
            
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"API request failed. Status code: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "Request timeout. Please try again."
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    st.set_page_config(
        page_title="CloudOps Assistant",
        page_icon="☁️",
        layout="wide"
    )
    
    st.title("☁️ CloudOps Assistant")
    st.markdown("*AI assistant for Kubernetes, Docker, Cloud Infrastructure & DevOps*")
    
    assistant = CloudOpsAssistant()
    
    if not assistant.chunks:
        st.error("Vector database not found. Please ensure vectorstore files exist.")
        st.stop()
    
    query = st.text_area(
        "Ask your CloudOps question:",
        placeholder="Examples:\n• How to deploy a Pod in Kubernetes?\n• Docker best practices for production\n• Kubernetes troubleshooting guide\n• Git branching strategies for DevOps\n• How to create ConfigMaps and Secrets?\n• CI/CD pipeline setup with GitHub Actions",
        height=240
    )
            
    col1, col2 = st.columns([1.5, 4.5])
    with col1:
        analyze_clicked = st.button("🔍 Analyze", type="primary", use_container_width=True)
    if analyze_clicked:
        if query.strip():
            with st.spinner("Generating answer..."):
                search_results = assistant.search_knowledge_base(query, top_k=3)
                answer = assistant.generate_answer(query, search_results)
            
                st.subheader("🤖 CloudOps Answer (AI + Vectorstore)")
                st.markdown(answer, unsafe_allow_html=True)
            
                if search_results:
                    st.subheader("📚 Vectorstore Sources Used")
                    for i, result in enumerate(search_results, 1):
                        with st.expander(f"📄 {result['source_file']} (relevance: {result['similarity_score']:.0%})"):
                            st.text(result['content'][:1000] + "..." if len(result['content']) > 1000 else result['content'])
                else:
                    st.info("💡 Answer generated using AI knowledge (no specific vectorstore matches found)")
    else:
        st.warning("Please enter a question.")
if __name__ == "__main__":
    main()