import numpy as np
import random
import math
from matplotlib import pyplot as plt, cm, colors
from shapely import geometry
from mpl_toolkits.mplot3d import Axes3D
import scipy.stats as stats
import matplotlib as mpl
import grid_generator

def graph_grid_2d(grid_obj) -> None:

    fig, ax = plt.subplots()
    plot = ax.imshow(grid_obj.grid_master)

    print(grid_obj.grid_master)
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)  # turn off summarization, line-wrapping
    with open("test", 'w') as f:
        f.write(np.array2string(grid_obj.grid_master, separator=', '))
    cbar = fig.colorbar(plot, ax=ax, shrink=1)
    cbar.set_ticks([0, 50, 100])
    cbar.set_ticklabels(['0', '50', '100'])
    ax.set_title("Population Desity Map")
    fig.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()    
    
    return None

def graph_grid_3d(grid_obj) -> None:
    
    fig = plt.figure(figsize=(7, 5))

    #fig.suptitle('Population Desinity Map With N = {n} Poulation Clusters'.format(n=3) , fontsize=16)

    ### FIGURE 1 - 3D PLOT ###

    ax = fig.add_subplot(111, projection='3d')
    ax.xaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.fill = False
    ax.zaxis.pane.set_edgecolor('white')
    ax.grid(False)

    ticks = [numb for numb in range(0, grid_obj.grid_size)]

    # Create meshgrid
    X, Y = np.meshgrid(ticks, ticks)
    plot = ax.plot_surface(X=X, Y=Y, Z=grid_obj.grid_master, cmap='YlGnBu', vmin=0, vmax=100, alpha=0.9)

    # Plot surface
    for c in grid_obj.cluster_peaks:
        ax.scatter(c[0], c[1], 100, color="Red")

    # Plut cluster peaks
    for c in grid_obj.cluster_peaks:
        ax.plot([c[0],c[0]],[c[1],c[1]], [0, 150], 'k--', alpha=0.95, linewidth=1)

    # Plot polygon / perimiter
    x_poly,y_poly = grid_obj.polygon.exterior.xy
    ax.plot(x_poly,y_poly, color='Blue', linestyle='dashed')

    # Adjust plot view
    ax.view_init(elev=40, azim=225)
    ax.dist=11

    # Add colorbar
    cbar = fig.colorbar(plot, ax=ax, shrink=0.3)
    cbar.set_ticks([0, 50, 100])
    cbar.set_ticklabels(['0', '50', '100'])

    # Set tick marks
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
    

    # Set axis labels
    ax.set_xlabel("Longitude", labelpad=10)
    ax.set_ylabel("Latitude", labelpad=10)
    ax.set_zlabel("Population Desnity", labelpad=10)

    # Set z-limit
    ax.set_zlim(0, 100)

    plt.show()
    return None

