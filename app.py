import os, streamlit as st
from openai import OpenAI

st.set_page_config(page_title="RAG-as-a-Service (OpenAI)", layout="centered")
st.title("RAG-as-a-Service (OpenAI)")

# 1) Client + Vector Store bootstrap
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if "vs_id" not in st.session_state:
    st.session_state.vs_id = client.vector_stores.create(name="rag-store").id  # creates once

# 2) Uploader → add files to Vector Store
files = st.file_uploader("Upload PDFs/Docs", accept_multiple_files=True)
if files:
    with st.spinner("Indexing…"):
        uploaded_ids = []
        for f in files:
            up = client.files.create(file=(f.name, f.read()), purpose="assistants")
            uploaded_ids.append(up.id)
        for fid in uploaded_ids:
            client.vector_stores.files.create(vector_store_id=st.session_state.vs_id, file_id=fid)
    st.success(f"Added {len(files)} file(s) to your knowledge base.")

# 3) Ask questions over your docs
q = st.text_input("Ask a question about your documents")
model = st.selectbox("Model", ["gpt-5-mini", "gpt-5-pro"], index=0)
if st.button("Search & Answer") and q:
    with st.spinner("Thinking…"):
        resp = client.responses.create(
            model=model,
            instructions="Answer using the provided documents; cite filenames inline when useful.",
            tools=[{"type": "file_search", "vector_store_ids": [st.session_state.vs_id]}],
            input=[{"role": "user", "content": q}],
        )
    st.markdown(resp.output_text or "No text output.")

    # Optional: show which files were used (best-effort)
    used = []
    try:
        for item in getattr(resp, "output", []) or []:
            for c in getattr(item, "content", []) or []:
                if getattr(c, "type", "") == "tool_result" and getattr(c, "tool_name", "") == "file_search":
                    for r in getattr(c, "results", []) or []:
                        if hasattr(r, "file_name"):
                            used.append(r.file_name)
    except Exception:
        pass
    if used:
        st.caption("Sources: " + ", ".join(dict.fromkeys(used)))
