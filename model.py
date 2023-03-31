import env_generator
import firm
import env_generator
import numpy as np
import math

class Model:

    def __init__(self, grid_params:dict, firm_params) -> None:

        self.iteration = 0
        self.grid_params = grid_params
        self.firm_params = firm_params

        self.model_grid = self.setup_grid()
        
        self.firm_groups = list()
        self.firm_dict = dict()
        
        self.setup_firms()
        self.firm_market_shares = self.assign_consumers()
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
            self.firm_dict[firm_id].update_rev(self.firm_market_shares, self.model_grid)
        
    def evaluate_pos(self, grid_in:env_generator.EnvGrid, pos:list) -> int:
        """
        Return revenue firm would get IF positioned at pos
        """
        return 0
    
    def consider_pos(self, firm_id, new_pos) -> None:
        """
        Allow a firm to consider its revenue at a new position
        """

        # Temporarily change firm location to new pos (Keeping track of old pos)
        print(self.firm_dict)
        old_pos = self.firm_dict[firm_id].position
        self.firm_dict[firm_id].position = new_pos

        # Create a market share with firms new pos
        new_market_share = self.assign_consumers()
        
        # Collect new revenue for a firm at this position
        new_rev = self.firm_dict[firm_id].evaluate_market_share(new_market_share, self.model_grid)

        # Change firm back to its original pos
        self.firm_dict[firm_id].position = old_pos

        return new_rev

    def assign_consumers(self) -> dict:
        """
        Assign positions to their closest firm
        """
        # Setup market share for each firm
        market_shares = dict()
        for group in self.firm_groups:
            market_shares[group] = []

        # Assign each position to a firms market share
        for (i,j) in np.ndindex(self.model_grid.system_grid.shape):
            closest_firm = self.get_closest_firm([i,j])

            # Update market share of each firm
            market_shares[closest_firm.group].append([i, j])
        return market_shares

    def get_closest_firm(self, pos:list) -> firm.Firm:
        """
        Return closest firm to a pos
        """
        min_dist = math.inf
        closest_firm = None
        for firm_id in self.firm_dict.keys():
            dist = math.dist(pos, self.firm_dict[firm_id].position)
            if dist < min_dist:
                min_dist = dist
                closest_firm = self.firm_dict[firm_id]
        return closest_firm
    
    def list_firm_locations(self) -> list:
        """
        Return list of all positions firms take
        """
        firm_positions = []
        for firm_id in self.firm_dict.keys():
            firm_positions.append(self.firm_dict[firm_id].position)
        return firm_positions

    def log_system(self) -> None:
        print("-"*100)
        print("System Status For Iteration Number : {iter}".format(iter=self.iteration))
        print("System Operating With {n} Firms.".format(n=self.firm_params['FirmCount']))
        for firm_id in self.firm_dict.keys():
            print(self.firm_dict[firm_id].log_firm())
            mshare = len(self.firm_market_shares[firm_id])
            print("Firm : {id} Controls : {mshare} Positions".format(id=firm_id, mshare=mshare))
        print("-"*100)