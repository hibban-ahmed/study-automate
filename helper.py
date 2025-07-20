import httpx
from dotenv import load_dotenv
import os
load_dotenv()


async def call_ai_model(prompt: str, resources: str, model: str, api_key: str) -> str:
    full_input = f"Resources:\n{resources}\n\nPrompt:\n{prompt}"

    if model == "gemini":
        return await call_gemini_api(full_input, api_key)
    elif model == "llama":
        return await call_llama_api(full_input, api_key)
    else:
        return "Model not supported"


async def call_gemini_api(text: str, api_key: str) -> str:
    model_name = "models/text-bison-001"
    url = f"https://generativelanguage.googleapis.com/v1beta2/{model_name}:generateText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
    }

    payload = {
        "prompt": {"text": text},
        "maxTokens": 512,
        "temperature": 0.7,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                return data["candidates"][0].get("output", "No output text found")
            return "No output returned from Gemini API"
    except Exception as e:
        return f"Error calling Gemini API: {e}"


async def call_llama_api(text: str, api_key: str) -> str:
    model_name = "llama2-70b-chat"
    url = f"https://api.groq.ai/v1/models/{model_name}/invoke"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": text,
        "max_tokens": 512,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                return data["results"][0].get("text", "No text found in response")
            return "No output returned from GROQ API"
    except Exception as e:
        return f"Error calling GROQ LLaMA API: {e}"
