import nltk
from nltk.tokenize import word_tokenize
import wikipedia

nltk.download("punkt")

print("NLP Wikipedia Chatbot 🤖")
print("Ask me anything! Type 'exit' to quit.\n")

# Greeting keywords
greetings = ["hi", "hello", "hey", "hii"]

while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Bot: Goodbye! 👋")
        break

    # Greeting response
    if user_input.lower() in greetings:
        print("Bot: Hello! 👋 Ask me anything.")
        continue

    try:
        # NLP preprocessing
        tokens = word_tokenize(user_input.lower())
        clean_query = " ".join(tokens)

        # Fetch answer from Wikipedia
        answer = wikipedia.summary(clean_query, sentences=2)

        print("\nBot:", answer, "\n")

    except wikipedia.exceptions.DisambiguationError as e:
        print("\nBot: Your question is too broad. Try one of these:")
        for option in e.options[:5]:
            print("-", option)
        print()

    except wikipedia.exceptions.PageError:
        print("\nBot: Sorry, I couldn't find information on that.\n")

    except Exception:
        print("\nBot: Something went wrong. Please try again.\n")
