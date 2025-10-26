# scripts/gd_update.py
import numpy as np

def gradient_descent_update(weights, gradients, learning_rate=0.01):
    return list(np.array(weights) - learning_rate * np.array(gradients))

if __name__ == '__main__':
    weights = [1.0, 0.95]
    gradients = [0.1, -0.05]
    print("New weights:", gradient_descent_update(weights, gradients))
