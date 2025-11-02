# compute_aav.py
import numpy as np

def compute_aav(weights, scores, biases=None, reciprocities=None):
    weights = np.array(weights, dtype=float)
    scores = np.array(scores, dtype=float)
    if biases is None:
        biases = np.ones_like(scores)
    if reciprocities is None:
        reciprocities = np.ones_like(scores)
    numerator = np.sum(weights * scores * biases * reciprocities)
    denom = np.sum(weights)
    return float(numerator / denom) if denom != 0 else 0.0

if __name__ == "__main__":
    w = [1.0,0.95,0.90,0.85,0.95,0.80,0.85,0.95]
    s = [0.85,0.78,0.92,0.70,0.95,0.82,0.88,0.91]
    print("AAV:", compute_aav(w,s))
