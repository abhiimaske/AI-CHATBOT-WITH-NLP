import nltk
import string
import datetime
import pytz
import wikipedia
import sympy as sp
from nltk.tokenize import word_tokenize


# Download tokenizer
nltk.download("punkt")

print("🤖 Smart NLP Chatbot")
print("Supports: Math | Time | Wikipedia")
print("Type 'help' or 'exit'\n")

GREETINGS = {"hi", "hello", "hey", "hii"}
MATH_KEYWORDS = {
    "add": "+", "plus": "+",
    "subtract": "-", "minus": "-",
    "multiply": "*", "times": "*",
    "divide": "/", "by": "/",
    "power": "**", "square": "**2",
    "percent": "/100"
}

def clean_text(text):
    tokens = word_tokenize(text.lower())
    return [w for w in tokens if w not in string.punctuation]

def is_math_query(tokens):
    return any(word.isdigit() or word in MATH_KEYWORDS for word in tokens)

def normalize_math_expression(tokens):
    expression = []

    for token in tokens:
        if token.isdigit():
            expression.append(token)
        elif token in MATH_KEYWORDS:
            expression.append(MATH_KEYWORDS[token])
        elif token in {"+", "-", "*", "/", "**"}:
            expression.append(token)

    return " ".join(expression)

def solve_math(expression):
    try:
        result = sp.sympify(expression)
        return f"Result = {result}"
    except ZeroDivisionError:
        return "Math Error: Division by zero ❌"
    except Exception:
        return "Invalid math expression ❌"

while True:
    user_input = input("You: ").strip()

    if not user_input:
        print("Bot: Say something 🙂")
        continue

    tokens = clean_text(user_input)

    # Exit
    if any(word in {"exit", "quit", "bye"} for word in tokens):
        print("Bot: Goodbye 👋")
        break

    # Greeting
    if any(word in GREETINGS for word in tokens):
        print("Bot: Hello! Ask me anything 📘")
        continue

    # Time intent
    if "time" in tokens and "india" in tokens:
        tz = pytz.timezone("Asia/Kolkata")
        current_time = datetime.datetime.now(tz).strftime("%I:%M %p")
        print(f"Bot: Current time in India is {current_time}")
        continue

    # Math intent
    if is_math_query(tokens):
        expression = normalize_math_expression(tokens)
        result = solve_math(expression)
        print("Bot:", result)
        continue

    # Wikipedia intent
    try:
        query = " ".join(tokens)
        summary = wikipedia.summary(query, sentences=2)
        print("Bot:", summary)
    except wikipedia.exceptions.DisambiguationError as e:
        print("Bot: Be more specific. Try:")
        for option in e.options[:5]:
            print(" -", option)
    except wikipedia.exceptions.PageError:
        print("Bot: No information found.")
    except Exception:
        print("Bot: Something went wrong.")
