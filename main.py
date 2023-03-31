import env_plotter
import numpy as np
import model
import math

grid_params = {
    'Size': 100,
    'Seed': 1,
    'Dim':1,
    'Uniform':False,
    'ClusterCount':2
}

firm_params = {
    'FirmCount': 3,
    'StartPrice': 10,
    'Seed': 1
}

system_test = model.Model(grid_params, firm_params)


env_plotter.plot_1d_system(system_test.model_grid)

def closest_point(point, points_list):
    dist_func = lambda p: math.sqrt((point[0]-p[0])**2 + (point[1]-p[1])**2)
    closest_point = min(points_list, key=dist_func)
    return closest_point