import model
import config
import env_plotter
import random

class Simulator:
    """
    Build all elements of an experiment and carry out the simulations.
    This class holds all logic relating to the per iteration logic of the simulation.
    """
    def __init__(self, simulation_params:dict) -> None:

        self.model_env = model.Model(config.grid_params, config.firm_params)
        self.max_iters = simulation_params['MaxIters']
        self.two_dimensions = True if config.grid_params['Dim'] == 2 else False
        self.with_price = config.simulation_params['WithPrice']

    def simulate(self) -> None:
        
        """
        Carry out the simulation
        """

        while self.model_env.iteration < self.max_iters:

            # Log The Simulation
            if self.model_env.iteration % (config.simulation_params['MaxIters']/4) == 0:
                self.log_sim()
                print(self.model_env.iteration)

            # Randomise the order firms take to move
            firm_list_random = list(self.model_env.firm_dict.keys())
            random.shuffle(firm_list_random)

            for firm_id in firm_list_random:

                current_firm = self.model_env.firm_dict[firm_id]

                # Collect the current list of all firm positions
                firm_positions = self.model_env.list_firm_locations()

                # Collect all new potential positions
                if not self.two_dimensions:
                    potential_positions = current_firm.get_potential_positions_1_dimension(firm_positions)
                else:
                    potential_positions = current_firm.get_potential_positions_2_dimension(firm_positions)

                potential_positions = [
                    pos for pos in potential_positions if 
                    pos[0] >= 0 and 
                    pos[1] < config.grid_params['Size']
                ]

                # Track revenue, position, and price to determine best potential new position
                current_rev = current_firm.revenue
                current_rev = 0
                best_position = current_firm.position
                current_price = current_firm.price
                current_mshare = 0

                # Evaluate each potential position
                for pos in potential_positions:
                    
                    # If pirce changes are allowed
                    if self.with_price:

                        # Go through each potential change to price
                        for price_change in config.firm_params['PriceChanges']:

                            # Collect new and old revenue given changes to position and price
                            new_rev, new_mshare_size, old_rev, old_mshare_size = self.model_env.consider_pos_with_price(firm_id, pos, price_change)

                            if price_change < 0:
                                pass
                                print("-"*100)
                                print("Pos = " + str(pos))
                                print("Firm ID = " + str(firm_id))
                                print(new_rev, old_rev)
                                print("-"*100)

                            if self.model_env.iteration == 0:
                                self.model_env.firm_dict[firm_id].revenue = old_rev
                                self.model_env.firm_dict[firm_id].revenue_history.append(old_rev)
                                self.model_env.firm_dict[firm_id].market_share_history.append(old_mshare_size)

                            # If revenue increases, update out trackers
                            if new_rev > old_rev:
                                current_rev = new_rev
                                best_position = pos
                                current_price = current_firm.price + price_change
                                current_mshare = new_mshare_size

                    # If price changes are not enabled
                    else:

                        new_rev, old_rev = self.model_env.consider_pos_new(firm_id, pos)

                        if self.model_env.iteration == 0:
                                self.model_env.firm_dict[firm_id].revenue = old_rev
                                self.model_env.firm_dict[firm_id].revenue_history.append(old_rev)

                        if new_rev > old_rev:
                            current_rev = new_rev
                            best_position = pos

                # Update Firm Objects & Histories, even if changes are not made, track history
                self.model_env.firm_dict[firm_id].position = best_position
                self.model_env.firm_dict[firm_id].position_history.append(best_position)
                self.model_env.firm_dict[firm_id].revenue = current_rev
                self.model_env.firm_dict[firm_id].revenue_history.append(current_rev)
                self.model_env.firm_dict[firm_id].price = current_price
                self.model_env.firm_dict[firm_id].price_history.append(current_price)
                self.model_env.firm_dict[firm_id].market_share_history.append(current_mshare)

            self.model_env.iteration += 1

        self.log_sim()

    # Plot the current simulation state
    def log_sim(self) -> None:
        if not self.two_dimensions:
            env_plotter.plot_1d_system(self.model_env, True)
        else:
            env_plotter.plot_2d_system(self.model_env)

    