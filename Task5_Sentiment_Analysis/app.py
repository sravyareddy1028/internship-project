import streamlit as st
import nltk
import random
from nltk.sentiment import SentimentIntensityAnalyzer

# ----------------------------
# Download VADER Lexicon
# ----------------------------
nltk.download("vader_lexicon", quiet=True)

# Initialize analyzer
sia = SentimentIntensityAnalyzer()

# ----------------------------
# Response Collections
# ----------------------------
positive_responses = [
    "That's wonderful to hear! 😊",
    "I'm delighted you're having a positive experience!",
    "Great news! Thanks for sharing.",
    "I'm glad things are going well for you."
]

negative_responses = [
    "I'm sorry you're experiencing that. Let's work through it together.",
    "I understand your concern. Could you tell me more?",
    "That sounds frustrating. I'm here to help.",
    "Thank you for sharing your concern. Let's find a solution."
]

neutral_responses = [
    "I hear you. Could you tell me more so I can assist better?",
    "Thanks for sharing. What would you like me to do for you?",
    "I understand. Would you like advice or support?",
    "I'm here to help. Please explain a bit more."
]

mixed_responses = [
    "It sounds like you're experiencing mixed emotions. That's completely normal. 💙",
    "I can see you're feeling both positive and negative emotions. Would you like to talk more about it?",
    "Mixed feelings can happen sometimes. I'm here to listen."
]

advice_responses = [
    "Try getting enough sleep 😴 and exercising regularly 🏃.",
    "Spending time with loved ones ❤️ can help improve mood.",
    "Practicing gratitude 🙏 often helps improve emotional wellbeing.",
    "Listening to music 🎶 or journaling your thoughts can help you feel better.",
    "Meditation 🧘 and deep breathing can calm your mind.",
    "Going for a walk 🚶 in nature often lifts spirits.",
    "Talking to a trusted friend 👥 can ease sadness.",
    "Setting small goals 🎯 and achieving them boosts motivation."
]

# ----------------------------
# Custom Sentiment Rules
# ----------------------------
def custom_sentiment(message):

    msg = message.lower().strip()

    # Advice/help requests should be neutral
    if any(word in msg for word in [
        "suggest", "advice", "tips","guide",
        "recommend", "ways to","assist","support",
        "how can i", "help"
    ]):
        return "NEUTRAL", "LOW", 0.0

    # Mixed emotions
    if (
        ("happy" in msg or "good" in msg)
        and
        ("sad" in msg or "bad" in msg or "upset" in msg)
    ):
        return "MIXED", "MEDIUM", 0.0

    neutral_phrases = [
        "i am okay",
        "i'm okay",
        "i am fine",
        "i'm fine",
        "i am not sad",
        "i'm not sad"
    ]

    positive_phrases = [
        "i am very happy",
        "i'm very happy",
        "i am so happy",
        "i'm so happy"
    ]

    negative_phrases = [
        "i am not happy",
        "i'm not happy",
        "i am upset",
        "i'm upset",
        "i feel bad",
        "i am sad",
        "i'm sad",
        "poor service",
        "bad experience"
    ]

    if any(p in msg for p in neutral_phrases):
        return "NEUTRAL", "LOW", 0.0

    if any(p in msg for p in positive_phrases):
        return "POSITIVE", "HIGH", 0.9

    if any(p in msg for p in negative_phrases):
        return "NEGATIVE", "HIGH", -0.9

    return None

# ----------------------------
# Sentiment Analysis
# ----------------------------
def analyze_sentiment(message):

    custom_result = custom_sentiment(message)

    if custom_result:
        return custom_result

    scores = sia.polarity_scores(message)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "POSITIVE"
    elif compound <= -0.05:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    abs_score = abs(compound)

    if abs_score >= 0.75:
        intensity = "HIGH"
    elif abs_score >= 0.30:
        intensity = "MEDIUM"
    else:
        intensity = "LOW"

    return sentiment, intensity, compound

# ----------------------------
# Intent Detection
# ----------------------------
def detect_intent(message):

    msg = message.lower()

    if any(word in msg for word in ["hi", "hello", "hey"]):
        return "GREETING"

    elif any(word in msg for word in [
        "issue", "problem", "error",
        "refund", "complaint",
        "poor service", "bad experience",
        "frustrated", "angry"
    ]):
        return "COMPLAINT"

    elif any(word in msg for word in [
        "help", "assist", "support"
    ]):
        return "HELP"

    elif any(word in msg for word in [
        "suggest", "advice", "tips",
        "recommend", "ways to"
    ]):
        return "ADVICE"

    elif any(word in msg for word in [
        "bye", "goodbye", "see you"
    ]):
        return "FAREWELL"

    elif any(word in msg for word in [
        "thank", "thanks"
    ]):
        return "THANKS"

    elif "?" in msg:
        return "QUESTION"

    return "GENERAL"

