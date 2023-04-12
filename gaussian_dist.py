import numpy as np
import scipy.stats as stats
import math

class gaussian:

    def __init__(self, mu, variance) -> None:
        """
        Initialize gaussian parameters
        """
        self.mu = 0
        self.variance = variance
        self.sigma = math.sqrt(variance)
        self.x = np.linspace(mu - 3*self.sigma, mu + 3*self.sigma, 100)
        self.x = [number for number in range(-100, 100)]
        self.y = stats.norm.pdf(self.x, mu, self.sigma)
    
    def generate_gaussian_value(self, val) -> float:
        """
        Generate a gaussian value based on input value
        """
        for i in range(0, len(self.x)):
            if self.x[i] == val:
                return self.y[i]
