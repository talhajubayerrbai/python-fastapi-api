"""FastAPI service — replace the routes below with your application."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI(title="app")

_LANDING = (Path(__file__).parent / "static" / "index.html").read_text()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return _LANDING
