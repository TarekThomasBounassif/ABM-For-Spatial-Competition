import numpy as np
import random
import math
from shapely import geometry
import utility
import gaussian_dist


class grid_generator_nbyn:

    def __init__(self, size, seed) -> None:
        random.seed(seed)

        self.grid_size = size

        # Make base grid
        self.grid_master = self.initialise_grid()

        # Make perimeter
        self.polygon = self.create_polygon()

        # Make cluster centers
        self.clusters = self.make_cluster_centers(3, self.grid_size, self.polygon)

        # Plot clusters
        self.grid_master = self.plot_clusters(self.grid_master, self.clusters)

        # Track cluster peaks for graphing purposes
        self.cluster_peaks = self.get_cluster_peaks(self.grid_master, self.clusters)

        # Normalize grid values
        self.grid_master = utility.normalize(self.grid_master)

        # Fill in perimiter
        self.grid_master = self.fill_polygon(self.grid_master, self.polygon)

    def initialise_grid(self) -> np.ndarray:
        """
        Initialise the grid to random population desinty within range 0 -> 15
        """ 
        grid = np.full((100,100), 0)
        for (i,j), value in np.ndenumerate(grid):
            grid[j][i] = value + random.randint(0,15)
        return grid

    def make_cluster_centers(self, n, grid_size, polygon) -> list:
        """
        Create n clusters. Must be a min distance apart. Must be within perimiter. 
        """ 

        centers_list = []

        while len(centers_list) < n:
            x = random.randint(0, grid_size)
            y = random.randint(0, grid_size)

            # Only accept centers within perimiter
            if polygon.contains(geometry.Point(x,y)):
                
                potential_center = [x,y]
                good_cluster = True

                # Clusters cannot be within 10 units of distance from eachother
                if len(centers_list) > 0:
                    for c in centers_list:
                        if math.dist(potential_center, c) < 10:
                            good_cluster = False
                            break

                if good_cluster:
                    centers_list.append(potential_center)

        return centers_list
    
    def plot_cluster(self, grid, center):
        """
        Plot a cluster where surounding population desity follows gaussian dist with peak at popultion center.
        """ 
        gaussian = gaussian_dist.gaussian(0, random.randint(25, 50))
        for (i,j), value in np.ndenumerate(grid):
            current_point = [i, j]
            d = round(math.dist(center, current_point))
            if d < 20:
                grid[j][i] = grid[j][i] + gaussian.generate_gaussian_value(d) * 1000
        return grid

    def plot_clusters(self, grid, clusters) -> np.ndarray:
        for c in clusters:
            grid = self.plot_cluster(grid, c)
        return grid

    def get_cluster_peaks(self, grid, clusters) -> list:
        """
        Helper method that returns the peak population desity of each cluster, incremented by 10 for graphing.
        """
        peaks = []
        for c in clusters:
            peaks.append((c[0], c[1], grid[c[1]][c[0]] + 10))
        return peaks

    def make_rand_points(self, number_of_points, grid_size) -> list:  
        """
        Randomly generate a list of points, this will be perimiter of the map.
        """ 
        list_out = []
        while len(list_out) < number_of_points:
            x = random.randint(0, grid_size)
            y = random.randint(0, grid_size)
            if (
                (x < 10 or x > 90) or (30 < x < 70)
                or (y < 10 or y > 90) or (30 < y < 70)
                or geometry.Point(x, y) in list_out
            ):
                continue
            list_out.append(geometry.Point(x, y))
        return list_out

    def arrange_points(self, point_list) ->  list:
        """
        Arange points based on shortest distance from eachother. Used to better define perimiter. 
        """ 

        # Start with point closest to origin
        starting_point = utility.find_closest(geometry.Point(0,0), point_list, [])
        new_order = [starting_point]

        while len(new_order) < len(point_list):
            closest_point = utility.find_closest(starting_point, point_list, new_order)
            new_order.append(closest_point)
            starting_point = closest_point

        return new_order

    def fill_polygon(self, grid, polygon) -> np.ndarray:
        """
        Set all positions on grid to none if outside perimiter 
        """ 
        for (i,j), value in np.ndenumerate(grid): 
            if not polygon.contains(geometry.Point(i,j)):
                grid[j][i] = None
        return grid

    def create_polygon(self) -> geometry.Polygon:
        # Make points
        pointList = self.make_rand_points(20, 100)
        pointList = self.arrange_points(pointList)

        # Convert to  polygon
        poly = geometry.Polygon([[p.x, p.y] for p in pointList])
        poly = poly.buffer(0)

        # If multi take largest
        try:
            polygons = poly.geoms
            largest_len = 0
            for p in polygons:
                if len(p.wkt) > largest_len:
                    largest_len = len(p.wkt)
                    poly = p
        except:
            None
        return poly
