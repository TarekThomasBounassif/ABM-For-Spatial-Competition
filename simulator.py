
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
        while not self.stop_sim():
            if self.model_env.iteration % 10 == 0:
                self.log_sim()
            break
    
    def stop_sim(self) -> bool:
        """
        Check for termination of simulation
        """
        if self.model_env.iteration <= self.max_iters:
            return False
        else:
            return True

    def log_sim(self) -> None:
        env_plotter.plot_1d_system(self.model_env, True)
        self.model_env.log_system()