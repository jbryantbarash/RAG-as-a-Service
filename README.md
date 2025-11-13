# RAG-as-a-Service

A lightweight, production-ready Retrieval-Augmented Generation (RAG) application built with:

- OpenAI Responses API  
- OpenAI Vector Stores (`file_search`)  
- Streamlit UI  

Upload documents, index them into a vector store, and ask questions — all in less than 100 lines of code.

---

## 🚀 Features
- Upload & index PDFs, text files, docs
- OpenAI vector-store-based RAG
- Fully serverless: no database required
- Choose between `gpt-5-mini` and `gpt-5-pro`
- Minimal deployment footprint (Streamlit app)

---

## ✅ Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/rag-openai.git
cd rag-openai

2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Add your OpenAI API key

Create .env from the example:

cp .env.example .env

Edit .env and add:

OPENAI_API_KEY=sk-proj-xxxxxxx

5. Run the app
streamlit run app.py
