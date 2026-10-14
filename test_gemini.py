
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for model in [
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
]:
    try:
        response = client.models.generate_content(
            model=model,
            contents="Reply with only: Gemini is working"
        )
        print(f"\nSUCCESS: {model}")
        print(response.text)
        break
    except Exception as e:
        print(f"\nFAILED: {model}")
        print(str(e)[:300])
