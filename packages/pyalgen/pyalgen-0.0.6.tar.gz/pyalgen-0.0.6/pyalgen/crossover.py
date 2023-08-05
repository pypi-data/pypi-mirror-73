import random
import numpy as np


class Crossover:
    def __init__(self) -> None:
        pass

    @staticmethod
    def onepoint(population, fitness, cr=0.25):
        indices = []
        random_numbers = np.random.uniform(0, 1, (len(population)))
        for idx, val in enumerate(random_numbers):
            if val < cr:
                indices.append(idx)
        for idx, val in enumerate(indices):
            cur_index = indices[idx]
            nxt_index = indices[idx + 1] if idx < len(indices) - 1 else indices[0]
            index = random.randint(0, len(population) - 1)
            population[cur_index, index:], population[nxt_index, index:] = (
                population[nxt_index, index:],
                population[cur_index, index:],
            )
        return population

    @staticmethod
    def clone(population, fitness):
        return population
