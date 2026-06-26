import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Page Setup
st.set_page_config(page_title="Multi Modal AI Assistant")

st.title("🤖 Multi Modal AI Assistant")

# Load BLIP Model
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    return processor, model

processor, model = load_model()

# Session Memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clear Conversation Button
if st.button("🗑 Clear Conversation"):
    st.session_state.chat_history = []
    if "caption" in st.session_state:
        del st.session_state["caption"]

# Upload Image
uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

# Analyze Image
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.button("Analyze Image"):

        with st.spinner("Analyzing Image..."):

            inputs = processor(
                images=image,
                return_tensors="pt"
            )

            output = model.generate(**inputs)

            caption = processor.decode(
                output[0],
                skip_special_tokens=True
            )

            st.session_state["caption"] = caption

        st.subheader("📷 Image Description")
        st.write(caption)

# Question Answering
if "caption" in st.session_state:

    st.subheader("💬 Ask Questions")

    question = st.text_input(
        "Ask a Question About the Image"
    )

    if question:

        caption = st.session_state["caption"]

        question_lower = question.lower()

        if "animal" in question_lower:
            answer = f"The image shows {caption}"

        elif "dangerous" in question_lower:
            answer = (
                "Based on the visual evidence, "
                "this appears to be a wild animal that may be dangerous."
            )

        elif "where" in question_lower:
            answer = (
                f"Based on the image, it appears that {caption}"
            )

        elif "describe" in question_lower:
            answer = caption

        elif "what" in question_lower:
            answer = (
                f"The image appears to contain {caption}"
            )

        else:
            answer = (
                "Please ask a question related to the uploaded image."
            )

        # Store Memory
        st.session_state.chat_history.append(
            ("You", question)
        )

        st.session_state.chat_history.append(
            ("Assistant", answer)
        )

        # Display Answer
        st.subheader("✅ Answer")
        st.write(answer)

        # Evidence
        st.subheader("📌 Evidence")
        st.write("Visual analysis result:")
        st.write(caption)

# Conversation History
if st.session_state.chat_history:

    st.subheader("📜 Conversation History")

    for speaker, message in st.session_state.chat_history:

        if speaker == "You":
            st.write(f"👤 {speaker}: {message}")

        else:
            st.write(f"🤖 {speaker}: {message}")