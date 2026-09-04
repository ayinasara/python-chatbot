import json
import re

with open("intents.json", "r") as file:
    data = json.load(file)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return text

def load_data():
    with open("intents.json", "r") as file:
        return json.load(file)

def get_response(message):
    data = load_data()

    message = preprocess_text(message)

    # PERSONAL QUESTION DETECTION
    personal_keywords = [
        "you",
        "your",
        "yourself",
        "personal",
        "age",
        "phone",
        "password",
        "family",
        "where do you live"
    ]

    for word in personal_keywords:
        if word in message:
            return """
I am PyTutor Assistant.

I cannot share personal details,
but I can help you learn Python.
"""

    # NORMAL INTENT MATCHING
    for intent in data["intents"]:
        patterns = intent.get("patterns", [])
        response = intent.get("response", "")

        for pattern in patterns:
            pattern = preprocess_text(pattern)

            if pattern == message:
                return response

    return """
Sorry, I don't understand that topic yet.

Try asking about:
- variables
- data types
- loops
- functions
- lists
- tuples
- sets
- dictionaries
- modules
- packages
"""
