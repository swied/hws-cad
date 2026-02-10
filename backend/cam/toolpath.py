# backend/cam/toolpath.py
import numpy as np

class GCodeGenerator:
    """
    Generates 3-Axis G-Code for CNC shaping.
    Replaces boardcam.toolpathgenerators.
    """
    def __init__(self, board_model, cutter_diameter=10.0, feed_rate=1200):
        self.board = board_model
        self.cutter_radius = cutter_diameter / 2.0
        self.feed_rate = feed_rate
        self.safe_height = 50.0

    def generate_outline_cut(self):
        """
        Generates a 2D profile cut for the outline.
        """
        gcode = []
        gcode.append(f"%")
        gcode.append(f"G90 G21 (Absolute positioning, Millimeters)")
        gcode.append(f"G00 Z{self.safe_height} (Safe Z)")
        
        # Move to start
        start = self.board.outline_points[0]
        gcode.append(f"G00 X{start[0]} Y{start[1]}")
        gcode.append(f"G01 Z-5.0 F{self.feed_rate} (Plunge)")

        # Follow points (Offset logic would go here in production code)
        for p in self.board.outline_points[1:]:
            # Apply cutter offset roughly
            gcode.append(f"G01 X{p[0]} Y{p[1]}")

        gcode.append(f"G00 Z{self.safe_height}")
        gcode.append(f"M30 (End of program)")
        return "\n".join(gcode)

    def generate_deck_surface(self):
        """
        Raster scan path for deck.
        """
        pass  # Placeholder for complex raster logic