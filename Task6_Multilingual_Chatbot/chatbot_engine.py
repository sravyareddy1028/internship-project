print("chatbot_engine loaded")
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from openrouter_client import OpenRouterClient


SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
}


LANGUAGE_HINTS = {
    "hi": {
        "devanagari": re.compile(r"[\u0900-\u097F]"),
        "words": {
            "namaste", "mujhe", "mera", "meri", "kya", "kaise", "kal", "aaj",
            "ticket", "madad", "chahiye", "jana", "delhi", "hai", "kripya",
            "dhanyavaad", "shukriya", "batao", "samjhao", "mausam",
        },
    },
    "es": {
        "words": {
            "hola", "gracias", "por", "favor", "quiero", "necesito", "boleto",
            "billete", "clima", "tiempo", "mañana", "hoy", "estado", "cancelar",
            "ayuda", "reservar", "viajar", "a", "desde",
        },
    },
    "fr": {
        "words": {
            "bonjour", "merci", "s'il", "vous", "plait", "veux", "besoin",
            "billet", "meteo", "météo", "demain", "aujourd'hui", "annuler",
            "aide", "réserver", "reserver", "voyager", "statut", "état", "etat",
        },
    },
    "en": {
        "words": {
            "hello", "hi", "thanks", "please", "want", "need", "ticket",
            "weather", "tomorrow", "today", "status", "cancel", "help", "book",
            "travel", "from", "to",
        },
    },
}


INTENT_KEYWORDS = {
    "greeting": {
        "hello", "hi", "hey", "namaste", "hola", "bonjour",
    },
    "thanks": {
        "thanks", "thank", "dhanyavaad", "shukriya", "gracias", "merci",
    },
    "book_ticket": {
        "book", "booking", "ticket", "train", "flight", "bus", "reserve",
        "reservar", "réserver", "reserver", "boleto", "billete", "viajar",
        "mujhe", "jana", "टिकट", "जाना", "बुक",
    },
    "weather": {
        "weather", "climate", "forecast", "mausam", "मौसम", "clima",
        "tiempo", "meteo", "météo",
    },
    "status": {
        "status", "track", "tracking", "estado", "statut", "état", "etat",
        "स्थिति", "batao",
    },
    "cancel": {
        "cancel", "cancelar", "annuler", "रद्द", "cancelation", "cancellation",
    },
}


ENTITY_PATTERNS = {
    "date": {
        "today": "today",
        "aaj": "today",
        "hoy": "today",
        "aujourd'hui": "today",
        "आज": "today",
        "tomorrow": "tomorrow",
        "kal": "tomorrow",
        "mañana": "tomorrow",
        "demain": "tomorrow",
        "कल": "tomorrow",
    },
    "time": {
        "morning": "morning",
        "subah": "morning",
        "mañana": "morning",
        "matin": "morning",
        "सुबह": "morning",
        "evening": "evening",
        "shaam": "evening",
        "tarde": "evening",
        "soir": "evening",
        "शाम": "evening",
        "night": "night",
        "raat": "night",
        "noche": "night",
        "nuit": "night",
        "रात": "night",
    },
}


KNOWN_PLACES = {
    "delhi": "Delhi",
    "mumbai": "Mumbai",
    "chennai": "Chennai",
    "bangalore": "Bangalore",
    "bengaluru": "Bangalore",
    "paris": "Paris",
    "madrid": "Madrid",
    "london": "London",
    "दिल्ली": "Delhi",
    "मुंबई": "Mumbai",
}


