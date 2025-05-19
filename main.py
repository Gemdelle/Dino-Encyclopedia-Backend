from fastapi import FastAPI
from app import create_app
from app.api.v1.api import api_router

app = create_app()
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)