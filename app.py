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
        """Initialize the CloudOps Assistant"""
        self.index = None
        self.chunks = None
        self.metadata = None
        self.embedding_model = None
        self._auto_load_database()
    
    def _auto_load_database(self):
        """Automatically load vector database on startup"""
        
        try:
            required_files = [FAISS_INDEX_FILE, CHUNKS_FILE, METADATA_FILE]
            if not all(os.path.exists(f) for f in required_files):
                st.error("Vector database not found! Please run the index builder first.")
                st.info("Run: `python build_index.py` to create the knowledge base")
                return False
            
            self.index = faiss.read_index(FAISS_INDEX_FILE)
            
            with open(CHUNKS_FILE, 'rb') as f:
                self.chunks = pickle.load(f)
            
            with open(METADATA_FILE, 'r') as f:
                self.metadata = json.load(f)
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error loading vector database: {e}")
            return False
            
       
    
    @st.cache_resource
    def get_embedding_model(_self):
        """Load embedding model (cached for performance)"""
        if _self.embedding_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                model_name = _self.metadata.get('model_name', 'sentence-transformers/all-MiniLM-L6-v2')
                _self.embedding_model = SentenceTransformer(model_name)
            except ImportError:
                st.error("❌ sentence-transformers not installed!")
                st.info("Install with: `pip install sentence-transformers`")
                return None
        return _self.embedding_model
    
    def search_knowledge_base(self, query, top_k=3):
        """Search for relevant CloudOps knowledge"""
        if not self.index or not self.chunks:
            return []
        
        # Get embedding model
        model = self.get_embedding_model()
        if model is None:
            return []
        
        try:
            query_embedding = model.encode([query]).astype('float32')
            
            distances, indices = self.index.search(query_embedding, min(top_k, len(self.chunks)))
            
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.chunks):
                    chunk = self.chunks[idx]
                    results.append({
                        'rank': i + 1,
                        'source_file': chunk['source_file'],
                        'content': chunk['content'],
                        'similarity_score': 1 / (1 + distance)
                    })
            
            return results
            
        except Exception as e:
            st.error(f"❌ Search error: {e}")
            return []
    
    def generate_cloudops_answer(self, query, context_chunks):
        """Generate CloudOps-focused answer using OpenRouter"""
        if not OPENROUTER_API_KEY:
            st.error("OPENROUTER_API_KEY not found in environment variables!")
            st.info("Add OPENROUTER_API_KEY to your .env file")
            return None
        
        try:
            context_parts = []
            for chunk in context_chunks:
                context_parts.append(f"📄 {chunk['source_file']}:\n{chunk['content']}\n")
            
            context = "\n".join(context_parts)
            
            # Create CloudOps-focused prompt
            user_prompt = f"""Context from CloudOps knowledge base:
{context}

CloudOps Question: {query}

Please provide a practical answer focused on Cloud & DevOps engineering. Include specific commands, configurations, or best practices where applicable."""
            
            # API request
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
                "max_tokens": 750,
                "temperature": 0.1
            }
            
            response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                return answer
            else:
                # Fallback to basic response if API fails
                st.warning(f"API temporarily unavailable. Showing context-based response.")
                return self._generate_fallback_answer(query, context_chunks)
                
        except requests.exceptions.Timeout:
            st.warning("Response timeout. Showing context-based response.")
            return self._generate_fallback_answer(query, context_chunks)
        except Exception as e:
            st.warning(f"API error: {str(e)[:100]}... Showing context-based response.")
            return self._generate_fallback_answer(query, context_chunks)
    
    def _generate_fallback_answer(self, query, context_chunks):
        """Generate a simple fallback answer when API is unavailable"""
        if not context_chunks:
            return f"I found information related to '{query}' but couldn't generate a comprehensive answer. Please check the retrieved context below for relevant details."
        
        # Simple context summary
        sources = [chunk['source_file'] for chunk in context_chunks]
        return f"""Based on the available CloudOps documentation, I found relevant information in: {', '.join(sources)}.

For detailed information about '{query}', please refer to the context sections below. The documentation covers practical aspects of Cloud & DevOps engineering including Kubernetes, Docker, infrastructure management, and best practices.

*Note: Full AI response temporarily unavailable - showing context-based results.*"""

