from uvicorn import run
from fastapi import FastAPI

from api.routes import init_routes
from db.models.model_base import setup_db

app = init_routes(FastAPI())

if __name__ == "__main__":
    setup_db()
    run("api.main:app")
