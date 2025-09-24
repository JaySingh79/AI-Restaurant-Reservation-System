from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

async def gemini_client_test(prompt):
        
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=prompt,
    )

    return response.text