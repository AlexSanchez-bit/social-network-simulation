import numpy as np
from src.metaheuristics import PSO


def build_func_obj(C: np.ndarray, rel: np.array, pp: np.array):
    def func_obj(v):
        if any(map(lambda x: x < 0 or x > 1, v)):
            return -float('inf')
        
        s_rest = [v[i] for i in pp] # relevancia de los temas(dados por el usuario) en el vector solución
        for i, topic in enumerate(v):
            if i not in pp:
                if np.any(topic > s_rest):
                    return -float('inf')
        
        I = np.dot(v,C[:,0])*rel[0] + np.dot(v, C[:,1])*rel[1] + np.dot(v, C[:,2])*rel[2]
        return I 

    return func_obj


def run_meta(C: np.ndarray, rel: np.array, pp: np.array):
    func_obj = build_func_obj(C, rel, pp)
    
    pso = PSO()
    # TODO: take sol_dim from txt with topics
    w, vsol = pso.solve(func_obj, sol_dim=328, pop_size=5)
    
    # solutions = []
    # for _ in range(3):
    #     pso = PSO()
    #     # TODO: take sol_dim from txt with topics
    #     sol, vsol = pso.solve(func_obj, sol_dim=328, pop_size=5)
        
    #     if vsol != -float('inf'):
    #         solutions.append(sol)

    # w = []
    # for i in range(2):
    #     v = 0
    #     for s in solutions:
    #         v += s[i]
        
    #     v /= len(solutions)
    #     w.append(v)
    
    
    sol = [[i, v] for i, v in enumerate(w)]
    sol = sorted(sol, key=lambda x: x[1], reverse=True)
    
    return sol[:5]    