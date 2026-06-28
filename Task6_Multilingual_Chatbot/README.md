# Multilingual Context-Aware Chatbot

This is a fresh internship prototype that demonstrates multilingual chatbot behavior across English plus three additional languages: Hindi, Spanish, and French.

## Features

- Automatic language detection for English, Hindi, Spanish, and French.
- Mixed-language support using language hints and Unicode script detection.
- Intent detection for greeting, ticket booking, weather, status checking, cancellation, and thanks.
- Context memory using a session ID, so follow-up messages can update previous intent and entities.
- Language switching inside the same conversation.
- Browser-based chat UI with live language, intent, confidence, and turn count.
- Dependency-free Python backend using only the standard library.
- Optional OpenRouter API mode for stronger online multilingual reasoning.

## Run

```powershell
cd C:\you  folder/multilingual_chatbot
python app.py

Open:

```text
http://127.0.0.1:8000
```

## OpenRouter Online Mode

### Option 1: Enter the key in the app

1. Start the app.
2. Open `http://127.0.0.1:8000`.
3. Paste your OpenRouter key into the OpenRouter API section.
4. Keep the model as `openrouter/auto` or enter another OpenRouter model ID.
5. Click `Save API Key`.
The app saves the key to a local `.env` file and uses OpenRouter for the next message.
```text
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_MODEL=openrouter/auto
```

4. Start the app again:

```powershell
python app.py
```

When the key is present, the app calls OpenRouter's OpenAI-compatible chat completions API:

```text
https://openrouter.ai/api/v1/chat/completions
```

If the internet is unavailable or the key/model is wrong, the app automatically falls back to the offline rule-based response.


## Demo Conversation

```text
User: Hello, I want to book a train ticket
Bot: I understood that you want to book a ticket. Please tell me destination, date, time.

User: मुझे दिल्ली जाना है
Bot: मैं समझ गया कि आप टिकट बुक करना चाहते हैं। कृपया date, time बताइए।

User: tomorrow evening
Bot: Got it. I will look for a train ticket from your origin to Delhi for tomorrow in the evening.

User: ¿Cuál es el clima en Madrid mañana?
Bot: Entendí que quieres el clima de Madrid para tomorrow.

User: Bonjour, je veux annuler ma réservation
Bot: J'ai compris que vous voulez annuler quelque chose. Partagez l'ID de réservation pour continuer.
```

## How It Works

The chatbot follows this pipeline:

```text
User message
  -> language detection
  -> intent detection
  -> entity extraction
  -> conversation state update
  -> response generation in detected language
```

The internal memory stores:

- preferred language
- last intent
- extracted entities such as destination, date, time, and travel mode
- full conversation history

## Suggested Report Points

- The system supports cross-lingual continuity because the same memory object is updated regardless of input language.
- Ambiguous follow-up messages reuse the previous intent when they contain useful entities.
- Mixed-language messages are handled through script detection and keyword matching.
- The prototype uses open-source-friendly architecture and can later be upgraded with `fastText`, `sentence-transformers`, Rasa, MarianMT, mBART, or NLLB.