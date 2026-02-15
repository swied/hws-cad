# backend/config.py
import os

class Settings:
    PROJECT_NAME: str = "BoardCAD React"
    PROJECT_VERSION: str = "4.0.0"

    def __init__(self):
        # 1. Start with defaults
        origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0:3000"]
        
        # 2. Add origins from environment variables if they exist
        env_origins = os.getenv("ALLOWED_ORIGINS")
        if env_origins:
            origins.extend([o.strip() for o in env_origins.split(",")])
            
        self.ALLOWED_ORIGINS = list(set(origins))
        print(f"CORS Allowed Origins: {self.ALLOWED_ORIGINS}")

    BOARDS_DIR = os.path.join(os.getcwd(), "boards")
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")

settings = Settings()