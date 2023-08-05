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

    @staticmethod
    def roulette(population, fitness):
        probs = fitness / np.sum(fitness)
        cumsum = np.cumsum(probs)
        new_index = []
        for _ in range(len(population)):
            # for idx, val in enumerate(fitness):
            #     r = random.random()
            #     if r < val:
            #         new_index.append(idx)
            cs_list = list(cumsum)
            r = random.random()
            cs_list.append(r)
            cs_list.sort()
            new_index.append(cs_list.index(r))


        return population[new_index]
