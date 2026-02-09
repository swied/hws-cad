"""
Hollow Wooden Surfboard Geometry Engine.

This module is responsible for reading surfboard design parameters (JSON)
and calculating the precise B-Spline curves required to generate manufacturing
data for a hollow wooden surfboard frame (spine and ribs).

It uses Scipy for spline interpolation to ensure smooth, organic curves.

Author: [Your Name]
License: MIT
"""

import json
import numpy as np
from scipy.interpolate import BSpline, make_interp_spline
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

class SurfboardDesign:
    """
    A class representing the geometry of a hollow wooden surfboard.

    Attributes:
        length (float): Length of the board in inches.
        width (float): Width at the wide point in inches.
        thickness (float): Thickness at the thickest point in inches.
        nose_rocker (float): Lift at the nose in inches.
        tail_rocker (float): Lift at the tail in inches.
    """

    def __init__(self, design_file_path: str):
        """
        Initialize the design object by loading parameters from a JSON file.

        Args:
            design_file_path (str): Path to the .json file exported from the Web App.
        """
        self._load_parameters(design_file_path)
        self.spine_curve = None
        self.outline_curve = None
        self.deck_curve = None
        self.bottom_curve = None

    def _load_parameters(self, path: str):
        """
        Parses the JSON file and converts units to a standard inch-based system.
        """
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Convert Feet to Inches for consistent internal math
        self.length = data.get('length', 7.0) * 12.0 
        self.width = data.get('width', 21.0)
        self.thickness = data.get('thickness', 2.75)
        self.nose_rocker = data.get('nose_rocker', 4.0)
        self.tail_rocker = data.get('tail_rocker', 2.5)
        
        # Offsets are percentages (-20 to 20)
        self.wide_point_offset = data.get('widthOffset', 0) / 100.0
        self.thick_point_offset = data.get('thicknessOffset', 0) / 100.0

    def generate_rocker_profile(self, num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates the rocker (side profile) curve of the surfboard spine.
        
        Uses a spline interpolation through the tail, center, and nose.

        Args:
            num_points (int): Resolution of the generated array.

        Returns:
            Tuple[np.ndarray, np.ndarray]: (x_coordinates, y_coordinates)
        """
        # X coordinates (Length): 0 is Tail, Length is Nose
        x = np.array([0, self.length / 2, self.length])
        
        # Y coordinates (Height): Tail Rocker, 0 (Center), Nose Rocker
        # Note: Usually center is lowest point (0), rockers are positive Y
        y = np.array([self.tail_rocker, 0, self.nose_rocker])
        
        # Create a smooth B-Spline, k=2 (quadratic) or k=3 (cubic)
        spline = make_interp_spline(x, y, k=2)
        
        x_new = np.linspace(0, self.length, num_points)
        y_new = spline(x_new)
        
        self.spine_curve = (x_new, y_new)
        return x_new, y_new

    def generate_outline(self, num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates the plan shape (half-width) of the board.

        Args:
            num_points (int): Resolution.

        Returns:
            Tuple[np.ndarray, np.ndarray]: (x_coords, y_coords_half_width)
        """
        # Define key control points for the outline
        # Tail (0,0), Wide Point, Nose (Length, 0)
        
        # Calculate Wide Point X location
        # Standard wide point is center (L/2). Offset shifts it forward/back.
        center_x = (self.length / 2) - (self.wide_point_offset * self.length)
        
        x = np.array([0, 12, center_x, self.length - 12, self.length])
        # Y is half-width at these points. 
        # 12" from ends usually has specific width, here we approximate.
        half_width = self.width / 2.0
        y = np.array([1.0, half_width * 0.6, half_width, half_width * 0.4, 0.5]) # 0.5 min width at tips
        
        spline = make_interp_spline(x, y, k=3) # Cubic spline for smooth outline
        x_new = np.linspace(0, self.length, num_points)
        y_new = spline(x_new)
        
        # Clamp Y to be non-negative
        y_new[y_new < 0] = 0
        
        self.outline_curve = (x_new, y_new)
        return x_new, y_new

    def calculate_cross_section(self, station_x: float) -> List[Tuple[float, float]]:
        """
        Calculates a specific cross-section (rib) at a given distance from the tail.

        This combines the Rocker (height), Outline (width), and Thickness 
        at that specific X location to create an ellipse-like rib shape.

        Args:
            station_x (float): Distance from tail in inches.

        Returns:
            List[Tuple[float, float]]: List of (y, z) coordinates for the rib 2D shape.
            Note: In cross section, Y is width, Z is thickness/height relative to bottom.
        """
        # 1. Get Width at this station
        if self.outline_curve is None: self.generate_outline()
        x_out, y_out = self.outline_curve
        current_half_width = np.interp(station_x, x_out, y_out)
        
        # 2. Get Rocker height at this station (Bottom reference)
        if self.spine_curve is None: self.generate_rocker_profile()
        x_rock, y_rock = self.spine_curve
        current_rocker_y = np.interp(station_x, x_rock, y_rock)
        
        # 3. Calculate Thickness at this station
        # Simple foil distribution based on sine wave for now
        # Normalized length 0..1
        t_norm = station_x / self.length
        # Shift thickness apex
        t_apex = 0.5 - self.thick_point_offset
        # Create a foil curve (parabolic/sine)
        current_thickness = self.thickness * np.sin(np.pi * t_norm) 

        # 4. Generate points for the Rib
        # We generate an ellipse, then subtract 'skin_thickness' later
        angles = np.linspace(0, 2 * np.pi, 60)
        rib_points = []
        
        for theta in angles:
            # Ellipse formula
            # Width is X-axis in local rib coords
            w_local = current_half_width * np.cos(theta)
            # Thickness is Y-axis in local rib coords
            h_local = (current_thickness / 2.0) * np.sin(theta)
            
            rib_points.append((w_local, h_local))
            
        return rib_points

    def export_rib_svg(self, station_x: float, filename: str):
        """
        Exports a specific rib as an SVG file for printing/cutting.
        
        Args:
            station_x (float): Position from tail.
            filename (str): Output filename.
        """
        points = self.calculate_cross_section(station_x)
        
        # SVG Header
        svg = [f'<svg viewBox="-20 -10 40 20" xmlns="http://www.w3.org/2000/svg">']
        
        # Convert points to SVG path
        path_d = "M " + " L ".join([f"{p[0]},{p[1]}" for p in points]) + " Z"
        
        # Add path with styling (Cut line)
        svg.append(f'<path d="{path_d}" fill="none" stroke="black" stroke-width="0.05" />')
        
        # Add centerline marker
        svg.append(f'<line x1="0" y1="-5" x2="0" y2="5" stroke="red" stroke-width="0.02" />')
        
        svg.append('</svg>')
        
        with open(filename, 'w') as f:
            f.write("\n".join(svg))
        print(f"Exported rib at {station_x:.1f}\" to {filename}")

# --- Example Usage Logic ---
if __name__ == "__main__":
    # 1. Initialize
    # In a real scenario, this file path comes from the JSON downloaded from the Web App
    # We will mock the file creation here for demonstration
    mock_data = {
        "length": 7.2,
        "width": 21.5,
        "thickness": 2.75,
        "nose_rocker": 4.5,
        "tail_rocker": 2.5
    }
    with open("my_surfboard_design.json", "w") as f:
        json.dump(mock_data, f)

    # 2. Process
    board = SurfboardDesign("my_surfboard_design.json")
    
    # 3. Analyze
    print(f"Processing Board: {board.length}\" Long")
    
    # 4. Generate Ribs every 12 inches
    for i in range(12, int(board.length), 12):
        board.export_rib_svg(i, f"rib_station_{i}.svg")
    
    print("Done. Check generated SVG files.")