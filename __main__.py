import random
from src.simulation import run_simulations


run_simulations(
    number_agents=20, 
    number_posts=30, 
    simulations_count=10,
    selectes_characteristics=[5, 8, 7, 4, 1],
)