from backend.openrouter_client import client

response = client.chat.completions.create(
    model="google/gemini-2.5-flash",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Say hello"
        }
    ]
)

print(response.choices[0].message.content)