def main():
    """Main Streamlit app"""
    
    st.set_page_config(
        page_title="☁️ CloudOps Assistant",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"  
    )
    
    # Header
    st.title("☁️ CloudOps Assistant")
    st.markdown("*Your AI assistant for Kubernetes, Docker, Cloud Infrastructure & DevOps* 🚀")
    
    assistant = CloudOpsAssistant()
    
    if not assistant.index:
        st.error(" Knowledge base not loaded!")
        st.info(" Please run `python build_index.py` first to create the CloudOps cache files")
        st.stop()
    
    st.subheader("💬 Ask CloudOps Questions")
    
    example_questions = [
        "How to deploy a Pod in Kubernetes?",
        "Docker best practices for production",
        "Kubernetes troubleshooting guide",
        "Git branching strategies"
    ]
    
    st.markdown("**💡 Example questions:**")
    cols = st.columns(3)
    for i, question in enumerate(example_questions):
        with cols[i % 3]:
            if st.button(question, key=f"example_{i}", help="Click to use this question"):
                st.session_state.query = question
    
    # Query input
    query = st.text_area(
        "**Your CloudOps question:**",
        value=st.session_state.get('query', ''),
        placeholder="e.g., How do I create a Kubernetes deployment with health checks?",
        height=100,
        key="query_input"
    )
    
    # Search button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        search_clicked = st.button("🔍 Ask CloudOps AI", type="primary")
    with col2:
        if st.button("🗑️ Clear", type="secondary"):
            st.session_state.query = ""
            st.rerun()
    
    # Process query
    if search_clicked and query.strip():
        with st.spinner("🔍 Searching CloudOps knowledge base..."):
            # Search for relevant content
            search_results = assistant.search_knowledge_base(query, top_k=3)
            
            if not search_results:
                st.warning("❌ No relevant information found in the knowledge base.")
                st.info("💡 Try rephrasing your question or ask about Kubernetes, Docker, Cloud, or DevOps topics.")
            else:
                # Generate answer
                with st.spinner("🤖 Generating CloudOps answer..."):
                    answer = assistant.generate_cloudops_answer(query, search_results)
                
                if answer:
                    # Display answer
                    st.subheader("🎯 CloudOps Answer")
                    st.markdown(answer)
                    
                    # Show sources
                    st.subheader("📚 Knowledge Sources")
                    for i, result in enumerate(search_results, 1):
                        with st.expander(f"📄 Source {i}: {result['source_file']} (relevance: {result['similarity_score']:.1%})"):
                            st.code(result['content'][:800] + "..." if len(result['content']) > 800 else result['content'])
                    
                    st.caption(f"*Powered by {OPENROUTER_MODEL} • {len(search_results)} sources used*")
    
    elif search_clicked and not query.strip():
        st.warning("⚠️ Please enter a CloudOps question!")
    
    # Footer
    st.divider()
    
    # Help section (collapsible)
    with st.expander("❓ Help & Tips"):
        st.markdown("""
        **🎯 What can I help you with?**
        - 🚀 **Kubernetes**: Pods, Services, Deployments, Ingress, ConfigMaps
        - 🐳 **Docker**: Containerization, Dockerfile best practices, multi-stage builds
        - ☁️ **Cloud Infrastructure**: AWS, Azure, GCP services and configurations
        - 🔧 **DevOps Tools**: Git, GitHub Actions
        - 🔒 **Security**: Container security, cloud security best practices
        
        **💡 Tips for better answers:**
        - Be specific about your use case
        - Mention the technology stack you're using
        - Include error messages if troubleshooting
        - Ask about best practices and real-world scenarios
        
        **🔧 Technical Details:**
        - Semantic search across CloudOps documentation
        - AI-powered responses with source attribution
        - Optimized for practical, actionable advice
        """)

if __name__ == "__main__":
    main()