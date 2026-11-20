import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="ASKORA AI API", version="0.2.0")
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: Optional[str] = "auto"

@app.get("/")
def root():
    return {"name": "ASKORA AI", "status": "starter-ready", "message": "Your AI. Your Shopping Agent."}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat")
def chat(payload: ChatRequest):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {"reply": "ASKORA backend is online, but the AI engine is not connected yet. Add OPENAI_API_KEY in your hosting environment to activate AI chat.", "ai_connected": False}
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            instructions="""You are ASKORA AI, a Hindi-first shopping assistant. Understand the user's shopping request, ask concise follow-up questions when needed, compare criteria, and never invent current prices, availability, discounts, merchant stock, or delivery times. If live commerce data is not provided, say so clearly. Do not place orders or payments; always require user confirmation and direct them to a verified merchant checkout.""",
            input=payload.message
        )
        return {"reply": response.output_text, "ai_connected": True}
    except Exception as exc:
        # Do not expose secrets or raw provider error details to clients.
        raise HTTPException(status_code=502, detail="AI provider request failed. Check backend configuration and logs.") from exc


@app.post("/api/products/search")
def product_search(payload: ChatRequest):
    # No commerce search provider has been configured. This endpoint deliberately does not fabricate listings.
    return {"live_search_connected": False, "query": payload.message, "message": "Live product search provider is not configured. Add a compliant product-search/affiliate data source before displaying real prices."}
