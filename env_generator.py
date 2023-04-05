import numpy as np
import random
import math
import gaussian_dist


class EnvGrid:

    def __init__(self, size:int, seed:int, dimension:int, uniform_density:bool, cluster_count:int) -> None:

        random.seed(seed)

        self.size = size
        self.dimension = dimension
        self.uniform_density = uniform_density
        self.cluster_count = cluster_count
        self.cluster_centers = list()

        # Store the map
        self.system_grid = None
        self.initialise_env()

    def initialise_env(self) -> np.ndarray:
        """
        Create the grid representing the market. 
        Each position in the grid represents the number of consumers that occupy that position.
        """

        system_grid = None

        if self.dimension == 1:

            system_grid = np.ones((1, self.size))

            if not self.uniform_density:
                
                self.generate_clusters(system_grid)
                system_grid = self.plot_population(system_grid)
                
        elif self.dimension == 2:

            system_grid = np.ones((self.size, self.size))

            if not self.uniform_density:
                system_grid = np.random.randint(0, 5, size=(self.size, self.size))
                self.generate_clusters(system_grid)
                system_grid = self.plot_population(system_grid)

        self.system_grid = system_grid

    def generate_clusters(self, grid_in:np.ndarray) -> None:
        """
        Generate random cluster co-ordinates within grid
        
        Args:
            grid_in (np.ndarray): The grid representing the market that cluster centers will be generated within.

        """

        while len(self.cluster_centers) < self.cluster_count:

            point = self.get_random_point(grid_in)

            if all(math.dist(point, cluster) >= 15 for cluster in self.cluster_centers):

                self.cluster_centers.append(point)

    def plot_population(self, grid_in:np.ndarray) -> np.ndarray:
        """
        Allow a firm to consider its revenue at a new position with a price change.
        This method will plot a population density following a normal distribution centered at each cluster center.

        Args:
            grid_in (np.ndarray): The grid representing the market.

        Returns:
            grid_in (np.ndarray): The grid representing the market with a non-uniform population desnity plotted. 
            
        """
        for center in self.cluster_centers:
            gaussian = gaussian_dist.gaussian(0, random.randint(25, 50))
            for (i,j) in np.ndindex(grid_in.shape):
                distance_to_center = round(math.dist(center, [i, j]))
                if distance_to_center < 100:
                    grid_in[i][j] += round(gaussian.generate_gaussian_value(distance_to_center) * 1000)
        return grid_in
    
    def get_random_point(grid_in:np.ndarray) -> list():
        return [random.randint(0, grid_in.shape[0] - 1), random.randint(0, grid_in.shape[1] - 1)]

 