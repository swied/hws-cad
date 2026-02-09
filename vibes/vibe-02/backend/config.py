# backend/config.py
import os

class Settings:
    PROJECT_NAME: str = "BoardCAD React"
    PROJECT_VERSION: str = "4.0.0"
    
    # CORS
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000"  # <--- ADDED THIS LINE
    ]
    
    # File Paths
    BOARDS_DIR = os.path.join(os.getcwd(), "boards")
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")

settings = Settings()