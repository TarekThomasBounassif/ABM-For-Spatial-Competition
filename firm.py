
import env_generator
import config
import math

class Firm:

    def __init__(self, starting_pos:list, firm_id:int, base_price:int) -> None:
        
        self.firm_id = firm_id
        
        # Track current position and history
        self.position = starting_pos
        self.position_history = [starting_pos]

        # track firm price and history
        self.price = base_price
        self.price_history = [base_price]

        # Track history of a firms market share
        self.market_share_history = []
        
        # Track firm revenue and history
        self.revenue = 0
        self.revenue_history = [0]
    
    def evaluate_market_share(self, market_share:dict, grid_in:env_generator.EnvGrid) -> int:

        """
        Return revenue of firm for an input market share
        """

        rev = 0
        for position in market_share[self.firm_id]:
            rev += grid_in.system_grid[position[0], position[1]]
        return rev # * self.price
        
    def initialise_rev(self, market_share:dict, grid_in:env_generator.EnvGrid) -> None:

        """
        Set initial firm revenue
        """

        rev = self.evaluate_market_share(market_share, grid_in)
        self.revenue = rev
        self.revenue_history.append(rev)

    def get_potential_positions_1_dimension(self, firm_positions:list) -> list:

        """
        Explore the potential new positions the firm can take (1d)
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

    def get_potential_positions_2_dimension(self, firm_positions:list) -> list:

        """
        Explore the potential new positions the firm can take (2d)
        """

        pos_x = self.position[0]
        pos_y = self.position[1]
        
        size = config.grid_params['Size']

        adjacent_positions = []
        if pos_x < size - 2:
            adjacent_positions.append([pos_x + 2, pos_y])
        if pos_x > 2:
            adjacent_positions.append([pos_x - 2, pos_y])
        if pos_y < size - 2:
            adjacent_positions.append([pos_x, pos_y + 2])
        if pos_y > 2:
            adjacent_positions.append([pos_x, pos_y - 2])
        if pos_x < size - 2 and pos_y < size - 2:
            adjacent_positions.append([pos_x + 2, pos_y + 2])
        if pos_x > 2 and pos_y >  2:
            adjacent_positions.append([pos_x - 2, pos_y - 2])
        if pos_x < size - 2 and pos_y > 2:
            adjacent_positions.append([pos_x + 2, pos_y - 2])
        if pos_x > 2 and pos_y > size - 2:
            adjacent_positions.append([pos_x - 2, pos_y + 2])
        return [pos for pos in adjacent_positions if pos not in firm_positions]

    def log_firm(self) -> str:

        """
        Print basic logs for a firm
        """

        pos_str = " [{x}, {y}] ".format(x=self.position[0], y=self.position[1])
        return "Firm : {group} Has Revenue : {rev} & Is Located At Position :{pos}""".format(
            group=self.firm_id,
            rev=self.revenue,
            pos=pos_str
        )

