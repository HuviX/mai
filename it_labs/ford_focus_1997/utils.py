import numpy as np
def generate_points(size, mu, sigma):
    return sigma * np.random.randn(size, 2) + mu