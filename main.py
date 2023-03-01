import grid_generator
import plotter

"""
Good Seeds To Try:
739
676
243
25
521
8
"""

g = grid_generator.grid_generator(100, 8)
plotter.graph_grid_2d(g)