# ----------------------------
# Response Generator
# ----------------------------
def generate_response(sentiment, intensity, intent):

    escalation = False

    if intent == "GREETING":
        return "Hello! 😊 Welcome. How can I assist you today?", False

    if intent == "FAREWELL":
        return "Goodbye! 👋 Have a wonderful day ahead.", False

    if intent == "HELP":
        return "I'd be happy to help 😊. Please tell me more about your issue.", False

    if intent == "ADVICE":
        return random.choice(advice_responses), False

    if intent == "QUESTION":
        return "That's a good question 🤔. I'll do my best to help you.", False

    if intent == "THANKS":
        return "You're welcome! 😊 I'm glad I could help.", False

    if intent == "COMPLAINT":
        escalation = True
        return (
            "I'm sorry for the inconvenience. "
            "I understand your frustration and will do my best to help resolve the issue."
        ), escalation

    # General responses

    if sentiment == "POSITIVE":
        return random.choice(positive_responses), False

    if sentiment == "NEGATIVE":

        if intensity == "HIGH":
            escalation = True

        return random.choice(negative_responses), escalation

    if sentiment == "MIXED":
        return random.choice(mixed_responses), False

    return random.choice(neutral_responses), False

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(
    page_title="Sentiment-Aware Customer Support Chatbot",
    page_icon="🤖"
)

st.title("🤖 Sentiment-Aware Customer Support Chatbot")

st.write(
    "This chatbot detects sentiment (Positive, Negative, Neutral), "
    "understands intent, and adapts responses to improve customer satisfaction."
)

# ----------------------------
# Session State
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "ratings" not in st.session_state:
    st.session_state.ratings = []

if "escalations" not in st.session_state:
    st.session_state.escalations = 0

# ----------------------------
# User Input
# ----------------------------
user_input = st.text_input("Enter your message:")

if user_input:

    sentiment, intensity, score = analyze_sentiment(user_input)

    intent = detect_intent(user_input)

    response, escalation = generate_response(
        sentiment,
        intensity,
        intent
    )

    if escalation:
        st.session_state.escalations += 1

    st.session_state.history.append(
        (
            user_input,
            sentiment,
            intensity,
            score,
            intent,
            response
        )
    )

    st.subheader("Analysis")
    st.success(f"Sentiment: {sentiment}")
    st.info(f"Intensity: {intensity}")
    st.write(f"Sentiment Score: {score:.2f}")
    st.write(f"Intent: {intent}")

    st.subheader("Chatbot Response")
    st.write(response)

    if escalation:
        st.error(
            "⚠ High negative sentiment detected. "
            "Recommend escalation to a human support agent."
        )

# ----------------------------
# Customer Satisfaction
# ----------------------------
st.subheader("⭐ Customer Satisfaction")

rating = st.slider(
    "Rate this response (1 = poor, 5 = excellent)",
    1,
    5,
    3
)

if st.button("Submit Rating"):
    st.session_state.ratings.append(rating)

if st.session_state.ratings:

    avg_rating = (
        sum(st.session_state.ratings)
        / len(st.session_state.ratings)
    )

    st.metric(
        "Average Customer Rating",
        f"{avg_rating:.2f}/5"
    )

# ----------------------------
# Evaluation Metrics
# ----------------------------
st.subheader("📊 Evaluation Metrics")

st.write(
    f"Total Conversations: {len(st.session_state.history)}"
)

st.write(
    f"Escalations Triggered: {st.session_state.escalations}"
)

# ----------------------------
# Conversation History
# ----------------------------
st.subheader("📜 Conversation History")

for (
    msg,
    sentiment,
    intensity,
    score,
    intent,
    response
) in reversed(st.session_state.history):

    st.write(f"**You:** {msg}")
    st.write(f"**Sentiment:** {sentiment}")
    st.write(f"**Intensity:** {intensity}")
    st.write(f"**Score:** {score:.2f}")
    st.write(f"**Intent:** {intent}")
    st.write(f"**Bot:** {response}")
    st.write("---")