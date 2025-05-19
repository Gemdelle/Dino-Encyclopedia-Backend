from fastapi import FastAPI
from app import create_app
from app.api.v1.api import api_router
from app.core.config import settings

app = create_app()
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)