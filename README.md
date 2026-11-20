# ASKORA AI — Deployment Starter v0.2

This package contains a FastAPI backend and the prototype web UI. It is **not deployed** and does not include any API credentials.


## Endpoints
- `GET /` — service metadata
- `GET /health` — health check
- `POST /api/chat` — AI chat (requires `OPENAI_API_KEY`)
- `POST /api/products/search` — placeholder that clearly reports live product search is not configured

## Deploy on Render
1. Upload this folder to a new GitHub repository (do not commit secrets).
2. In Render, choose **New → Blueprint**, connect the repository and select `render.yaml`.
3. In Render service Environment, set `OPENAI_API_KEY` securely. Keep it private; never put it in frontend code or chat.
4. Deploy. Once service is live, verify `https://YOUR-SERVICE.onrender.com/health` returns `{"status":"ok"}`.
5. API docs are at `https://YOUR-SERVICE.onrender.com/docs`.

## Local run
```bash
python -m venv .venv
# Activate the venv, then:
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"  # macOS/Linux shell only; do not share the key
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs to test. Windows PowerShell environment command:
`$env:OPENAI_API_KEY="your-key"`

## Current limits
- AI chat requires a valid API key.
- Product endpoint is a placeholder. No retailer live prices, inventory, affiliate links, carts, or checkout are connected yet.
- Orders/payments are not executed; user must confirm at a merchant checkout.
