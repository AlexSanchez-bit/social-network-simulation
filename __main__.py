import random
from src.simulation import run_simulations

run_simulations(
    number_agents=20, 
    number_posts=300, 
    simulations_count=1,
    selectes_characteristics=[5, 8, 7, 4, 1],
)