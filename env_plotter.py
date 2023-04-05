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
    ax.set_title('Firm Locations In 2 Dimensional System After {iter} Iterations'.format(iter=model_in.iteration),
               fontstyle='italic')

    # Set z-limit
    ax.set_zlim(0, 100)
    plt.margins(0)
    plt.savefig('plots/2d/2_d_non_uniform_system_{iter}.png'.format(iter=model_in.iteration))
    return None

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

def plot_2d_system_2(model_in) -> None:
    
    grid_obj = model_in.model_grid
    
    fig = plt.figure(figsize=(4, 4))
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
    #ax.set_title('2 Dimensional System After {iter} Iterations'.format(iter=model_in.iteration),
    #           fontstyle='italic')
    
    # Set z-limit
    ax.set_zlim(0, 100)
    plt.margins(0)
    plt.savefig('plots/2d/2_d_non_uniform_system_{iter}.png'.format(iter=model_in.iteration))
    return None

def plot_price_history_only(model_in, ax) -> None:

    price_history_list = [
        model_in.firm_dict[firm_id].price_history for firm_id in model_in.firm_dict.keys()
    ]
    max_price = 0
    for i, price_history in enumerate(price_history_list):
        max_p = max(price_history)
        if max_p > max_price:
            max_price = max_p
        ax.plot(price_history, label=f"Firm : {i+1}")
        ax.legend(fontsize=5)

    # Add a grid background
    ax.grid()

    # Set the x and y labels
    ax.set_xlabel("Iteration", fontweight='bold', fontstyle='italic')
    ax.set_ylabel("Price", fontweight='bold', fontstyle='italic')
    ax.set_xmargin(0)
    ax.set_ymargin(0)
    ax.grid(True)
    ax.set_ylim(-2, max_price * 1.1)
    

def plot_rev_history_only(model_in, ax) -> None:

    revenue_history_list = [
        model_in.firm_dict[firm_id].revenue_history for firm_id in model_in.firm_dict.keys()
    ]

    max_rev = 0
    for i, revenue_history in enumerate(revenue_history_list):
        max_r = max(revenue_history)
        if max_r > max_rev:
            max_rev = max_r
        ax.plot([rev // 1000 for rev in revenue_history], label=f"Firm : {i+1}")
        ax.legend(fontsize=5)

    ax.set_xlabel("Iteration", fontweight='bold', fontstyle='italic')
    ax.set_ylabel("Revenue (Thousands Of Units)", fontweight='bold', fontstyle='italic')
    ax.set_xmargin(0)
    ax.set_ymargin(0)
    ax.grid(True)
    ax.set_ylim(-2, (max_rev / 1000) * 1.1)

def plot_distance_to_closest_firm(model_in, ax):

    # Plot Evolution Of Distance To Closest Firm
    
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

    max_dist = 0
    for i, distance_list in enumerate(distance_lists):
        max_d = max(distance_list)
        if max_d > max_dist:
            max_dist = max_d
        ax.plot(distance_list, label=f"Firm : {i+1}")


    ax.legend()
    ax.set_xlabel("Iteration", fontweight='bold', fontstyle='italic')
    ax.set_ylabel("Distance To Closest Firm", fontweight='bold', fontstyle='italic')
    ax.grid(True)
    ax.set_xmargin(0)
    ax.set_ymargin(0)
    ax.set_ylim(-2, max_dist * 1.1)

def plot_combine(model_in):
    # Create the figure and subplots
    #fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=False)
    fig, axs = plt.subplots(2, 2, figsize=(10, 10), sharey=False)

    # Plot the price history in the first subplot
    plot_price_history_only(model_in, ax=axs[0, 0])

    # Plot the revenue history in the second subplot
    plot_rev_history_only(model_in, ax=axs[0, 1])

    plot_distance_to_closest_firm(model_in, ax=axs[1, 0])

    fig.set_facecolor('0.9')
    fig.set_edgecolor('black')
    # Show the plot
    plt.savefig('plots/price_charts/{exp}.png'.format(exp="1"))
    plt.show()





