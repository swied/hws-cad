# backend/api/board.py
from fastapi import APIRouter, HTTPException
from models.surfboard import SurfboardModel
from core.bezier import BezierCurve

router = APIRouter()

# In-memory storage for MVP
current_board = SurfboardModel(
    id="default",
    name="New Board",
    dimensions={"length": 600, "width": 50, "thickness": 5},
    outline_points=[[0, 0], [300, 25], [600, 0]],
    rocker_points=[[0, 5], [300, 0], [600, 2]]
)

@router.get("/", response_model=SurfboardModel)
async def get_current_board():
    return current_board

@router.post("/update")
async def update_board(board: SurfboardModel):
    global current_board
    current_board = board
    return {"status": "updated"}

@router.get("/calculate-volume")
async def calculate_volume():
    """
    Example of scientific task offloaded to Python.
    Calculates volume based on Bezier curves.
    """
    # 1. Reconstruct curves from points
    outline = BezierCurve(current_board.outline_points)
    # 2. Perform integration (Mock logic here)
    # In real impl, integration logic from cadcore/MathUtils moves here
    estimated_volume = 35.5 
    return {"volume_liters": estimated_volume}