import sys
import os

os.environ["USE_OPENROUTER"] = "false"

from chatbot_engine import MultilingualChatbot


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def run_demo_tests():
    bot = MultilingualChatbot()
    sid = "demo"

    cases = [
        ("Hello, I want to book a train ticket", "book_ticket", "en"),
        ("मुझे दिल्ली जाना है", "book_ticket", "hi"),
        ("tomorrow evening", "book_ticket", "en"),
        ("¿Cuál es el clima en Madrid mañana?", "weather", "es"),
        ("Bonjour, je veux annuler ma réservation", "cancel", "fr"),
    ]

    for message, expected_intent, expected_language in cases:
        result = bot.reply(message, session_id=sid)
        assert result["intent"] == expected_intent, result
        assert result["language"] == expected_language, result
        print(f"PASS: {message} -> {result['language']} / {result['intent']}")
        print(f"      {result['reply']}")


if __name__ == "__main__":
    run_demo_tests()