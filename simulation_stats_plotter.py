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

def plot_price_history(model_in, axs) -> None:
  
    max_price = 0
    for firm_id in model_in.firm_dict.keys():
        current_firm = model_in.firm_dict[firm_id]
        price_history = current_firm.price_history
        max_p = max(price_history)
        if max_p > max_price:
            max_price = max_p
        axs[0,0].plot(
            price_history,
            label="Firm {id}".format(id=firm_id),
            color=COLOR_DICT[firm_id]
        )

    # Add a grid background
    axs[0, 0].grid()
    axs[0, 0].set_xlabel("Iteration", fontstyle='italic')
    axs[0, 0].set_ylabel("Price", fontstyle='italic')
    axs[0, 0].set_title('Price', fontstyle='italic', weight='bold')
    axs[0, 0].set_xmargin(0)
    axs[0, 0].set_ymargin(0)
    axs[0, 0].grid(True)
    axs[0, 0].set_ylim(-1, max_price * 1.02)
    axs[0, 0].set_xlim(0, 50)
    

def plot_rev_history(model_in, axs) -> None:

    max_rev = 0
    for firm_id in model_in.firm_dict.keys():
        current_firm = model_in.firm_dict[firm_id]
        rev_history = current_firm.revenue_history
        max_r = max(rev_history)
        rev_history = [round(rev / 1000) for rev in rev_history]
        if max_r > max_rev:
            max_rev = max_r
        axs[0,1].plot(
            rev_history,
            label="Firm {id}".format(id=firm_id),
            color=COLOR_DICT[firm_id]
        )

    axs[0, 1].set_xlabel("Iteration", fontstyle='italic')
    axs[0, 1].set_ylabel("Revenue (Thousands Of Units)", fontstyle='italic')
    axs[0, 1].set_title('Revenue', fontstyle='italic', weight='bold')
    axs[0, 1].set_xmargin(0)
    axs[0, 1].set_ymargin(0)
    axs[0, 1].grid(True)
    axs[0, 1].set_ylim(-1, (max_rev / 1000) * 1.02)
    axs[0, 1].set_xlim(0, 50)

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

def plot_distance_to_closest_firm(model_in, axs):

    # Plot Evolution Of Distance To Closest Firm
    
    final_dict_to_plot = dict()
    
    distance_lists = dict()
    for firm_id in model_in.firm_dict.keys():
        distance_lists[firm_id] = model_in.firm_dict[firm_id].position_history
        final_dict_to_plot[firm_id] = []

    for i in range(0, model_in.iteration):
        firm_locations = [distance_lists[firm_id][i] for firm_id in distance_lists.keys()]
        for firm_id in distance_lists.keys():
            position_at_iteration = distance_lists[firm_id][i]
            dist_to_closest_firm = get_distance_to_closest_firm(position_at_iteration, firm_locations)
            final_dict_to_plot[firm_id].append(dist_to_closest_firm)

    max_dist = 0
    for firm_id in final_dict_to_plot.keys():
        d_list = final_dict_to_plot[firm_id]
        max_d = max(d_list)
        if max_d > max_dist:
            max_dist = max_d
        axs[1,0].plot(
            d_list,
            label="Firm {id}".format(id=firm_id),
            color=COLOR_DICT[firm_id]
        )

    axs[1,0].set_xlabel("Iteration", fontstyle='italic')
    axs[1,0].set_ylabel("Distance", fontstyle='italic')
    axs[1,0].set_title('Distance To Closest Firm', fontstyle='italic', weight='bold')
    axs[1,0].grid(True)
    axs[1,0].set_xmargin(0)
    axs[1,0].set_ymargin(0)
    axs[1,0].set_ylim(-1, max_dist)

def plot_mshare_ratio(sim_in, axs) -> None:


    total_market = sim_in.model_env.model_grid.total_market_size
    grid = sim_in.model_env.model_grid.system_grid

    market_share_lists = dict()
    for firm_id in sim_in.model_env.firm_dict.keys():
        market_share_lists[firm_id] = []

    for i in range(0, sim_in.model_env.iteration):
        current_mshare = sim_in.market_share_list_history[i]

        for firm_id in current_mshare.keys():
            mshare = sum([grid[pos[1], pos[0]] for pos in current_mshare[firm_id]])
            market_share_lists[firm_id].append(round((mshare / total_market) * 100))

    for firm_id in market_share_lists.keys():      
        axs[1,1].plot(
            market_share_lists[firm_id],
            label="Firm {id}".format(id=firm_id),
            color=COLOR_DICT[firm_id]
        )

    axs[1,1].set_xlabel("Iteration", fontstyle='italic')
    axs[1,1].set_ylabel("Percentage Of Total Market Share", fontstyle='italic')
    axs[1,1].set_title('Proportion Of Market Share', fontstyle='italic', weight='bold')
    axs[1,1].grid(True)
    axs[1,1].set_xmargin(0)
    axs[1,1].set_ymargin(0)
    #axs[1,1].set_ylim(-1,  100)

def plot_combine(sim_in):

    fig, axs = plt.subplots(2, 2, figsize=(10, 10), sharey=False)

    plot_price_history(sim_in.model_env, axs)
    plot_rev_history(sim_in.model_env, axs)
    plot_distance_to_closest_firm(sim_in.model_env, axs)
    plot_mshare_ratio(sim_in, axs)

    fig.set_facecolor('0.9')
    fig.set_edgecolor('black')
    axs[0, 1].legend(title="Firms", bbox_to_anchor=(1.05, 0.5), loc='center left')

    plt.savefig('plots/price_charts/{exp}.png'.format(exp="1"))
    plt.show()


def plot_distance_trends(sim_list:list) -> None:
    # Plot Evolution Of Distance To Closest Firm

    lines_to_plot = []
    x_values = list()

    for sim in sim_list:
        curent_model = sim.model_env

        # List of distances for a sim

        final_dict_to_plot = dict()
        
        distance_lists = dict()
        for firm_id in curent_model.firm_dict.keys():
            distance_lists[firm_id] = curent_model.firm_dict[firm_id].position_history
            final_dict_to_plot[firm_id] = []

        for i in range(0, curent_model.iteration):
            firm_locations = [distance_lists[firm_id][i] for firm_id in distance_lists.keys()]
            for firm_id in distance_lists.keys():
                position_at_iteration = distance_lists[firm_id][i]
                dist_to_closest_firm = get_distance_to_closest_firm(position_at_iteration, firm_locations)
                final_dict_to_plot[firm_id].append(dist_to_closest_firm)

        lists = [final_dict_to_plot[firm_id] for firm_id in final_dict_to_plot.keys()]
        final_list_for_sim = []
        for i in range(0, curent_model.iteration):
            current_val = 0
            for l in lists:
                current_val += l[i]
            final_list_for_sim.append(current_val)
        final_list_for_sim = [val / len(final_dict_to_plot.keys()) for val in final_list_for_sim]
        lines_to_plot.append(final_list_for_sim)

        x_values = [i for i in range(0, curent_model.iteration)]

    for line in lines_to_plot:
        plt.plot(x_values, line)

    plt.title('The Average Distance To Closest Firm For {x} Simulations'.format(x=len(sim_list)), fontweight='bold', fontstyle='italic')
    plt.xlabel('Iterations', fontstyle='italic')
    plt.ylabel('Avergare Distance To Closest Firm', fontstyle='italic')
    fig = plt.gcf()
    fig.patch.set_facecolor('lightgrey')
    plt.margins(0)
    plt.grid(True)
    plt.show()
        
   
   
