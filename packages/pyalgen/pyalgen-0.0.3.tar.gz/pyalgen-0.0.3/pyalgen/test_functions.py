import math
import numpy as np

class TestFunctions:
    def __init__(self) -> None:
        pass

    @staticmethod
    def booth(x, y):
        return (x + 2*y - 7)**2 + (2*x + y -5)**2

    @staticmethod
    def beale(x, y):
        return (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2

    @staticmethod
    def matyas(x, y):
        return 0.26*(x**2 + y**2) - 0.48*x*y