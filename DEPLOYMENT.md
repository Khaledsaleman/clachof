# Deployment Guide for Render

## 1. Database (PostgreSQL)
- Create a "Blueprint" or "New PostgreSQL" on Render.
- Copy the External Database URL.

## 2. Backend (FastAPI)
- Create a "New Web Service".
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  - `DATABASE_URL`: Your Postgres URL.
  - `BOT_TOKEN`: Your Telegram Bot Token.
  - `TELEGRAM_SECRET`: Your bot secret for validation.

## 3. Frontend (React/Vite)
- Create a "New Static Site".
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`
- Environment Variables:
  - `VITE_API_URL`: URL of your backend web service.

## 4. Telegram Bot
- Create a "New Background Worker".
- Build Command: `pip install aiogram`
- Start Command: `python main.py`
- Environment Variables:
  - `BOT_TOKEN`: Your bot token.
  - `WEBAPP_URL`: URL of your frontend static site.
