# backend/core/vectors.py
import numpy as np

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm

def cross_product(a, b):
    return np.cross(a, b)

def dot_product(a, b):
    return np.dot(a, b)