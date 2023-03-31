import numpy as np
import random
import math
from matplotlib import pyplot as plt, cm, colors
from shapely import geometry
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
import matplotlib as mpl


def find_closest(point, point_list, exclude) -> geometry.Point:
    """
    Return the closest point between a point and a list of points.
    """ 
    smallest_distance = math.inf
    closest_point = None
    point = [point.x, point.y]

    for p in point_list:
        if p not in exclude:
            p_list = [p.x, p.y]
            dist = math.dist(point, p_list)
            if dist < smallest_distance:
                smallest_distance = dist
                closest_point = p_list

    return geometry.Point(closest_point[0], closest_point[1])

def normalize(data):
    normalizedData = (data-np.min(data))/(np.max(data)-np.min(data))*100
    return normalizedData