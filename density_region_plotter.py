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

def desnity_map_test(model_in, axs):

    # create a 2D array with random values
    data = model_in.model_grid.system_grid

    # Points iterations 0
    for firm_id in model_in.firm_dict.keys():
        current_firm_start_pos = model_in.firm_dict[firm_id].position_history[0]
        firm_x = current_firm_start_pos[0]
        firm_y = current_firm_start_pos[1]

        # Plot 1
        axs[0, 0].plot(
            firm_x,
            firm_y,
            marker='o',
            markersize=10,
            color=COLOR_DICT[firm_id],
            label="Firm {id}".format(id=firm_id),
            markeredgecolor='black'
        )
        axs[0, 0].set_title('Market Positions : 0 Iterations', fontstyle='italic', weight='bold')

        # Plot 3
        axs[1, 0].plot(
            firm_x,
            firm_y,
            marker='o',
            markersize=10,
            color=COLOR_DICT[firm_id],
            label="Firm {id}".format(id=firm_id),
            markeredgecolor='black'
        )

    # Points iterations max
    for firm_id in model_in.firm_dict.keys():
        firm_x = model_in.firm_dict[firm_id].position[0]
        firm_y = model_in.firm_dict[firm_id].position[1]

        # Plot 2
        axs[0, 1].plot(
            firm_x, 
            firm_y, 
            marker='o', 
            markersize=10, 
            color=COLOR_DICT[firm_id], 
            label="Firm {id}".format(id=firm_id),
            markeredgecolor='black'
        )
        x = []
        y = []

        for pos in model_in.firm_dict[firm_id].position_history:
            x.append(pos[0])
            y.append(pos[1])
        axs[0, 1].plot(x, y, linestyle=':', color=COLOR_DICT[firm_id])
        axs[0, 1].set_title('Market Positions : {iter} Iterations'.format(iter=model_in.iteration), fontstyle='italic', weight='bold')

        # Plot 4
        axs[1, 1].plot(
            firm_x, 
            firm_y, 
            marker='o', 
            markersize=10, 
            color=COLOR_DICT[firm_id], 
            label="Firm {id}".format(id=firm_id),
            markeredgecolor='black'
        )

    # Density Plot 1
    axs[0, 0].imshow(data, cmap='Greys', interpolation='nearest')
    axs[0, 0].set_xlabel('Latitude', fontstyle='italic')
    axs[0, 0].set_ylabel('Longitude', fontstyle='italic')
    axs[0, 0].invert_yaxis()
    axs[0, 0].set_xlim(0, model_in.grid_params['Size'])
    axs[0, 0].set_ylim(0, model_in.grid_params['Size'])

    # Density Plot 2
    axs[0, 1].imshow(data, cmap='Greys', interpolation='nearest')
    axs[0, 1].set_xlabel('Latitude', fontstyle='italic')
    axs[0, 1].set_ylabel('Longitude', fontstyle='italic')
    axs[0, 1].invert_yaxis()
    axs[0, 1].set_xlim(0, model_in.grid_params['Size'])
    axs[0, 1].set_ylim(0, model_in.grid_params['Size'])

    

def plot_regions(sim_in, axs):

    first_market_share = sim_in.market_share_list_history[0]
    final_market_share = sim_in.market_share_list_history[-1]

    points_list_first = [first_market_share[firm_id] for firm_id in first_market_share.keys()]
    points_list_last = [final_market_share[firm_id] for firm_id in final_market_share.keys()]

    # Fig 1
    for index, list in enumerate(points_list_first):
        color = COLOR_DICT[index]
        axs[1, 0].scatter(*zip(*list), c=color, edgecolors='none', alpha=0.3)
    axs[1, 0].set_xmargin(0)
    axs[1, 0].set_ymargin(0)
    axs[1, 0].set_xlabel('Latitude', fontstyle='italic')
    axs[1, 0].set_ylabel('Longitude', fontstyle='italic')
    axs[1, 0].set_xlim(0, sim_in.grid_params['Size'])
    axs[1, 0].set_ylim(0, sim_in.grid_params['Size'])
    axs[1, 0].set_title('Market Share : 0 Iterations', fontstyle='italic', weight='bold')

    # Fig 2
    for index, list in enumerate(points_list_last):
        color = COLOR_DICT[index]
        axs[1, 1].scatter(*zip(*list), c=color, edgecolors='none', alpha=0.3)
    axs[1, 1].set_xmargin(0)
    axs[1, 1].set_ymargin(0)
    axs[1, 1].set_xlabel('Latitude', fontstyle='italic')
    axs[1, 1].set_ylabel('Longitude', fontstyle='italic')
    axs[1, 1].set_xlim(0, sim_in.grid_params['Size'])
    axs[1, 1].set_ylim(0, sim_in.grid_params['Size'])
    axs[1, 1].set_title('Market Share : {iter} Iterations'.format(iter=sim_in.model_env.iteration), fontstyle='italic', weight='bold')

    print(sim_in.max_iters)

def plot_combine_density(sim_in):

    model_in = sim_in.model_env

    # Create the figure and subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 10), sharey=False)

    # Plot the price history in the first subplot
    desnity_map_test(model_in, axs)

    plot_regions(sim_in, axs)

    fig.set_facecolor('0.9')
    fig.set_edgecolor('black')
    axs[0, 1].legend(title="Firms", bbox_to_anchor=(1.05, 0.5), loc='center left')

    # Show the plot
    plt.savefig('plots/price_charts/{exp}.png'.format(exp="1"))
    plt.show()


