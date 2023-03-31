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
        self.firm_market_shares = self.assign_consumers(self.firm_dict, self.model_grid)
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
        old_pos = self.firm_dict[firm_id].position

        firms = dict()
        for id in self.firm_dict.keys():
            if id == firm_id:
                firms[id] = firm.Firm(new_pos, id, 0)
            else:
                firms[id] = firm.Firm(old_pos, id, 0)

        old_market_share = self.assign_consumers(self.firm_dict, self.model_grid)
        old_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in old_market_share[firm_id])
        
        new_market_share = self.assign_consumers(firms, self.model_grid)
        new_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in new_market_share[firm_id])

        if firm_id == 0 and self.iteration == 1:
            print("-"*100)
            print("Current Firm : {id}".format(id=firm_id))
            self.display_firms(self.firm_dict)
            self.display_firms(firms)
            print("Old Rev : {old_rev}".format(old_rev=old_rev))
            print("New Rev : {new_rev}".format(new_rev=new_rev))
            print("Old Pos = " + str(old_pos))
            print("New Pos = " + str(new_pos))
            print("Old M share : " + str(len(old_market_share[firm_id])))
            print(sorted(old_market_share[firm_id], key=lambda x: x[1]))
            print("New M share : " + str(len(new_market_share[firm_id])))
            print(sorted(new_market_share[firm_id], key=lambda x: x[1]))
            print("-"*100)

        return new_rev
    

    def consider_pos_new(self, firm_id, new_pos) -> None:
        """
        Allow a firm to consider its revenue at a new position
        """

        # Temporarily change firm location to new pos (Keeping track of old pos)
        old_pos = self.firm_dict[firm_id].position

        old_firm_list = []
        for id in self.firm_groups:
            old_firm_list.append(self.firm_dict[id].position)
        
        new_firm_list = old_firm_list.copy()
        new_firm_list[firm_id] = new_pos

        old_market_share = self.assign_consumers_new(old_firm_list, self.model_grid)
        old_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in old_market_share[firm_id])
        
        new_market_share = self.assign_consumers_new(new_firm_list, self.model_grid)
        new_rev = sum(self.model_grid.system_grid[pos[0], pos[1]] for pos in new_market_share[firm_id])

        if firm_id == 1 and self.iteration < 10:
            print("-"*100)
            print("Current Firm : {id}".format(id=firm_id))
            print(old_firm_list)
            print(new_firm_list)
            print("Old Rev : {old_rev}".format(old_rev=old_rev))
            print("New Rev : {new_rev}".format(new_rev=new_rev))
            print("Old Pos = " + str(old_pos))
            print("New Pos = " + str(new_pos))
            print("Old M share : " + str(len(old_market_share[firm_id])))
            print(sorted(old_market_share[firm_id], key=lambda x: x[1]))
            print("New M share : " + str(len(new_market_share[firm_id])))
            print(sorted(new_market_share[firm_id], key=lambda x: x[1]))
            print("-"*100)

        return new_rev, old_rev
    
    def assign_consumers(self, firms:dict, grid_in:env_generator.EnvGrid) -> dict:
        """
        Assign positions to their closest firm
        """
        # Setup market share for each firm
        market_shares = dict()
        for group in self.firm_groups:
            market_shares[group] = []

        # Assign each position to a firms market share
        for (i,j) in np.ndindex(grid_in.system_grid.shape):
            closest_firm_id = self.get_closest_firm([i,j], firms)
            # Update market share of each firm
            market_shares[closest_firm_id].append([i, j])
        return market_shares
    
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

    def get_closest_firm(self, pos:list, firms:dict) -> firm.Firm:
        """
        Return closest firm to a pos
        """
        min_dist = math.inf
        closest_firm = None
        for firm_id in firms.keys():
            dist = math.dist(pos, firms[firm_id].position)
            if dist <= min_dist:
                min_dist = dist
                closest_firm = firm_id
        return closest_firm
    
    def list_firm_locations(self) -> list:
        """
        Return list of all positions firms take
        """
        firm_positions = []
        for firm_id in self.firm_dict.keys():
            firm_positions.append(self.firm_dict[firm_id].position)
        return firm_positions
    """
    def firm_rev(self, market_share:dict, firm_id:int) -> int:
        rev = 0
        for position in market_share[firm_id]:
            rev += self.model_grid.system_grid[position[0], position[1]]

        if firm_id == 1 and self.iteration == 1:
            print("1's m share")
            print(len(market_share[1]))
            print("1's rev")
            print(rev)
        return rev
    """
    def display_firms(self, firms:dict) -> None:
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