import numpy as np


class Mutation:
    def __init__(self) -> None:
        pass

    def randompoint(pop, low, high, dtype="int", mr=0.2):
        total_mutations = int(mr * len(pop))
        if dtype == "float":
            dtype = "float"
        elif dtype == "int64":
            dtype = "int"
        values = {
            "int": np.random.randint(low, high, (total_mutations)),
            "float": np.random.uniform(low, high, (total_mutations)),
        }
        mutation_points = np.random.randint(0, len(pop), size=(total_mutations))
        mutation_values = values[dtype]
        _pop = pop.reshape(-1, pop.shape[0] * pop.shape[1])
        for index, point in enumerate(mutation_points):
            _pop[0][point] = mutation_values[index]
        pop = _pop.reshape(pop.shape[0], pop.shape[1])
        return pop
