import simulator
import config
import env_plotter
import importlib
import config
import firm
sim_test = simulator.Simulator(config.simulation_params, config.grid_params, config.firm_params)
sim_test.simulate()
