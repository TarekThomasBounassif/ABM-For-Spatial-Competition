
import env_generator
import config

class Firm:

    def __init__(self, starting_pos:list, group:int, base_price:int) -> None:
        
        self.group = group
        
        self.position = starting_pos
        self.position_history = [starting_pos]

        self.price = base_price
        self.price_history = [base_price]

        self.revenue = 0
        self.revenue_history = [0]
    
    def evaluate_market_share(self, market_share:dict, grid_in:env_generator.EnvGrid) -> int:
        """
        Return revenue of firm for an input market share
        """
        rev = 0
        for position in market_share[self.group]:
            rev += grid_in.system_grid[position[0], position[1]]
        return rev # * self.price
        
    def update_rev(self, market_share:dict, grid_in:env_generator.EnvGrid) -> None:
        rev = self.evaluate_market_share(market_share, grid_in)
        self.revenue = rev
        self.revenue_history.append(rev)

    def get_potential_positions_1_dimension(self, firm_positions:list) -> list:
        """
        Explore the potential new positions the firm can take (1d case)
        """
        pos_x = self.position[1]
        potential_positions = []
        if pos_x > 1 and pos_x < config.grid_params['Size'] - 1:
            new_pos_left = [0, pos_x - 2]
            new_pos_right = [0, pos_x + 2]
            if new_pos_left not in firm_positions:
                potential_positions.append(new_pos_left)
            if new_pos_right not in firm_positions:
                potential_positions.append(new_pos_right)
        return potential_positions

    def log_firm(self) -> str:
        pos_str = " [{x}, {y}] ".format(x=self.position[0], y=self.position[1])
        return "Firm : {group} Has Revenue : {rev} & Is Located At Position :{pos}""".format(
            group=self.group,
            rev=self.revenue,
            pos=pos_str
        )
