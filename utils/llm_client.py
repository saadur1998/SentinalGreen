# utils/llm_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_FOUNDRY_ENDPOINT = os.getenv("AZURE_FOUNDRY_ENDPOINT")
API_KEY = os.getenv("AZURE_FOUNDRY_API_KEY")

USE_LOCAL = os.getenv("USE_LOCAL_LLM", "False").lower() == "true"
LOCAL_ENDPOINT = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:8000/query")

HEADERS = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

def get_llm_response(prompt: str) -> str:
    payload = {
        "input": prompt,
        "parameters": {
            "temperature": 0.7
        }
    }

    try:
        if USE_LOCAL:
            print("?? Using local LLM endpoint...")
            response = requests.post(LOCAL_ENDPOINT, json=payload, timeout=10)
        else:
            print("?? Using Azure AI Foundry endpoint...")
            response = requests.post(AZURE_FOUNDRY_ENDPOINT, headers=HEADERS, json=payload, timeout=15)

        response.raise_for_status()
        json_response = response.json()

        # Handle Azure Foundry and local LLM response formats
        if "output" in json_response:
            return json_response["output"]
        elif "choices" in json_response:  # if structured like OpenAI completion
            return json_response["choices"][0]["text"].strip()
        else:
            return "?? No output received from LLM."

    except Exception as e:
        print(f"? Error querying LLM: {e}")
        return "?? LLM error occurred. Check logs or endpoint."