RESPONSE_TEXT = {
    "en": {
        "greeting": "Hello. I can continue in English, Hindi, Spanish, or French. How can I help?",
        "thanks": "You're welcome. I will keep the conversation context ready for your next message.",
        "book_complete": "Got it. I will look for a {mode} ticket from {origin} to {destination} for {date} in the {time}.",
        "book_missing": "I understood that you want to book a ticket. Please tell me {missing}.",
        "weather_complete": "I understood you want the weather for {destination} for {date}.",
        "weather_missing": "Which city should I check the weather for?",
        "status": "I understood you want to check status. Please share the booking or tracking ID.",
        "cancel": "I understood you want to cancel something. Please share the booking ID so I can continue.",
        "ambiguous": "I am not fully sure what you mean. Are you asking about booking, weather, status, or cancellation?",
        "continuity": "I updated the previous request: {summary}",
    },
    "hi": {
        "greeting": "नमस्ते। मैं हिंदी, अंग्रेज़ी, स्पेनिश और फ्रेंच में बातचीत जारी रख सकता हूँ। बताइए, कैसे मदद करूँ?",
        "thanks": "आपका स्वागत है। मैं आपकी बातचीत का संदर्भ याद रखूँगा।",
        "book_complete": "ठीक है। मैं {origin} से {destination} के लिए {date} {time} में {mode} टिकट खोजूंगा।",
        "book_missing": "मैं समझ गया कि आप टिकट बुक करना चाहते हैं। कृपया {missing} बताइए।",
        "weather_complete": "मैं समझ गया कि आपको {destination} का {date} का मौसम चाहिए।",
        "weather_missing": "किस शहर का मौसम देखना है?",
        "status": "मैं समझ गया कि आप स्टेटस देखना चाहते हैं। कृपया booking या tracking ID बताइए।",
        "cancel": "मैं समझ गया कि आप कुछ cancel करना चाहते हैं। कृपया booking ID बताइए।",
        "ambiguous": "मुझे पूरी तरह स्पष्ट नहीं हुआ। क्या आप booking, weather, status या cancellation के बारे में पूछ रहे हैं?",
        "continuity": "मैंने पिछले अनुरोध को अपडेट कर दिया: {summary}",
    },
    "es": {
        "greeting": "Hola. Puedo continuar en español, inglés, hindi o francés. ¿Cómo puedo ayudarte?",
        "thanks": "De nada. Mantendré el contexto de la conversación para tu siguiente mensaje.",
        "book_complete": "Entendido. Buscaré un boleto de {mode} de {origin} a {destination} para {date} en la {time}.",
        "book_missing": "Entendí que quieres reservar un boleto. Por favor dime {missing}.",
        "weather_complete": "Entendí que quieres el clima de {destination} para {date}.",
        "weather_missing": "¿De qué ciudad quieres consultar el clima?",
        "status": "Entendí que quieres revisar el estado. Comparte el ID de reserva o seguimiento.",
        "cancel": "Entendí que quieres cancelar algo. Comparte el ID de reserva para continuar.",
        "ambiguous": "No estoy completamente seguro. ¿Preguntas sobre reserva, clima, estado o cancelación?",
        "continuity": "Actualicé la solicitud anterior: {summary}",
    },
    "fr": {
        "greeting": "Bonjour. Je peux continuer en français, anglais, hindi ou espagnol. Comment puis-je aider ?",
        "thanks": "Avec plaisir. Je garderai le contexte de la conversation pour votre prochain message.",
        "book_complete": "Compris. Je vais chercher un billet de {mode} de {origin} à {destination} pour {date} en {time}.",
        "book_missing": "J'ai compris que vous voulez réserver un billet. Veuillez indiquer {missing}.",
        "weather_complete": "J'ai compris que vous voulez la météo de {destination} pour {date}.",
        "weather_missing": "Pour quelle ville voulez-vous la météo ?",
        "status": "J'ai compris que vous voulez vérifier le statut. Partagez l'ID de réservation ou de suivi.",
        "cancel": "J'ai compris que vous voulez annuler quelque chose. Partagez l'ID de réservation pour continuer.",
        "ambiguous": "Je ne suis pas totalement sûr. Parlez-vous de réservation, météo, statut ou annulation ?",
        "continuity": "J'ai mis à jour la demande précédente : {summary}",
    },
}


@dataclass
class ConversationState:
    preferred_language: str = "en"
    last_intent: Optional[str] = None
    entities: Dict[str, str] = field(default_factory=dict)
    history: List[Dict[str, object]] = field(default_factory=list)


