import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

from config import DATABASE_URL

logger = logging.getLogger(__name__)

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

    except Exception:
        logger.exception("Database health check failed")
        raise HTTPException(status_code=503, detail="database unavailable")

    return {
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
