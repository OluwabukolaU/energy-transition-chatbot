import requests
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
url = "https://api.anthropic.com/v1/messages"
system_prompt = """
You are a helpful energy transition assistant that helps users
understand all about energy transition, sustainability, ESG 
and climate matters. You specialise in neighbourhood-level energy
systems, particularly Meerstad and Meerkracht cooperative in Groningen, Netherlands.
If someone asks about anything else, politely say you can 
only help with energy transition, sustainability, ESG and climate matters.
""" 
print("=" * 50)
print("⚡ Meerstad Energy Transition Chatbot ⚡")
print("Type 'quit' to exit")
print("=" * 50)

history = []

def ask_claude(user_input):
    try:
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 1024,
            "system": system_prompt,
            "messages": history
        }
        response = requests.post(url, headers=headers, json=payload)
       
        if response.status_code == 200:
            data = response.json()
            return data["content"][0]["text"]
        else:
            return f"Error: {response.status_code}"
    except ConnectionError:
        return "No internet connection!"
    except Exception as e:
        return "Something went wrong: " + str(e)


# ... your imports and variables at top ...

def log_conversation(role, message):      # ← add here
    with open("conversation.txt", "a", encoding="utf-8") as f:
        f.write(role + ": " + message + "\n")

while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    history.append({"role": "user", "content": user_input})
    log_conversation("You", user_input)      # ← log user message
    reply = ask_claude(user_input)
    history.append({"role": "assistant", "content": reply})
    log_conversation("Claude", reply)        # ← log Claude's reply
    print(reply)

print("Goodbye!")