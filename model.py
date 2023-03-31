import env_generator
import firm
import env_generator
import numpy as np
import math

class Model:


    def __init__(self, grid_params:dict, firm_params) -> None:

        self.grid_params = grid_params
        self.firm_params = firm_params

        self.model_grid = self.setup_grid()
        
        self.firm_groups = list()
        self.firm_list = list()
        self.firm_market_shares = dict()

        self.setup_firms()
    
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
            self.firm_market_shares[i] = []
            starting_pos = self.model_grid.get_random_point(self.model_grid.system_grid)
            self.firm_list.append(firm.Firm(starting_pos, i, self.firm_params['StartPrice']))
        self.log_system()

    def log_system(self) -> None:
        print("System Operating With {n} Firms.".format(n=self.firm_params['FirmCount']))
        for firm in self.firm_list:
            print(firm.log_firm())

    def evaluate_pos(self, grid_in:env_generator.EnvGrid, pos:list) -> int:
        """
        Return revenue firm would get IF positioned at pos
        """
        return 0
    
    def assign_consumers(self, grid_in:env_generator.EnvGrid):
        """
        Assign positions to their closest firm
        """
        self.clear_market_share()

        for (i,j) in np.ndindex(grid_in.shape):
            closest_firm = self.get_closest_firm([i,j])

            # Update market share of each firm
            self.firm_market_shares[closest_firm.group].append([i, j])
    
    def get_closest_firm(self, pos:list) -> firm.Firm:
        """
        Return closest firm to a pos
        """
        min_dist = math.inf
        closest_firm = None
        for firm in self.firm_list:
            dist = math.dist(pos, firm.position)
            if dist < min_dist:
                min_dist = dist
                closest_firm = firm
        return closest_firm

    def clear_market_share(self) -> None:
        """
        Clear market share for each firm. This method is used before a new evaluation.
        """
        for key in self.firm_market_shares:
            self.firm_market_shares[key] = []