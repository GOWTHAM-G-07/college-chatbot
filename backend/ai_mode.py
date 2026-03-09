import requests

API_KEY = "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"

def ai_answer(question):

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": question}
                ]
            }
        )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except:
        return "AI service unavailable."