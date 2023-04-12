import model
import env_plotter
import random

class Simulator:
    """
    Build all elements of an experiment and carry out the simulations.
    This class holds all logic relating to the per iteration logic of the simulation.
    """
    def __init__(self, simulation_params:dict, grid_params:dict, firm_params:dict) -> None:

        self.model_env = model.Model(simulation_params, grid_params, firm_params)
        self.max_iters = simulation_params['MaxIters']
        self.two_dimensions = True if grid_params['Dim'] == 2 else False
        self.with_price = simulation_params['WithPrice']
        self.simulation_params = simulation_params
        self.grid_params = grid_params
        self.firm_params = firm_params
        self.market_share_list_history = list()

    def simulate(self) -> None:

        """
        Carry out the simulation
        """

        while self.model_env.iteration < self.max_iters:

            # Log The Simulation
            if self.model_env.iteration % (self.simulation_params['MaxIters']/4) == 0:
                #self.log_sim()
                #print(self.model_env.iteration)
                pass

            # Randomise the order firms take to move
            firm_list_random = list(self.model_env.firm_dict.keys())
            random.shuffle(firm_list_random)
            current_mshare_list = list()

            for firm_id in firm_list_random:

                current_firm = self.model_env.firm_dict[firm_id]

                # Collect the current list of all firm positions
                firm_positions = self.model_env.list_firm_locations()

                # Collect all new potential positions
                if not self.two_dimensions:
                    potential_positions = current_firm.get_potential_positions_1_dimension(firm_positions)
                else:
                    potential_positions = current_firm.get_potential_positions_2_dimension(firm_positions)
                potential_positions = [pos for pos in potential_positions if pos[0] >= 0 and pos[1] < self.grid_params['Size']]
                potential_positions.append(current_firm.position)

                # Track Revenue & Market Share
                current_rev = current_firm.revenue
                current_mshare = current_firm.market_share
                best_position = current_firm.position
                current_price = current_firm.price
                

                # Evaluate each potential position
                for index1, pos in enumerate(potential_positions):
                    
                    # If pirce changes are allowed
                    if self.with_price:

                        # Go through each potential change to price
                        for index2, price_change in enumerate(self.firm_params['PriceChanges']):

                            if current_price + price_change > 0:
                                exploration_results = self.model_env.consider_position(firm_id, pos, price_change)
                                new_rev = exploration_results[0]
                                new_mshare_size = exploration_results[1]
                                new_mshare_list = exploration_results[2]

                                # If its the first move and first iteration, update the firms initial revenue and market share.
                                if pos == current_firm.position and self.model_env.iteration == 0:
                                        self.model_env.firm_dict[firm_id].revenue = new_rev
                                        self.model_env.firm_dict[firm_id].revenue_history.append(new_rev)
                                        self.model_env.firm_dict[firm_id].market_share = new_mshare_size
                                        self.model_env.firm_dict[firm_id].market_share_history.append(new_mshare_size)
                                        self.model_env.firm_dict[firm_id].price = current_price
                                        self.model_env.firm_dict[firm_id].price_history.append(current_price)
                                        current_rev = new_rev
                                        current_mshare = new_mshare_size
                                else:
                                    if new_rev > current_rev:
                                        current_rev = new_rev
                                        best_position = pos
                                        current_mshare = new_mshare_size
                                        current_price = current_price + price_change
                                        current_mshare_list = new_mshare_list
                                    
                    # If price changes are not enabled
                    else:
                        exploration_results = self.model_env.consider_position(firm_id, pos)
                        new_rev = exploration_results[0]
                        new_mshare_size = exploration_results[1]
                        new_mshare_list = exploration_results[2]

                        # If its the first move and first iteration, update the firms initial revenue and market share.
                        if pos == current_firm.position and self.model_env.iteration == 0:
                                self.model_env.firm_dict[firm_id].revenue = new_rev
                                self.model_env.firm_dict[firm_id].revenue_history.append(new_mshare_size)
                                self.model_env.firm_dict[firm_id].market_share = new_mshare_size
                                self.model_env.firm_dict[firm_id].market_share_history.append(new_mshare_size)
                                current_rev = new_rev
                                current_mshare = new_mshare_size
                                current_mshare_list = new_mshare_list
                        else:
                            if new_rev > current_rev:
                                current_rev = new_rev
                                best_position = pos
                                current_mshare = new_mshare_size
                                current_mshare_list = new_mshare_list

                # Update Firm Objects & Histories, even if changes are not made, track history
                self.model_env.firm_dict[firm_id].position = best_position
                self.model_env.firm_dict[firm_id].position_history.append(best_position)
                self.model_env.firm_dict[firm_id].revenue = current_rev
                self.model_env.firm_dict[firm_id].revenue_history.append(current_rev)
                self.model_env.firm_dict[firm_id].price = current_price
                self.model_env.firm_dict[firm_id].price_history.append(current_price)
                self.model_env.firm_dict[firm_id].market_share = current_mshare
                self.model_env.firm_dict[firm_id].market_share_history.append(current_mshare)

            current_mshare_list = self.model_env.assign_consumers(
                self.model_env.model_grid,
                self.model_env.firm_dict[0].position,
                None)
            
            self.market_share_list_history.append(current_mshare_list)

            self.model_env.iteration += 1

        self.log_sim()

    # Plot the current simulation state
    def log_sim(self) -> None:
        if not self.two_dimensions:
            env_plotter.plot_1d_system(self.model_env, True)
        else:
            env_plotter.plot_2d_system(self.model_env)

    