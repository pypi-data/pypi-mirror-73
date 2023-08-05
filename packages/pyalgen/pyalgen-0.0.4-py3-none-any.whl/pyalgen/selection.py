import random
import numpy as np


class Selection:
    def __init__(self) -> None:
        pass

    @staticmethod
    def tournament(population, fitness, tournament_size=2):
        new_pop = []
        number_of_tournaments = len(population)
        for _ in range(number_of_tournaments):
            x = random.randint(0, len(population) - 1)
            y = random.randint(0, len(population) - 1)
            if fitness[x] >= fitness[y]:
                new_pop.append(population[x])
            else:
                new_pop.append(population[y])
        return np.array(new_pop)
