"""
Simple AI Chatbot — no external APIs, no internet required.
Runs entirely locally using pattern matching + basic memory.
"""

import random
import re

class SimpleAI:
    def __init__(self, name="Bot"):
        self.name = name
        self.memory = {}  # remembers facts the user tells it
        self.history = []

        # Pattern -> list of possible responses
        # {name} etc. get filled in dynamically
        self.rules = [
            (r"\b(hi|hello|hey)\b", [
                "Hello! How can I help you today?",
                "Hey there!",
                "Hi! What's on your mind?"
            ]),
            (r"my name is (\w+)", [
                "Nice to meet you, {0}!"
            ]),
            (r"what('?s| is) my name", [
                "Your name is {name}!" 
            ]),
            (r"how are you", [
                "I'm just a simple program, but I'm running fine! How about you?",
                "Doing well, thanks for asking!"
            ]),
            (r"\b(bye|goodbye|exit|quit)\b", [
                "Goodbye! Have a great day.",
                "See you later!"
            ]),
            (r"\bthank(s| you)\b", [
                "You're welcome!",
                "No problem at all!"
            ]),
            (r"(.*) or (.*)\?", [
                "Hmm, tough choice — I'd go with {0}.",
                "Honestly, {1} sounds better to me."
            ]),
            (r"\b(\d+)\s*\+\s*(\d+)\b", None),  # handled specially below
            (r".*\?$", [
                "That's an interesting question. I'm not sure, what do you think?",
                "I don't have a certain answer for that, but tell me more."
            ]),
        ]

        self.fallback_responses = [
            "Tell me more about that.",
            "Interesting — go on.",
            "I see. Why do you say that?",
            "Hmm, I'm not sure I follow. Can you rephrase?",
        ]

    def _remember_name(self, match):
        name = match.group(1)
        self.memory["name"] = name
        return f"Nice to meet you, {name}!"

    def respond(self, user_input):
        text = user_input.strip()
        self.history.append(text)
        lower = text.lower()

        # Special case: simple math "x + y"
        math_match = re.search(r"(-?\d+)\s*\+\s*(-?\d+)", lower)
        if math_match:
            a, b = int(math_match.group(1)), int(math_match.group(2))
            return f"{a} + {b} = {a + b}"

        # Name capture (match on lowercase, but pull the name from original text
        # so capitalization like "Alex" isn't lost)
        name_match = re.search(r"my name is (\w+)", text, re.IGNORECASE)
        if name_match:
            return self._remember_name(name_match)

        # Recall name
        if re.search(r"what('?s| is) my name", lower):
            if "name" in self.memory:
                return f"Your name is {self.memory['name']}!"
            else:
                return "I don't think you've told me your name yet!"

        # Go through remaining rules
        for pattern, responses in self.rules:
            if responses is None:
                continue
            m = re.search(pattern, lower)
            if m:
                reply = random.choice(responses)
                try:
                    return reply.format(*m.groups(), name=self.memory.get("name", "friend"))
                except (IndexError, KeyError):
                    return reply

        return random.choice(self.fallback_responses)


def main():
    bot = SimpleAI()
    print(f"{bot.name}: Hi! Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if not user_input.strip():
            continue
        reply = bot.respond(user_input)
        print(f"{bot.name}: {reply}")
        if re.search(r"\b(bye|goodbye|exit|quit)\b", user_input.lower()):
            break


if __name__ == "__main__":
    main()
