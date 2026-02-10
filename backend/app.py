# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import board, cam
from config import settings, ALLOWED_ORIGINS

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Configure CORS to allow the React Frontend to communicate with this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the API routers
app.include_router(board.router, prefix="/api/board", tags=["board"])
app.include_router(cam.router, prefix="/api/cam", tags=["cam"])

@app.get("/")
async def root():
    """
    Health check endpoint.
    """
    return {
        "system": "BoardCAD Scientific Backend",
        "status": "online",
        "version": settings.PROJECT_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)