class MultilingualChatbot:
    def __init__(self):
        self.sessions: Dict[str, ConversationState] = {}
        self.openrouter = OpenRouterClient()

    def reply(self, message: str, session_id: str = "default") -> Dict[str, object]:
        state = self.sessions.setdefault(session_id, ConversationState())
        detected, languages = self.detect_language(message, state.preferred_language)
        tokens = self._tokens(message)
        intent, confidence = self.detect_intent(message, tokens, state.last_intent)
        entities = self.extract_entities(message, tokens)

        if detected in SUPPORTED_LANGUAGES:
            state.preferred_language = detected

        if intent == "follow_up" and state.last_intent:
            intent = state.last_intent

        if intent:
            state.last_intent = intent
        state.entities.update({k: v for k, v in entities.items() if v})

        fallback_response = self._build_response(state, intent, confidence, state.preferred_language)
        response, engine = self._generate_response(
            state=state,
            user_message=message,
            detected_language=detected,
            languages=languages,
            intent=intent,
            confidence=confidence,
            fallback_response=fallback_response,
        )
        state.history.append(
            {
                "user": message,
                "language": detected,
                "languages": sorted(languages),
                "intent": intent,
                "entities": dict(state.entities),
                "bot": response,
                "engine": engine,
            }
        )

        return {
            "reply": response,
            "engine": engine,
            "language": detected,
            "language_name": SUPPORTED_LANGUAGES.get(detected, "Unknown"),
            "languages_in_message": sorted(languages),
            "intent": intent or "ambiguous",
            "confidence": confidence,
            "context": {
                "last_intent": state.last_intent,
                "entities": dict(state.entities),
                "turns": len(state.history),
            },
        }

    def _generate_response(
        self,
        state: ConversationState,
        user_message: str,
        detected_language: str,
        languages: Set[str],
        intent: Optional[str],
        confidence: float,
        fallback_response: str,
    ) -> Tuple[str, str]:
        if not self.openrouter.enabled:
            return fallback_response, "offline"

        try:
            messages = self._openrouter_messages(
                state=state,
                user_message=user_message,
                detected_language=detected_language,
                languages=languages,
                intent=intent,
                confidence=confidence,
                fallback_response=fallback_response,
            )
            return self.openrouter.chat(messages), "openrouter"
        except RuntimeError as exc:
            return f"{fallback_response}\n\n[OpenRouter fallback: {exc}]", "offline-fallback"

    def _openrouter_messages(
        self,
        state: ConversationState,
        user_message: str,
        detected_language: str,
        languages: Set[str],
        intent: Optional[str],
        confidence: float,
        fallback_response: str,
    ) -> List[Dict[str, str]]:
        recent_turns = state.history[-6:]
        history_lines = []
        for turn in recent_turns:
            history_lines.append(f"User: {turn['user']}")
            history_lines.append(f"Assistant: {turn['bot']}")

        context = {
            "detected_language": detected_language,
            "languages_in_message": sorted(languages),
            "preferred_language": state.preferred_language,
            "intent": intent or "ambiguous",
            "confidence": confidence,
            "entities": state.entities,
            "offline_response": fallback_response,
        }

        system_prompt = (
            "You are a multilingual internship chatbot. Continue the conversation in the "
            "user's current language unless the user clearly asks for another language. "
            "Support English, Hindi, Spanish, and French. Handle mixed-language input, "
            "preserve previous context, resolve ambiguity with a short clarification, "
            "and keep the response concise. Do not claim to complete real bookings, "
            "payments, or cancellations; say what information is needed or what you would do next."
        )

        user_prompt = (
            "Conversation history:\n"
            + ("\n".join(history_lines) if history_lines else "No previous turns.")
            + "\n\nCurrent analysis JSON:\n"
            + json_dumps(context)
            + "\n\nCurrent user message:\n"
            + user_message
        )

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def detect_language(self, message: str, fallback: str) -> Tuple[str, Set[str]]:
        lowered = message.lower()
        tokens = set(self._tokens(lowered))
        scores = {code: 0 for code in SUPPORTED_LANGUAGES}

        if LANGUAGE_HINTS["hi"]["devanagari"].search(message):
            scores["hi"] += 4

        for code, hints in LANGUAGE_HINTS.items():
            scores[code] += len(tokens & hints.get("words", set()))

        languages = {code for code, score in scores.items() if score > 0}
        if not languages:
            return fallback, {fallback}

        detected = max(scores, key=scores.get)
        return detected, languages

    def detect_intent(self, message: str, tokens: List[str], last_intent: Optional[str]) -> Tuple[Optional[str], float]:
        normalized_tokens = set(tokens)
        scores = {
            intent: len(normalized_tokens & keywords)
            for intent, keywords in INTENT_KEYWORDS.items()
        }

        if re.search(r"[\u0900-\u097F]", message):
            if any(word in message for word in ("टिकट", "जाना", "बुक")):
                scores["book_ticket"] += 2
            if "मौसम" in message:
                scores["weather"] += 2
            if "रद्द" in message:
                scores["cancel"] += 2

        priority = ["cancel", "status", "weather", "book_ticket", "thanks", "greeting"]
        best_intent = max(priority, key=lambda name: scores[name])
        best_score = scores[best_intent]

        if best_score == 0 and last_intent and self.extract_entities(message, tokens):
            return "follow_up", 0.55
        if best_score == 0:
            return None, 0.0

        confidence = min(0.98, 0.45 + best_score * 0.18)
        return best_intent, round(confidence, 2)

    def extract_entities(self, message: str, tokens: List[str]) -> Dict[str, str]:
        entities: Dict[str, str] = {}
        lowered = message.lower()
        token_set = set(tokens)

        for raw, value in KNOWN_PLACES.items():
            if raw in lowered:
                if re.search(rf"\b(from|desde|de)\s+{re.escape(raw)}\b", lowered):
                    entities["origin"] = value
                elif re.search(rf"\b(to|a|à)\s+{re.escape(raw)}\b", lowered):
                    entities["destination"] = value
                elif "destination" not in entities:
                    entities["destination"] = value

        for key, mappings in ENTITY_PATTERNS.items():
            for raw, value in mappings.items():
                if raw in token_set or raw in lowered:
                    entities[key] = value

        if "flight" in token_set:
            entities["mode"] = "flight"
        elif "train" in token_set:
            entities["mode"] = "train"
        elif "bus" in token_set:
            entities["mode"] = "bus"
        elif any(word in token_set for word in ("boleto", "billete", "ticket")):
            entities.setdefault("mode", "travel")

        return entities

    def _build_response(self, state: ConversationState, intent: Optional[str], confidence: float, lang: str) -> str:
        text = RESPONSE_TEXT.get(lang, RESPONSE_TEXT["en"])
        entities = state.entities

        if intent == "greeting":
            return text["greeting"]
        if intent == "thanks":
            return text["thanks"]
        if intent == "status":
            return text["status"]
        if intent == "cancel":
            return text["cancel"]
        if intent == "weather":
            if entities.get("destination"):
                return text["weather_complete"].format(
                    destination=entities.get("destination"),
                    date=entities.get("date", "today"),
                )
            return text["weather_missing"]
        if intent == "book_ticket":
            missing = self._missing_booking_fields(entities)
            if not missing:
                return text["book_complete"].format(
                    mode=entities.get("mode", "travel"),
                    origin=entities.get("origin", "your origin"),
                    destination=entities.get("destination", "your destination"),
                    date=entities.get("date", "your selected date"),
                    time=entities.get("time", "preferred time"),
                )
            return text["book_missing"].format(missing=", ".join(missing))

        if state.last_intent and confidence >= 0.5:
            return text["continuity"].format(summary=self._summary(state))
        return text["ambiguous"]

    def _missing_booking_fields(self, entities: Dict[str, str]) -> List[str]:
        missing = []
        if "destination" not in entities:
            missing.append("destination")
        if "date" not in entities:
            missing.append("date")
        if "time" not in entities:
            missing.append("time")
        return missing

    def _summary(self, state: ConversationState) -> str:
        parts = [f"intent={state.last_intent}"]
        parts.extend(f"{key}={value}" for key, value in state.entities.items())
        return ", ".join(parts)

    def _tokens(self, message: str) -> List[str]:
        return re.findall(r"[\w\u0900-\u097F']+", message.lower(), flags=re.UNICODE)


def json_dumps(data: Dict[str, object]) -> str:
    import json

    return json.dumps(data, ensure_ascii=False, indent=2)