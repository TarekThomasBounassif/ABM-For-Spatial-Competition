import env_generator
import firm
import env_generator
import numpy as np
import math
import config

class Model:

    def __init__(self, grid_params:dict, firm_params) -> None:
        
        # Iterations passed
        self.iteration = 0

        # Params of the env and the firms
        self.grid_params = grid_params
        self.firm_params = firm_params

        # Does model allow price changes
        self.with_price = config.simulation_params['WithPrice']

        # Setup grid and firms
        self.model_grid = self.setup_grid()
        self.firm_groups = list()
        self.firm_dict = dict()
        
        # Create firm objects
        self.setup_firms()

        # Setup initial
        firm_start_positions = self.list_firm_locations()
        self.firm_market_shares = self.assign_consumers_new(firm_start_positions, self.model_grid)
        self.update_firm_revenue()

    def setup_grid(self) -> env_generator.EnvGrid:
        return env_generator.EnvGrid(
            self.grid_params['Size'],
            self.grid_params['Seed'],
            self.grid_params['Dim'],
            self.grid_params['Uniform'],
            self.grid_params['ClusterCount']
        )

    def setup_firms(self) -> None:
        for i in range(0, self.firm_params['FirmCount']):
            self.firm_groups.append(i)
            while True:
                starting_pos = self.model_grid.get_random_point(self.model_grid.system_grid)
                if starting_pos not in self.list_firm_locations():
                    self.firm_dict[i] = firm.Firm(starting_pos, i, self.firm_params['StartPrice'])
                    break 

    def update_firm_revenue(self) -> None:
        for firm_id in self.firm_dict.keys():
            self.firm_dict[firm_id].initialise_rev(self.firm_market_shares, self.model_grid)
    
    def consider_pos_new(self, firm_id, new_pos) -> None:
        """
        Allow a firm to consider its revenue at a new position
        """

        old_firm_list = []
        for id in self.firm_groups:
            old_firm_list.append(self.firm_dict[id].position)
        
        new_firm_list = old_firm_list.copy()
        new_firm_list[firm_id] = new_pos


        old_market_share = self.assign_consumers_new(old_firm_list, self.model_grid)
        old_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in old_market_share[firm_id])
        
        new_market_share = self.assign_consumers_new(new_firm_list, self.model_grid)
        new_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in new_market_share[firm_id])

        return new_rev, old_rev

    def consider_pos_with_price(self, firm_id, new_pos, price_change) -> None:
        """
        Allow a firm to consider its revenue at a new position
        """

        old_firm_list = []
        for id in self.firm_groups:
            old_firm_list.append(self.firm_dict[id].position)
        
        new_firm_list = old_firm_list.copy()
        new_firm_list[firm_id] = new_pos

        current_price = self.firm_dict[firm_id].price
        new_price = current_price + price_change

        #old_market_share = self.assign_consumers_with_price(old_firm_list, self.model_grid, firm_id, price_change)
        old_market_share = self.assign_consumers_with_price_new(self.model_grid, firm_id, new_pos, price_change)
        old_market_share_size = len(old_market_share)
        old_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in old_market_share[firm_id]) * current_price
        
        #new_market_share = self.assign_consumers_with_price(new_firm_list, self.model_grid, firm_id, price_change)
        new_market_share = self.assign_consumers_with_price_new(self.model_grid, new_pos, firm_id, price_change)
        new_market_share_size = len(new_market_share)
        new_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in new_market_share[firm_id]) * new_price

        return new_rev, new_market_share_size, old_rev, old_market_share_size
    
    def assign_consumers_new(self, firms:list, grid_in:env_generator.EnvGrid) -> dict:

        """
        Assign positions to their closest firm
        """

        # Setup market share for each firm
        market_shares = dict()
        for group in self.firm_groups:
            market_shares[group] = []

        # Assign each position to a firms market share
        for (i,j) in np.ndindex(grid_in.system_grid.shape):

            closest_firm_id = self.get_closest_firm_new([i,j], firms)

            # Update market share of each firm
            market_shares[closest_firm_id].append([i, j])
        return market_shares
    
    def assign_consumers_with_price(self, firms:list, grid_in:env_generator.EnvGrid, firm_id:int, price_change:int) -> dict:
       
        """
        Assign positions to their closest firm
        """

        # Setup market share for each firm
        market_shares = dict()
        for group in self.firm_groups:
            market_shares[group] = []

        # Assign each position to a firms market share
        for (i,j) in np.ndindex(grid_in.system_grid.shape):
            
            closest_firm_id = self.get_optimal_firm([i,j], firms, firm_id, price_change)
            # Update market share of each firm
            market_shares[closest_firm_id].append([i, j])
        return market_shares
    
    def assign_consumers_with_price_new(self, grid_in:env_generator.EnvGrid, new_pos:list, firm_id:int, price_change:int) -> dict:
       
        """
        Assign positions to their closest firm
        """

        # Setup market share for each firm
        market_shares = dict()
        for group in self.firm_groups:
            market_shares[group] = []

        # Assign each position to a firms market share
        for (i,j) in np.ndindex(grid_in.system_grid.shape):
            
            closest_firm_id = self.get_optimal_firm_new([i,j], new_pos, firm_id, price_change)
            # Update market share of each firm
            market_shares[closest_firm_id].append([i, j])
        return market_shares
    
    def get_closest_firm_new(self, pos:list, firms:list) -> firm.Firm:
        
        """
        Return closest firm to a pos
        """
        
        min_dist = math.inf
        closest_firm = None
        for index, firm_position in enumerate(firms):
            dist = math.dist(pos, firm_position)
            if dist < min_dist:
                min_dist = dist
                closest_firm = index
        return closest_firm
    
    def get_optimal_firm(self, pos:list, firms:list, firm_id:int, price_change:int) -> int:
       
        """
        Return closest firm to a pos
        """
        
        total_cost = math.inf
        best_firm = None
        for index, firm_position in enumerate(firms):
            move_cost = math.dist(pos, firm_position)
            if index != firm_id:
                price = self.firm_dict[index].price
            else:
                price = self.firm_dict[index].price + price_change
            net_cost = move_cost + price
            if net_cost < total_cost:
                total_cost = net_cost
                best_firm = index

        return best_firm

    def get_optimal_firm_new(self, pos:list, new_pos:list, id:int, price_change:int) -> int:
       
        """
        Return the best firm choice to a pos, given a potential new location and price change for a firm.
        This method will be used to evaluate a change in price and loction, this method represents the new best
        firm from a position IF a firm decides to alter its position and price. 
        """
        
        total_cost = math.inf
        best_firm = None

        for firm_id in self.firm_dict.keys():
            current_firm = self.firm_dict[firm_id]
            if firm_id != id:
                cost = math.dist(pos, current_firm.position) + current_firm.price
            else:
                cost = math.dist(pos, new_pos) + current_firm.price + price_change
            if cost < total_cost:
                total_cost = cost
                best_firm = firm_id 

        return best_firm

    def list_firm_locations(self) -> list:
        """
        Return list of all positions firms take
        """
        firm_positions = []
        for firm_id in self.firm_dict.keys():
            firm_positions.append(self.firm_dict[firm_id].position)
        return firm_positions

    def display_firms(self, firms:dict) -> None:
        """
        Print out firm info
        """
        print("="*100)
        for id in firms:
            print("Firm ID : " + str(id) + " Pos : " + str(firms[id].position))

    def log_system(self) -> None:
        print("-"*100)
        print("System Status For Iteration Number : {iter}".format(iter=self.iteration))
        print("System Operating With {n} Firms.".format(n=self.firm_params['FirmCount']))
        for firm_id in self.firm_dict.keys():
            print(self.firm_dict[firm_id].log_firm())
            mshare = len(self.firm_market_shares[firm_id])
            print("Firm : {id} Controls : {mshare} Positions".format(id=firm_id, mshare=mshare))
        print("-"*100)