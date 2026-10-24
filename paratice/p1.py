from email.mime import application
from google import genai
import os
from dotenv import load_dotenv
from app.schemas import ExtractionResponse
load_dotenv()  # Load environment variables from .env file
# load_dotenv()

client=genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

output=client.models.generate_content(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    contents="we have 4 person travelling from New York to Paris on 2024-07-15 for 7 days. Please provide the best travel package.",
    config  ={
        "response_mime_type": "application/json",
        "response_json_schema": ExtractionResponse.model_json_schema()
    },
)
print(output.parsed)
response = ExtractionResponse.model_validate_json(output.text)
