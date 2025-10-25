import numpy as np

def compute_aav(weights, scores, biases=None, reciprocities=None):
    if biases is None:
        biases = np.ones(len(scores))
    if reciprocities is None:
        reciprocities = np.ones(len(scores))
    numerator = np.sum(np.array(weights) * np.array(scores) * biases * reciprocities)
    denominator = np.sum(weights)
    return numerator / denominator

# Príklad použitia
weights = [1.0, 0.95, 0.90, 0.85, 0.95, 0.80, 0.85, 0.95] # INT, LEX, WIS, REL, VER, LIB, UNI, CRE
scores = [0.85, 0.78, 0.92, 0.70, 0.95, 0.82, 0.88, 0.91]
aav = compute_aav(weights, scores)
print(f"AAV: {aav:.4f}")
