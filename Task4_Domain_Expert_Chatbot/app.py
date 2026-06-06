import streamlit as st
from src.data_loader import load_data
from src.embedding import create_embeddings
from src.retriever import Retriever
from src.chatbot import get_query_embedding

st.set_page_config(page_title="ArXiv Expert Chatbot", layout="wide")

st.title("📚 ArXiv Expert Chatbot")
st.write("Ask any research topic and get relevant arXiv papers instantly.")

@st.cache_data
def initialize():
    df = load_data()
    embeddings = create_embeddings(df["summary"].tolist())
    retriever = Retriever(embeddings)
    return df, retriever

df, retriever = initialize()

query = st.text_input("🔍 Enter your research question:")

if query:
    with st.spinner("Searching relevant papers..."):
        query_embedding = get_query_embedding(query)
        indices = retriever.search(query_embedding)

    st.subheader("📌 Top Results")

    for i, idx in enumerate(indices):
        st.markdown(f"### {i+1}. {df.iloc[idx]['title']}")
        st.write(df.iloc[idx]["summary"])
        st.markdown("---")