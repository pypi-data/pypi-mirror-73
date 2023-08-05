import random
import numpy as np

class Mutation:
    def __init__(self) -> None:
        pass

    def randompoint(pop, mr=0.2):
        total_mutations = mr*len(pop)
        mutation_points = np.random.randint(0, len(pop), size=(total_mutations))
        mutation_values = np.random.randint()
        _pop = pop.reshape(-1, pop.shape[0]*pop.shape[1])
        for index, point in enumerate(mutation_points):
            _pop[0][point] = mutation_values[index]
        pop = _pop.reshape(pop.shape[0], pop.shape[1])
        return pop
