import random
import numpy as np


class Population:
    """
    Class to generate population to the Genetic Algorithm

    Parameters:
        low: lowest value to generate population value
        high: highest value to generate population value
        seed: set random seed value
        dtype: type of generated population, [`int`, `float`]
        dist: if `float`, distribution to be selected from [`normal`, `uniform`]
        unique: if selected `int`, unique makes sure each chromosome created has unique values in it
    Returns: None
    """

    def __init__(self, low, high, dtype="int", dist=None, unique=False) -> None:
        super().__init__()
        self.unique = unique
        self.dtype = dtype
        self.dist = dist
        self.high = high
        self.low = low

    def forward(self, pop_size, variables):
        """
        Function creates a population 

        Parameters: 
            pop_size: size of population
            variables: variables to optimize in problem 
        Returns: population in numpy.ndarray
        """
        params = (self.low, self.high, (pop_size, variables))
        assert self.dtype in ["int", "float"]
        if self.dist is not None:
            assert self.dist in ["normal", "uniform"]
        if self.dtype == "int":
            if self.unique:
                sample = set(range(self.low, self.high + 1))
                unique_nums = [
                    random.sample(sample, variables) for _ in range(pop_size)
                ]
                return np.array(unique_nums)
            else:
                return np.random.randint(*params)
        else:
            if self.dist == "uniform":
                return np.random.uniform(*params)
            else:
                return np.random.normal(*params)

    def __call__(self, pop_size, variables):
        """
        call the forward function automatically
        """
        return self.forward(pop_size, variables)
