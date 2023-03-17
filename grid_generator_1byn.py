import numpy as np
import random

class grid_generator:

    def __init__(self, size, flag, seed) -> None:

        if flag == "uniform":
            self.grid = self.initialise_grid(size)
        elif flag == "gaussian":
            self.grid = None

    
    def initialise_grid_uniform(self, size) -> np.ndarray:
        """
        Initialise 1 x N grid with uniform population density. 
        """ 
        return np.ones((1, size))
    
    def initialise_grid_gaussian(self, population_centers, size) -> np.ndarray:
        """
        Initialise 1 x N grid with gaussian population density. Each distribution will be centered
        at a point representing a population cetner. 
        """ 
        return np.ones((1, size))