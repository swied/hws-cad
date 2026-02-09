# backend/core/nurbs.py
import numpy as np

class NurbsSurface:
    """
    Python implementation of Non-Uniform Rational B-Splines.
    Replaces Java cadcore.NurbsSurface.
    """
    def __init__(self, control_points, knots_u, knots_v, degree_u=3, degree_v=3):
        self.ctrl_pts = np.array(control_points)
        self.knots_u = np.array(knots_u)
        self.knots_v = np.array(knots_v)
        self.p = degree_u
        self.q = degree_v

    def point_at(self, u, v):
        """
        Evaluate surface at (u, v) using De Boor's algorithm.
        """
        # Simplified placeholder logic:
        # In reality, this requires basis function computation (N_i,p)
        return np.array([u * 100, 0, v * 20])