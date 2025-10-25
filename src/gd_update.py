import numpy as np

def gradient_descent_update(weights, gradients, learning_rate=0.01):
    return np.array(weights) - learning_rate * np.array(gradients)

# Príklad: Weights, computed gradients (z loss function)
weights = [1.0, 0.95]
gradients = [0.1, -0.05] # Príklad gradientov
new_weights = gradient_descent_update(weights, gradients)
print(f"New weights: {new_weights}")
