import numpy as np
from matplotlib import pyplot as plt, cm, colors
import matplotlib as mpl
import env_generator
import model
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math
from matplotlib.path import Path
import matplotlib.pyplot as plt
import numpy as np



COLOR_DICT = {
    0: plt.cm.tab10(0),
    1: plt.cm.tab10(1),
    2: plt.cm.tab10(2),
    3: plt.cm.tab10(3),
    4: plt.cm.tab10(4),
    5: plt.cm.tab10(5),
    6: plt.cm.tab10(6),
    7: plt.cm.tab10(7),
    8: plt.cm.tab10(8),
    9: plt.cm.tab10(9),
    10: plt.cm.tab10(10)
}

def plot_1d_system(model_in:model.Model, with_firms:bool) -> None:

    data = [(index[1], value) for index, value in np.ndenumerate(model_in.model_grid.system_grid)]
    x, y = zip(*data)

    fig, ax = plt.subplots(figsize=(8,6))
    ax.grid(True)

    # Plot the points
    plt.plot(x, y, '-', color='blue')
    plt.fill_between(x, y, color='blue', alpha=0.2)

    # Add labels and title 
    plt.xlabel('Position Along 1 Dimensional System')
    plt.ylabel('Population Density')
    #plt.title('1 Dimensional System After {iter} Iterations'.format(iter=model_in.iteration), fontstyle='italic')

    # Modify ticks
    ticks = [i for i in range(0, model_in.model_grid.size + 1) if i%10==0]
    plt.xlim([min(x), max(x)])
    plt.ylim([min(y), max(y)])
    plt.xticks(ticks, rotation=45)
    plt.yticks(ticks)

    if with_firms:
        for firm_id in model_in.firm_dict.keys():
            ax.axvline(
                x=model_in.firm_dict[firm_id].position[1],
                color=COLOR_DICT[firm_id],
                linestyle='--',
                label="Firm {id}".format(id=firm_id))
            
        ax.legend()

    plt.margins(0)
    plt.savefig('plots/1d/1_d_non_uniform_system_{iter}.png'.format(iter=model_in.iteration))

def plot_2d_system(model_in) -> None:
    
    grid_obj = model_in.model_grid
    
    fig = plt.figure(figsize=(8, 6))

    #fig.suptitle('Population Desinity Map With N = {n} Poulation Clusters'.format(n=3) , fontsize=16)

    ### FIGURE 1 - 3D PLOT ###

    ax = fig.add_subplot(111, projection='3d')

    ticks = [numb for numb in range(0, grid_obj.size)]

    # Create meshgrid
    X, Y = np.meshgrid(ticks, ticks)
    
    for firm_id in model_in.firm_dict.keys():

        ax.plot(
            [model_in.firm_dict[firm_id].position[0],model_in.firm_dict[firm_id].position[0]],
            [model_in.firm_dict[firm_id].position[1],model_in.firm_dict[firm_id].position[1]],
            [0, 150],
            'k--',
            alpha=0.95,
            linewidth=1,
            color=COLOR_DICT[firm_id],
            zorder=3
        )
            
        ax.scatter(
            model_in.firm_dict[firm_id].position[0], 
            model_in.firm_dict[firm_id].position[1],
            100,
            color=COLOR_DICT[firm_id],
            label="Firm {id}".format(id=firm_id),
            zorder=2
        )
        
        ax.legend(fontsize=7)

    plot = ax.plot_surface(
        X=X,
        Y=Y,
        Z=grid_obj.system_grid,
        cmap='YlGnBu',
        vmin=0,
        vmax=100, 
        alpha=0.9,
        zorder=0
    )
    ax.computed_zorder = False
    # Adjust plot view
    ax.view_init(elev=40, azim=225)
    ax.dist=11

    # Set tick marks
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    
    # Set axis labels
    ax.set_xlabel("Longitude", labelpad=10)
    ax.set_ylabel("Latitude", labelpad=10)
    ax.set_zlabel("Population Desnity", labelpad=10)
    #ax.set_title('Firm Locations In 2 Dimensional System After {iter} Iterations'.format(iter=model_in.iteration),
    #           fontstyle='italic')

    # Set z-limit
    ax.set_zlim(0, 100)
    plt.margins(0)
    plt.savefig('plots/2d/2_d_non_uniform_system_{iter}.png'.format(iter=model_in.iteration))
    return None

def plot_2d_system_2(model_in) -> None:
    
    grid_obj = model_in.model_grid
    
    fig = plt.figure(figsize=(5, 5))
    #fig.subplots_adjust(left=0.4, right=0.9, bottom=0.1, top=0.9, wspace=0.2, hspace=0.2)

    #fig.suptitle('Population Desinity Map With N = {n} Poulation Clusters'.format(n=3) , fontsize=16)

    ### FIGURE 1 - 3D PLOT ###

    ax = fig.add_subplot(111, projection='3d')

    ticks = [numb for numb in range(0, grid_obj.size)]

    # Create meshgrid
    X, Y = np.meshgrid(ticks, ticks)
    
    for firm_id in model_in.firm_dict.keys():

        ax.plot(
            [model_in.firm_dict[firm_id].position[0],model_in.firm_dict[firm_id].position[0]],
            [model_in.firm_dict[firm_id].position[1],model_in.firm_dict[firm_id].position[1]],
            [0, 150],
            'k--',
            alpha=0.95,
            linewidth=1,
            color=COLOR_DICT[firm_id],
            zorder=3
        )
            
        ax.scatter(
            model_in.firm_dict[firm_id].position[0], 
            model_in.firm_dict[firm_id].position[1],
            100,
            color=COLOR_DICT[firm_id],
            label="Firm {id}".format(id=firm_id),
            zorder=2
        )
        
        ax.legend(fontsize=7)

    plot = ax.plot_surface(
        X=X,
        Y=Y,
        Z=grid_obj.system_grid,
        cmap='YlGnBu',
        vmin=0,
        vmax=100, 
        alpha=0.9,
        zorder=0
    )
    ax.computed_zorder = False
    ax.view_init(elev=40, azim=225)
    ax.dist=11
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(10))
    ax.set_xlabel("Longitude", labelpad=10)
    ax.set_ylabel("Latitude", labelpad=10)
    ax.set_zlabel("Population Desnity", labelpad=10)
    ax.set_zlim(0, 100)
    fig.set_facecolor('0.9')
    fig.set_edgecolor('black')
    ax.legend(title="Firms", bbox_to_anchor=(1.05, 0.5), loc='center left')
    plt.margins(0)
    plt.savefig('plots/2d/2_d_non_uniform_system_{iter}.png'.format(iter=model_in.iteration))
    return None

