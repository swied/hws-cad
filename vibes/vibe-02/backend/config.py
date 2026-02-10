# backend/config.py
import os


class Settings:
    PROJECT_NAME: str = "BoardCAD React"
    PROJECT_VERSION: str = "4.0.0"

    # Read from environment variable, split by comma, or default to localhost:3000
    origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
    ALLOWED_ORIGINS = [
        origin.strip() 
        for origin 
        in origins_raw.split(",") 
        if origin.strip()]
    
    print(f"CORS Allowed Origins: {ALLOWED_ORIGINS}") # Helps verify in Docker logs

    # CORS
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:3000"  # <--- ADDED THIS LINE
    ]

    ALLOWED_ORIGINS = list(set(ALLOWED_ORIGINS))
    
    # File Paths
    BOARDS_DIR = os.path.join(os.getcwd(), "boards")
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")

settings = Settings()