# MasterClass

FastAPI + LangChain backend with an OpenRouter-powered LLM gateway, built for production and containerized deployment (Docker/Dokploy).

> 📖 ¿Primeros pasos? Leé la [guía para principiantes en español](docs/guia-principiantes.md) — tecnologías explicadas desde cero.

## Stack

- **FastAPI** 0.162 — async routing, Pydantic v2 validation, dependency injection
- **LangChain** 1.5 — LCEL chain composition (LLM via OpenRouter)
- **Uvicorn** — ASGI server
- **Python** 3.13

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # then set OPENROUTER_API_KEY

uvicorn app.main:app --reload          # API on http://127.0.0.1:8000
python seo_agent.py                    # interactive Real Estate SEO agent CLI
```

## Docker

```bash
docker compose up --build   # dev: live-reload on port 8000
```

## Layout

```
app/
  main.py            # app factory + /health
  core/config.py     # typed settings (pydantic-settings)
seo_agent.py         # standalone LLM CLI (OpenRouter)
```
