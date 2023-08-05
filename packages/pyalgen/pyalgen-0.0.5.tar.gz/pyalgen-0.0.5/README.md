## pyalgen - A minimal library for genetic algorithm in python

### Install
```bash
pip3 install pyalgen
```

### How to use
1. Import the package

```python
import pyalgen # import pyalgen
from pyalgen import TestFunctions as tf # test functions to optimize
```
2. Define population
```python
pop = pyalgen.Population(low=-10, high=10, dtype='float', dist='uniform')
# the variable in the population is of type float and the 
# values are taken from a uniform distribution in (low, high)
population = pop(pop_size=1000, variables=2)
# variables is the number of variables to optimize. We are optimizing the 
# matyas function which has two variables
# search space ranges from -10 to 10
# pop_size is the population size of each generation
```
<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Matyas_function.pdf/page1-1200px-Matyas_function.pdf.jpg" height=300></img>
<br>
Matyas function
</p>

3. Select type of selection, crossover and mutation strategies
```python
selection = pyalgen.Selection.tournament
crossover = pyalgen.Crossover.onepoint
mutation = pyalgen.Mutation.randompoint
```

4. Instantiate Genetic Algorithm object with defined variables
```python
ga = pyalgen.GeneticAlgorithm(population, tf.matyas, selection, crossover, mutation)
```

5. Run the algorithm
```python
iterations, objective, pop = ga.forward(iterations=200)
# iterations is the number of generations to run for
print(f'min_value: {objective.min()}, solution: {pop[objective.argmin()]}, generation: {iterations}')
# print the minimum objective and the chromosome in population which 
# given minimum objective 
```

6. Check the result
```bash
100%|██████████████████████████████████████████████████████████| 1000/1000 [00:03<00:00, 262.55it/s]
min_value: 7.719286052427051e-07, solution: [-0.00447918 -0.00410235], generation: 1000
# global minimum of matyas is at f(0, 0) = 0
# our algorithm gives minimum, f(-0.004, -0.004) = 7.7e-07
# which is pretty close 
```

### Results can be improved by tweaking the parameters

### Testing the algorithm on custom function

Let's solve the equation,
<p align="center">
<img src="https://latex.codecogs.com/svg.latex?a%20+%202*b%20+%203*c%20+%204*d%20=%2030"></img>
</p>

##### Complete code
```python
import pyalgen

pop = pyalgen.Population(1, 30, unique=True, dtype='int')
population = pop(1000, 4) # here we generate intergers in range[1, 30)
# for population

selection = pyalgen.Selection.tournament
crossover = pyalgen.Crossover.onepoint
mutation = pyalgen.Mutation.randompoint

def obj(a, b, c, d): # objective function
    return a + 2*b + 3*c + 4*d - 30 

ga = pyalgen.GeneticAlgorithm(population, obj, selection, crossover, mutation)


iterations, objective, pop = ga.forward(iterations=1000)

if iterations == 1000:
    print(f'min_value: {objective.min()}, \
        solution: {pop[objective.argmin()]}, generation: {iterations}')   
else:
    print(f'min_value: {objective[objective == 0][0]},\
         solution: {pop[objective == 0][0]}, generation: {iterations}')   
```
GeneticAlgorithm breaks the computation, if any of the chromosome reached out objective, i.e, `0`
### Result
```bash
  1%|▋                                                           | 11/1000 [00:00<00:05, 171.30it/s]
min_value: 0, solution: [11  4  1  2], generation: 11
```
The algorithm reached a solution during generation: `11`
Solution: a = `11`, b = `4`, c = `1`, d = `2`