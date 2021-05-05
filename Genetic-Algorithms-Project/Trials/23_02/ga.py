import numpy as np
import client as ta
import json
SECRET = 'z60uCu1jsJeEi4n96iH7qwpMMnvIO1BEdnbC38CokXIn9y9lSR'
# TODO: We need to fig out these values... hmm
MUTATION_PERC = 0.3
MUTATION_RANGE = 1
POPULATION_SIZE = 7
MATE_POOL_SIZE = 3
MAX_GEN = 10
initial_chromosome = []
ctr = 0


def mutate_children(children, low=-MUTATION_RANGE, high=MUTATION_RANGE):
    for i in range(len(children)):
        noise = np.random.uniform(low=low, high=high, size=children[i].shape)
        indices = np.random.choice(np.arange(
            children[i].size), replace=False, size=int(children[i].size*(1-MUTATION_PERC)))
        noise[indices] = 0
        children[i] += noise
    return np.clip(children, -10, 10)


def get_fitness(chromosomes):
    fitness = []
    for chromosome in chromosomes:
        #ta_answer = ta.get_errors(SECRET, list(chromosome))
        fitness.append(ta_answer[0]+ta_answer[1])
        print(
            f'train error: {ta_answer[0]}, validation error: {ta_answer[1]}')
    return np.array(fitness)


def isIn(given_array, actual_list):
    for element in actual_list:
        if np.array_equal(element, given_array):
            return True
    return False


def cross(parent1, parent2):
    point = np.random.randint(4, 7)
    child1 = np.concatenate((parent1[:point], parent2[point:]), axis=0)
    child2 = np.concatenate((parent2[:point], parent1[point:]), axis=0)
    return child1, child2


def breed(selected_population):
    children = []
    child1, child2 = cross(selected_population[0], selected_population[1])
    children.append(child1)
    children.append(child2)
    mating_combinations = []
    while len(children) < (POPULATION_SIZE - MATE_POOL_SIZE):
        par_num1 = np.random.randint(0, np.shape(selected_population)[0])
        par_num2 = (par_num1 + 1) % np.shape(selected_population)[0]
        mating_combinations.append([par_num1, par_num2])
        child1, child2 = cross(
            selected_population[par_num1], selected_population[par_num2])
        if not isIn(child1, children):
            children.append(child1)
        if len(children) == POPULATION_SIZE-MATE_POOL_SIZE:
            break
        if not isIn(child2, children):
            children.append(child2)
        if len(children) == POPULATION_SIZE-MATE_POOL_SIZE:
            break
    return mutate_children(np.array(children))


def get_init(chromosome):
    '''Gets the initial Chromosomes'''
    temp = [list(chromosome) for i in range(POPULATION_SIZE)]
    temp = np.array(temp, dtype=np.double)
    temp = mutate_children(temp, -1, 1)
    temp[0] = chromosome
    return temp


# TODO: Should this be read from file? That is, will the file overfit.txt be in evaluations or should it be hard-coded? ASK A TA...
with open("overfit.txt", "r") as f:
    initial_chromosome = json.load(f)

population = get_init(initial_chromosome)
fitness = get_fitness(population)

for gen in range(MAX_GEN+1):
    sorted_fitness_index = np.argsort(fitness)
    population = population[sorted_fitness_index]
    fitness = fitness[sorted_fitness_index]
    print(
        f'gen: {gen} best:{fitness[0]}')
    population = population[:POPULATION_SIZE]
    fitness = fitness[:POPULATION_SIZE]
    selected_population = population[: MATE_POOL_SIZE]
    selected_fitness = fitness[: MATE_POOL_SIZE]
    children = breed(selected_population)
    children_fitness = get_fitness(children)
    population = np.concatenate((population, children), axis=0)
    fitness = np.concatenate((fitness, children_fitness), axis=0)

final_fitness = np.min(fitness)
print("Answer", final_fitness)
