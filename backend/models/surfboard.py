# backend/models/surfboard.py
from pydantic import BaseModel
from typing import List, Tuple

class BoardDimensions(BaseModel):
    length: float
    width: float
    thickness: float

class SurfboardModel(BaseModel):
    """
    Replaces board.AbstractBoard and board.BezierBoard.
    This serves as the DTO (Data Transfer Object) between Python and React.
    """
    id: str
    name: str
    dimensions: BoardDimensions
    # Outline control points (x, y)
    outline_points: List[Tuple[float, float]]
    # Rocker control points (x, y)
    rocker_points: List[Tuple[float, float]]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123",
                "name": "Shortboard Classic",
                "dimensions": {"length": 180.0, "width": 50.0, "thickness": 5.0},
                "outline_points": [[0, 0], [90, 25], [180, 0]],
                "rocker_points": [[0, 2], [90, 0], [180, 1]]
            }
        }
    }