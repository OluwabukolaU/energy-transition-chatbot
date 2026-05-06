import requests

api_key = "paste-your-real-key-here"

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    json={
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 100,
        "messages": [
            {"role": "user", "content": "say hello"}
        ]
    }
)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)