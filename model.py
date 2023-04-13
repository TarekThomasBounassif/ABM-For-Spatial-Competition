import env_generator
import firm
import env_generator
import numpy as np
import math
from typing import Tuple
import random

class Model:

    def __init__(self, simulation_params:dict, grid_params:dict, firm_params:dict) -> None:
        
        # Iterations passed
        self.iteration = 0

        # Params of the env and the firms
        self.grid_params = grid_params
        self.firm_params = firm_params
        self.simulation_params = simulation_params

        # Does model allow price changes
        self.with_price = self.simulation_params['WithPrice']

        # Setup grid and firms
        self.model_grid = self.setup_grid()
        self.firm_groups = list()
        self.firm_dict = dict()
        self.seed =  grid_params['Seed']
        random.seed(self.seed)

        
        # Create firm objects
        self.setup_firms()

    def setup_grid(self) -> env_generator.EnvGrid:
        """
        Initialise the Market / Grid / Env.
        """
        return env_generator.EnvGrid(
            self.grid_params['Size'],
            self.grid_params['Seed'],
            self.grid_params['Dim'],
            self.grid_params['Uniform'],
            self.grid_params['ClusterCount']
        )

    def setup_firms(self) -> None:
        """
        Initialise the firms.
        """
        for i in range(0, self.firm_params['FirmCount']):
            self.firm_groups.append(i)
            while True:
                starting_pos = self.model_grid.get_random_point(self.model_grid.system_grid)
                firm_locations = self.list_firm_locations()

                # Logic to ensure firms are not inisialised too close to eachother
                min_dist = math.inf
                for firm_pos in firm_locations:

                    # Ensure firms do not share the same starting position
                    if firm_pos == starting_pos:
                        continue
                    min_d = math.dist(starting_pos, firm_pos)
                    if min_d < min_dist:
                        min_dist = min_d
                if min_dist > (self.grid_params['Size'] / 6):
                    
                    # Either set to global shared initial price or random price.
                    if self.firm_params['randPrice']:
                        self.firm_dict[i] = firm.Firm(starting_pos, i, random.randint(10, 30))
                    else:
                        self.firm_dict[i] = firm.Firm(starting_pos, i, self.firm_params['StartPrice'])
                    break 

    def consider_position(self, firm_id:int, new_pos:list, price_change:int=None) -> Tuple[int, int]:
        """
        Allow a firm to consider its revenue at a new position with a price change.

        Args:
            firm_id (int): The ID of the firm currently considering a price and position change.
            new_pos (list): The new potential location of the firm.
            price_change (int, optional): The price change being considered, null if price changes are disabled.

        Returns:
            Tuple(int, int): The first element is the new revenue, and the second is the market share of the firm. 
            
        """

        new_market_share = self.assign_consumers(self.model_grid, new_pos, firm_id, price_change)
        new_market_share_for_firm = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in new_market_share[firm_id])

        if price_change != None:
            new_price = self.firm_dict[firm_id].price + price_change
            new_rev = new_market_share_for_firm * new_price
        else:
            new_rev = new_market_share_for_firm
        
        return (new_rev, new_market_share_for_firm, new_market_share)
    
    def assign_consumers(self, grid_in:env_generator.EnvGrid, new_pos:list, firm_id:int, price_change:int=None) -> dict:
        """
        Assign positions to their closest firm. 
        Create a market share for the case that a firm decides to move its position and change its price.

        Args:
            grid_in (env_generator.EnvGrid): The Market / Grid / Env. 
            new_pos (list): The new potential location of the firm.
            firm_id (int): The ID of the firm currently considering a price and position change.
            price_change (int, optional): The price change being considered, null if price changes are disabled.

        Returns:
            market_shares (dict): A dict where each key is a firm ID and each value is the list of positions that choose that firm.
        """

        # Setup market share for each firm
        market_shares = dict()
        for group in self.firm_groups:
            market_shares[group] = []

        # Assign each position to a firms market share
        for (i, j) in np.ndindex(grid_in.system_grid.shape):
            if price_change != None:
                closest_firm_id = self.get_optimal_firm([i,j], new_pos, firm_id, price_change)
            else:
                closest_firm_id = self.get_optimal_firm([i,j], new_pos, firm_id, None)

            # Update market share of each firm
            market_shares[closest_firm_id].append([i, j])

        return market_shares

    def get_optimal_firm(self, pos:list, new_pos:list, id:int, price_change:int=None) -> int:
        """
        Get the optimal firm for a given position. 
        Choose this optimal firm under the assumption that an input firm is considering a new position and price change.

        Args:
            new_pos (list): The position in the market currently picking its preffered firm.
            new_pos (list): The new potential location of the firm.
            id (int): The ID of the firm currently considering a price and position change.
            price_change (int, optional): The price change being considered, null if price changes are disabled.

        Returns:
            best_firm (int): The ID of a positions chosen firm. 
        """
        
        total_cost = math.inf
        best_firm = None

        for firm_id in self.firm_dict.keys():
            current_firm = self.firm_dict[firm_id]
            cost = math.inf

            # Choose the closest firm in the market where the input firm moves and changes price
            if price_change != None:
                if firm_id != id:
                    cost = math.dist(pos, current_firm.position) + current_firm.price
                else:
                    cost = math.dist(pos, new_pos) + current_firm.price + price_change

            # Choose the closest firm in the market where the input firm moves
            else:
                if firm_id != id:
                    cost = math.dist(pos, current_firm.position)
                else:
                    cost = math.dist(pos, new_pos)
            if cost < total_cost:
                    total_cost = cost
                    best_firm = firm_id
        return best_firm

    def list_firm_locations(self) -> list:
        """
        Return list of all positions.
        """
        return [self.firm_dict[firm_id].position for firm_id in self.firm_dict.keys()]
    
