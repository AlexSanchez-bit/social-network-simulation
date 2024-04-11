from typing import Callable
import numpy as np
import random

# Particle Swarm Optimization
class PSO:
    def __init__(self) -> None:
        self.hpos = None
        super().__init__()
    
    class Particle:
        def __init__(self, pos, speed, inertia=0.5, cognitive_coeff=0.6, social_coeff=0.6):
            assert len(pos) == len(speed), "The particle position and speed must be the same length"
            self.pos = pos
            self.speed = speed
            self.best_pos = pos
            self.dim = len(pos)
            
            self.inertia = inertia
            self.cog_coeff = cognitive_coeff
            self.soc_coeff = social_coeff

        def upd_speed(self, global_best):
                rp = random.random()
                rg = random.random()
                self.speed = self.inertia*self.speed + self.cog_coeff*rp*(self.best_pos-self.pos) + self.soc_coeff*rg*(global_best - self.pos)
    
        def upd_pos(self):
            self.pos += self.speed            

        def upd_best_pos(self):
            self.best_pos = self.pos
            
        def __str__(self) -> str:
            return str(self.pos)
        
    
    def stop_condition(self, t) -> bool:
        return t > 1000
        
    def get_init_pop(self, sol_dim, pop_size):        
        init_pop = [
            PSO.Particle(
                # TODO: change (-5, 5) by the correct search zone
                pos=np.array([random.uniform(-5, 5) for _ in range(sol_dim)]),
                speed=np.zeros(sol_dim)
            )
            for i in range(pop_size)
        ]
        return init_pop
    
    def is_best_sol(self, x, y, obj_func: Callable):
        if obj_func(x) < obj_func(y):
            return True
        else:
            return False
    
    def solve(self, obj_func: Callable, sol_dim, pop_size=random.randint(6, 10), verbose=False):
        # generate the initial population
        sols = self.get_init_pop(sol_dim, pop_size)
        
        # search the best position
        global_best = None        
        for sol in sols:
            if global_best is None or self.is_best_sol(sol.pos, global_best, obj_func):
                global_best = sol.pos
        
        t = 0
        while(not self.stop_condition(t)):
            if verbose:
                print(f'\n======== Iteracion {t} =========')
                print(f'Best sol: {global_best}')
                print(f'Cand sol: {[x.pos for x in sols]}')
            
            for p in sols:
                p.upd_speed(global_best)
                p.upd_pos()
                if self.is_best_sol(p.best_pos, p.pos, obj_func):
                    p.upd_best_pos()
                if self.is_best_sol(p.best_pos, global_best, obj_func):
                    global_best = p.best_pos
            t += 1
                    
        return global_best