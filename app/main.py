from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import url_check

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(url_check.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "URL Scanner API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
