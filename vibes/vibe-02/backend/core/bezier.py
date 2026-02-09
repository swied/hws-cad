# backend/core/bezier.py
import numpy as np

class BezierCurve:
    """
    Replaces Java cadcore.BezierCurve
    Utilizes numpy for vectorized calculation of scientific data.
    """
    def __init__(self, control_points):
        # control_points should be a list of tuples or numpy array [(x,y), ...]
        self.control_points = np.array(control_points)

    def evaluate(self, t):
        """
        Calculate point at t (0.0 to 1.0) using De Casteljau's algorithm
        or Bernstein polynomials.
        """
        n = len(self.control_points) - 1
        return np.sum([
            self.bernstein_poly(n, i, t) * self.control_points[i]
            for i in range(n + 1)
        ], axis=0)

    @staticmethod
    def bernstein_poly(n, i, t):
        from scipy.special import comb
        return comb(n, i) * (t ** i) * ((1 - t) ** (n - i))

    def to_dict(self):
        return {"control_points": self.control_points.tolist()}