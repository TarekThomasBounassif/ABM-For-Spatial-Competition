
import env_generator
import model
import firm
import config
import env_plotter

class Simulator:
    """
    Build all elements of an experiment and carry out the simulations.
    This class holds all logic relating to the per iteration logic of the simulation.
    """
    def __init__(self, simulation_params:dict) -> None:

        self.model_env = model.Model(config.grid_params, config.firm_params)
        self.max_iters = simulation_params['MaxIters']

    def simulate(self) -> None:
        """
        Carry out the simulation
        """

        moves = 0
        while self.model_env.iteration < self.max_iters:

            # Check for termination
            if self.model_env.iteration % (config.simulation_params['MaxIters']/10) == 0:
                self.log_sim()

            # Iterate over firms
            for firm_id in self.model_env.firm_dict.keys():

                # Consider potential new positions
                current_firm = self.model_env.firm_dict[firm_id]
                firm_positions = self.model_env.list_firm_locations()   
                potential_positions = current_firm.get_potential_positions_1_dimension(firm_positions)

                # Pick position with best revenue
                best_position = current_firm.position
                current_rev = 0

                for pos in potential_positions:
                    new_rev, old_rev = self.model_env.consider_pos_new(firm_id, pos)
                    
                    """
                    print("-"*100)
                    print("Current Iteration : {iter}".format(iter=self.model_env.iteration))
                    print("Current Firm : {id}".format(id=firm_id))
                    print("Old Rev : {old_rev}".format(old_rev=current_rev))
                    print("New Rev : {new_rev}".format(new_rev=new_rev))
                    print("Old Pos = " + str(best_position))
                    print("New Pos = " + str(pos))
                    print("-"*100)
                    """

                    if new_rev > old_rev:
                        moves += 1
                        current_rev = new_rev
                        best_position = pos

                # Update system
                self.model_env.firm_dict[firm_id].position = best_position
                self.model_env.firm_dict[firm_id].position_history.append(best_position)
                self.model_env.firm_dict[firm_id].revenue = current_rev
                self.model_env.firm_dict[firm_id].revenue_history.append(current_rev)

            
        
            self.model_env.iteration += 1
        print(moves)

    def log_sim(self) -> None:
        env_plotter.plot_1d_system(self.model_env, True)
        # self.model_env.log_system()