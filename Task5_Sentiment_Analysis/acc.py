from app import analyze_sentiment, detect_intent, generate_response

# Define test dataset: (input, expected sentiment)
test_cases = [
    ("I love this service", "POSITIVE"),
    ("Thank you so much", "POSITIVE"),
    ("This is excellent", "POSITIVE"),
    ("I am very happy", "POSITIVE"),
    ("Great experience", "POSITIVE"),

    ("I am upset", "NEGATIVE"),
    ("This is the worst service", "NEGATIVE"),
    ("I am not happy", "NEGATIVE"),
    ("I feel bad", "NEGATIVE"),
    ("The product is broken", "NEGATIVE"),

    ("I am okay", "NEUTRAL"),
    ("I am fine", "NEUTRAL"),
    ("What is my order status?", "NEUTRAL"),
    ("Tell me more about this product", "NEUTRAL"),

    ("I was happy but sad at the same time", "MIXED"),
    ("Suggest some ways to be happy", "NEUTRAL"),  # advice treated as neutral in custom rules
]

correct = 0
results = []

for text, expected in test_cases:
    sentiment, intensity, score = analyze_sentiment(text)
    intent = detect_intent(text)
    response, escalation = generate_response(sentiment, intensity, intent)

    is_correct = (sentiment == expected)
    if is_correct:
        correct += 1

    results.append({
        "input": text,
        "expected": expected,
        "detected": sentiment,
        "intensity": intensity,
        "score": score,
        "intent": intent,
        "response": response,
        "escalation": escalation,
        "match": is_correct
    })

# Print detailed results
for r in results:
    print(f"Input: {r['input']}")
    print(f"Expected: {r['expected']} | Detected: {r['detected']} ({r['intensity']}, {r['score']:.2f})")
    print(f"Intent: {r['intent']} | Response: {r['response']}")
    if r['escalation']:
        print("⚠ Escalation triggered")
    print(f"Correct: {r['match']}\n")

# Accuracy
accuracy = correct / len(test_cases) * 100
print(f"Sentiment Detection Accuracy: {accuracy:.2f}%")
