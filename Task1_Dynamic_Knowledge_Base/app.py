import json
import streamlit as st

from src.embeddings import create_embeddings
from src.vector_store import VectorStore
from src.chatbot import get_query_embedding

st.set_page_config(page_title="Dynamic Knowledge Base Chatbot")

st.title("🤖 Dynamic Knowledge Base Chatbot")

with open("data/articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

texts = [article["summary"] for article in articles]

embeddings = create_embeddings(texts)

vector_db = VectorStore(embeddings)

query = st.text_input("Ask a question:")

if query:
    query_embedding = get_query_embedding(query)

    indices = vector_db.search(query_embedding)

    st.subheader("Top Results")

    for idx in indices:
        st.write("### " + articles[idx]["title"])
        st.write(articles[idx]["summary"])
        st.write("---")