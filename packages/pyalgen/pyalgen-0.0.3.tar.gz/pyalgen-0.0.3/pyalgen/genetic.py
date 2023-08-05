from tqdm import tqdm


class GeneticAlgorithm:
    def __init__(self, population, objective_fn, selection, crossover) -> None:
        self.population = population
        self.objective_fn = objective_fn
        self.selection = selection
        self.crossover = crossover

    def forward(self, iterations):
        objective, pop = None, None
        pop = self.population

        for i in tqdm(range(iterations), ncols=100):
            objective = self.objective_fn(*pop.T)
            # print(objective)
            fitness = 1 / (1 + objective)
            pop = self.selection(pop, fitness)
            pop = self.crossover(pop, fitness)
            if (objective == 0).sum() >= 1:
                break
        return iterations, objective, pop
