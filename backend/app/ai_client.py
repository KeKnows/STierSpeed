# AI_CLIENT: simple wrapper. For tests, calls are mocked.
# AI-GENERATED: This file contains helper prompt templates and a call function.

import os
from app.config import OPENAI_API_KEY
import httpx
from typing import List, Dict

OPENAI_API_KEY = OPENAI_API_KEY

def build_summary_prompt(user_profile: Dict, workouts: List[Dict]) -> str:
    # concise human-friendly prompt
    return f"User profile: {user_profile}\n\nWorkouts: {workouts}\n\nPlease summarize trends in 2-3 sentences, one strength, one weakness, and one actionable suggestion."

async def call_ai_summary(prompt: str) -> str:
    # This is a simple placeholder that uses OpenAI completion / chat API.
    if not OPENAI_API_KEY:
        # Return a mocked summary when no API key available (useful for local dev/tests)
        return "MOCK SUMMARY: no OPENAI_API_KEY provided. Weekly summary: keep consistent acceleration work."
    # Example using a hypothetical OpenAI REST call. Replace with official SDK as needed.
    async with httpx.AsyncClient(timeout=30.0) as client:
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        body = {"model": "gpt-4o-mini", "messages": [{"role":"user","content":prompt}], "max_tokens":300}
        resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
        resp.raise_for_status()
        data = resp.json()
        # parse response safely
        content = data["choices"][0]["message"]["content"]
        return content

