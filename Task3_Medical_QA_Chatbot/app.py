import streamlit as st
import chatbot_v3

st.set_page_config(
    page_title="Medical Information Assistant",
    page_icon="🩺"
)

st.title("🩺 Medical Information Assistant")

st.success("Medical Q&A Chatbot using MedQuAD Dataset")

st.warning(
    "This chatbot provides information from the MedQuAD dataset. "
    "It is for educational purposes only and is not a substitute "
    "for professional medical advice."
)

user_input = st.text_input(
    "Enter a disease or symptom:"
)

if user_input:

    response = chatbot_v3.get_response(user_input)

    st.subheader("Result")
    st.write(response)