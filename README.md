# CloudOps Assistant

This project is a **CloudOps Assistant** powered by **open-source LLMs** and **vector search (FAISS)**. It allows users to query system or cloud documentation stored in `.md` files. The assistant embeds documents, stores them in a FAISS index, and uses an LLM (via OpenRouter API) to provide meaningful responses to natural language queries.

The goal is to demonstrate **real-world impact** by combining AI, vector databases, and cloud-friendly deployment — all while using **free and open-source tools**.

### 🔗 [Live App on Render](https://cloudopsai.onrender.com)

## 🚀 Features

* Load your `.md` documents into a FAISS vector store
* Generate embeddings with `sentence-transformers/all-MiniLM-L6-v2`
* Query your docs with natural language
* Uses **OpenRouter free LLMs** (`openai/gpt-oss-20b`) for answering queries
* Lightweight → suitable for deployment on cloud platforms
* **Deployed on Render** for seamless cloud access

## 🛠️ Tech Stack

* **Python**
* **Sentence Transformers** (for embeddings)
* **FAISS** (for similarity search)
* **OpenRouter API** (for LLM responses)
* **Markdown Docs** as your knowledge base
* **Render** (for deployment)

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/gv-1280/CloudOps-Assistant.git
cd CloudOps-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your docs
Place all your `.md` files inside the `docs/` folder.

### 5. Generate embeddings

```bash
python embeddings.py
```

This will create:
* `faiss_index.idx` → vector index of your docs
* `doc_mapping.pkl` → mapping of docs to vectors

### 6. Run the assistant

```bash
python app.py
```

This starts the assistant, allowing you to query your docs via terminal or API.

## 🌐 Deployment

* **Deployed on Render** for production use
* Works seamlessly on the cloud since it uses **OpenRouter API** instead of heavy local models
* Can also be deployed on **Streamlit Cloud** or **Railway** for alternative hosting options

## 📄 License

This project is licensed under the **MIT License**.

## 📚 References

### Kubernetes
* [Kubernetes Official Documentation](https://kubernetes.io/docs/)
* [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

### Docker
* [Docker Official Documentation](https://docs.docker.com/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)

### Git & GitHub
* [Git Official Documentation](https://git-scm.com/doc)
* [GitHub Documentation](https://docs.github.com/)
* [GitHub CLI Manual](https://cli.github.com/manual/)
* [Pro Git Book](https://git-scm.com/book)
* [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)