from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from config import DATABASE_URL

app = FastAPI(title="AWS CI/CD Application")

engine = create_engine(DATABASE_URL)


@app.get("/")
def home():
    return {
        "message": "AWS CI/CD application is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/db-health")
def db_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "disconnected",
            "error": str(e)
        }