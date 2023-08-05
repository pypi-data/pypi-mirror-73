import numpy as np
from tqdm import tqdm


class GeneticAlgorithm:
    def __init__(
        self, population, objective_fn, selection, crossover, mutation
    ) -> None:
        """Class combines various objects like population, selection, crossover and mutation 
        to create a GA object and perform operation
        """
        self.population = population
        self.objective_fn = objective_fn
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation

    def forward(self, iterations):
        objective, pop = None, None
        pop = self.population
        i = None
        for i in tqdm(range(iterations), ncols=100):
            objective = self.objective_fn(*pop.T)
            if (objective == 0).sum() >= 1:
                break
            fitness = 1 / objective
            pop = self.selection(pop, fitness)
            pop = self.crossover(pop, fitness)
            pop = self.mutation(
                pop,
                low=np.min(self.population),
                high=np.max(self.population),
                dtype=self.population[-1][-1].dtype,
            )
        return i, objective, pop
