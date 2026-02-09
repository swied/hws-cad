# backend/api/cam.py
from fastapi import APIRouter, Response
from pydantic import BaseModel
from cam.toolpath import GCodeGenerator
from api.board import current_board # Import the active board state

router = APIRouter()

class CamSettings(BaseModel):
    cutter_diameter: float
    feed_rate: int

@router.post("/generate/outline")
async def generate_outline_gcode(settings: CamSettings):
    """
    Returns a downloadable G-Code file content.
    """
    generator = GCodeGenerator(current_board, settings.cutter_diameter, settings.feed_rate)
    gcode_content = generator.generate_outline_cut()
    
    return Response(
        content=gcode_content,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=outline.cnc"}
    )