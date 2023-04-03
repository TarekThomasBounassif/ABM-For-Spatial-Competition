import numpy as np
from matplotlib import pyplot as plt, cm, colors
import matplotlib as mpl
import env_generator
import model
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math


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

    fig, ax = plt.subplots(figsize=(8,5))
    ax.grid(True)

    # Plot the points
    plt.plot(x, y, '-', color='blue')
    plt.fill_between(x, y, color='blue', alpha=0.2)

    # Add labels and title 
    plt.xlabel('Position Along 1 Dimensional System', fontstyle='italic')
    plt.ylabel('Population Density', fontstyle='italic')
    plt.title('Firm Locations In 1 Dimensional System After {iter} Iterations'.format(iter=model_in.iteration),
               fontstyle='italic')

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

"""
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
"""

def plot_2d_system(model_in) -> None:
    
    grid_obj = model_in.model_grid
    
    fig = plt.figure(figsize=(8, 6))

    #fig.suptitle('Population Desinity Map With N = {n} Poulation Clusters'.format(n=3) , fontsize=16)

    ### FIGURE 1 - 3D PLOT ###

    ax = fig.add_subplot(111, projection='3d')
    ax.xaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.fill = False
    ax.zaxis.pane.set_edgecolor('white')
    ax.grid(False)

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
        
        ax.legend()

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
    ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
    ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(20))
    
    # Set axis labels
    ax.set_xlabel("Longitude", labelpad=10)
    ax.set_ylabel("Latitude", labelpad=10)
    ax.set_zlabel("Population Desnity", labelpad=10)
    ax.set_title('Firm Locations In 2 Dimensional System After {iter} Iterations'.format(iter=model_in.iteration),
               fontstyle='italic')

    # Set z-limit
    ax.set_zlim(0, 100)
    plt.margins(0)
    plt.savefig('plots/2d/2_d_non_uniform_system_{iter}.png'.format(iter=model_in.iteration))
    return None


def plot_price_history(model_in, exp_name:str) -> None:

    # Plot Price Evolution
    price_history_list = [
        model_in.firm_dict[firm_id].price_history for firm_id in model_in.firm_dict.keys()
    ]
    revenue_history_list = [
        model_in.firm_dict[firm_id].revenue_history for firm_id in model_in.firm_dict.keys()
    ]

    print(revenue_history_list)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=False)

    fig.suptitle('2 Dimensions, Non Uniform Population Desnity, I={iter} Iterations, N={firm_count}'.format(
        iter=model_in.iteration,
        firm_count=len(model_in.firm_dict.keys())
        ),
        fontstyle='oblique'
    )

    ax1.grid(True)
    for i, price_history in enumerate(price_history_list):
        print(price_history)
        ax1.plot(price_history, label=f"Firm : {i+1}")
    ax1.legend(fontsize=5)
    ax1.set_title('Price Evolution',
        fontstyle='italic'
    )
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Price")
    ax1.set_xmargin(0)
    ax1.set_ymargin(0)
    
    # Plot revenue evolution
    ax2.grid(True)
    for i, revenue_history in enumerate(revenue_history_list):
        ax2.plot([rev // 1000 for rev in revenue_history], label=f"Firm : {i+1}")
    ax2.set_title('Revenue Evolution (Thousands Of Units)',
        fontstyle='italic'
    )
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Revenue")
    ax2.set_xmargin(0)#
    ax2.set_ymargin(0)

    plt.savefig('plots/price_charts/{exp}.png'.format(exp=exp_name))

def get_distance_to_closest_firm(pos:list, firm_positions:list) -> None:
    """
    Get distance to the closest firm
    """
    closest_firm_position = min(firm_positions, key=lambda firm_pos: math.dist(firm_pos, pos))
    dist = math.dist(pos, closest_firm_position)
    min_dist = math.inf
    for firm in firm_positions:
        if firm != pos:
            dist = math.dist(pos, firm)
            if dist < min_dist:
                min_dist = dist
    return min_dist 

def desnity_map(model_in, exp_name):
    # create a 2D array with random values
    data = model_in.model_grid.system_grid

    # create a figure with two subplots side by side
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    fig.suptitle('2 Dimensions, Non Uniform Population Desnity, I={iter} Iterations, N={firm_count}'.format(
        iter=model_in.iteration,
        firm_count=len(model_in.firm_dict.keys())
        ),
        fontstyle='oblique'
    )

    # plot the density map on both subplots
    for ax in axs:
        ax.imshow(data, cmap='Greys', interpolation='nearest')
        ax.set_xlabel('Latitude')
        ax.set_ylabel('Longitude')

    # 0 Iterations
    for firm_id in model_in.firm_dict.keys():
        current_firm_start_pos = model_in.firm_dict[firm_id].position_history[0]
        firm_x = current_firm_start_pos[0]
        firm_y = current_firm_start_pos[1]
        axs[0].plot(
            firm_x,
            firm_y,
            marker='o',
            markersize=10,
            color=COLOR_DICT[firm_id],
            label="Firm {id}".format(id=firm_id)
        )
        axs[0].set_title('0 Iterations'.format(iter=model_in.iteration))

    # Max Iterations
    for firm_id in model_in.firm_dict.keys():
        firm_x = model_in.firm_dict[firm_id].position[0]
        firm_y = model_in.firm_dict[firm_id].position[1]
        axs[1].plot(
            firm_x,
            firm_y,
            marker='o',
            markersize=10,
            color=COLOR_DICT[firm_id],
            label="Firm {id}".format(id=firm_id)
        )
        x = []
        y = []

        
        for index, pos in enumerate(model_in.firm_dict[firm_id].position_history):
            x.append(pos[0])
            y.append(pos[1])

            if index % 2:
                pass
                # Plot every nth move for visibility
                axs[1].plot(
                    pos[0],
                    pos[1],
                    marker='o',
                    markersize=1.5,
                    color=COLOR_DICT[firm_id]
                )
        

        axs[1].plot(
            x,
            y,
            linestyle=':',
            color=COLOR_DICT[firm_id]
        )
        
        axs[1].set_title('{iter} Iterations'.format(iter=model_in.iteration))

    # add a legend to the left subplot
    axs[0].legend()

    # save the plot to a file
    plt.savefig('plots/heat_map/{exp}.png'.format(exp=exp_name))

    # show the plot
    plt.show()

def plot_distance_to_closest_firm(model_in, exp_name):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=False)

    # Plot Evolution Of Distance To Closest Firm
    ax2.grid(True)
    firm_locations = model_in.list_firm_locations()
    distance_lists = []
    for firm_id in model_in.firm_dict.keys():
        current_firm = model_in.firm_dict[firm_id]
        current_position_history = current_firm.position_history
        dist_to_closest_firm = []
        for pos in current_position_history:
            d = get_distance_to_closest_firm(pos, firm_locations)
            dist_to_closest_firm.append(d)
        distance_lists.append(dist_to_closest_firm)

    for i, distance_list in enumerate(distance_lists):
        ax2.plot(distance_list, label=f"Firm : {i+1}")
    ax2.legend()
    ax2.set_xlabel("Iteration")
    ax2.set_ylabel("Distance To Closest Firm")
    ax2.set_title('Distance To Closest Firm',
        fontstyle='italic'
    )

    ax2.set_xmargin(0)
    ax2.set_ymargin(0)

