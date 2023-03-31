

class Firm:

    def __init__(self, starting_pos:list, group:int, base_price:int) -> None:
        
        self.position = starting_pos
        self.position_history = [starting_pos]
        self.group = group
        self.price = base_price
        self.price_history = [base_price]
        self.revenue = 0
        self.revenue_history = [0]
    
    def log_firm(self) -> str:
        pos_str = " [{x}, {y}] ".format(x=self.position[0], y=self.position[1])
        return "Firm With Group ID : {group}, Currently Has Revenue : {rev} & Is Located At Position : {pos}""".format(
            group=self.group,
            rev=self.revenue,
            pos=pos_str
        )
