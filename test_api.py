
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
    timeout=180.0,
    max_retries=2
)

try:
    print("Connecting to Gemini...")

    response = client.chat.completions.create(
        model="gemini-3.8-flash",
        reasoning_effort="low",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: API WORKING"
            }
        ]
    )

    print("SUCCESS!")
    print(response.choices[0].message.content)

except Exception as e:
    print("ERROR:", type(e).__name__)
    print("DETAILS:", repr(e))
