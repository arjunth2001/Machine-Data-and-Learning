import numpy as np
import client as ta
import json
SECRET = 'z60uCu1jsJeEi4n96iH7qwpMMnvIO1BEdnbC38CokXIn9y9lSR'
MUTATION_SIZE = 5
MUTATION_RANGE = 1
POPULATION_SIZE = 15
SELECT_TOP_PARENTS = 2
MATE_POOL_SIZE = 5
MAX_GEN = 8
FACTOR = 1.5
initial_chromosome = []
minVal = None
minguy = None
requests = 0


def mutate_children(children, low=-MUTATION_RANGE, high=MUTATION_RANGE):
    for i in range(len(children)):
        noise = 1+np.random.uniform(low=low,
                                    high=high, size=children[i].shape)
        noise = np.where(noise == 0, np.random.uniform(0.000001, 1)+1, noise)
        indices = np.random.choice(np.arange(
            children[i].size), replace=False, size=len(children[i])-MUTATION_SIZE)
        noise[indices] = 1
        children[i] *= noise
    return np.clip(children, -10, 10)


def get_fitness(chromosomes):
    global minVal
    global minguy
    global requests
    fitness = []
    for chromosome in chromosomes:
        #ta_answer = ta.get_errors(SECRET, list(chromosome))
        requests += 1
        ta_answer = [np.random.uniform(
            10000, 1000000), np.random.uniform(10000, 100000)]
        if minVal == None:
            minVal = ta_answer
            minguy = chromosome
        else:
            if minVal[0]+minVal[1] > ta_answer[1]+ta_answer[0]:
                minVal = ta_answer
                minguy = chromosome
        fitness.append(ta_answer[0] + FACTOR * ta_answer[1])
        print(
            f'kid: {chromosome} train error: {ta_answer[0]}, validation error: {ta_answer[1]}')
    return np.array(fitness)


def isIn(given_array, actual_list):
    for element in actual_list:
        if np.array_equal(element, given_array):
            return True
    return False


def cross(parent1, parent2):
    d = np.abs(parent1-parent2)
    a = np.random.uniform()
    b = np.random.uniform()
    child1 = np.where(parent1 <= parent2, np.random.uniform(
        parent1-a*d, parent2+b*d), np.random.uniform(parent2-b*d, parent2+a*d))
    child2 = np.where(parent1 <= parent2, np.random.uniform(
        parent1-a*d, parent2+b*d), np.random.uniform(parent2-b*d, parent2+a*d))
    return child1, child2


def get_optimal_combinations(selected_population, selected_fitness):
    optimal_combinations = []
    n = np.shape(selected_population)[0]
    for i in range(n):
        for j in range(n):
            if i < j:
                optimal_combinations.append(
                    [selected_fitness[i] + selected_fitness[j], i, j])
    optimal_combinations = np.array(optimal_combinations)
    optimal_combinations = optimal_combinations[optimal_combinations[:, 0].argsort(
    )]
    return optimal_combinations


def optimal_breed(selected_population, selected_fitness):
    children = []
    mating_combinations = get_optimal_combinations(
        selected_population, selected_fitness)
    num = -1
    while len(children) < (POPULATION_SIZE - MATE_POOL_SIZE):
        num += 1
        par_num1 = int(mating_combinations[num % (
            np.shape(mating_combinations)[0])][1])
        par_num2 = int(mating_combinations[num % (
            np.shape(mating_combinations)[0])][2])
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

# Assumes that fittest parent has high positive fitness value


def roulette_selective_breed(selected_population, selected_fitness):
    normal_value = np.linalg.norm(selected_fitness)
    normalized_fitness = selected_fitness / normal_value
    sum_value = np.sum(normalized_fitness)
    probability_vector = normalized_fitness / sum_value
    children = []
    while len(children) < (POPULATION_SIZE - MATE_POOL_SIZE):
        par_num1 = np.random.choice(np.shape(selected_population)[
            0], p=probability_vector)
        par_num2 = np.random.choice(np.shape(selected_population)[
            0], p=probability_vector)
        if selected_fitness[par_num1] < selected_fitness[par_num2]:
            par_num1, par_num2 = par_num2, par_num1
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
    temp = np.array(temp)
    temp = mutate_children(temp)
    for i in range(np.shape(temp)[0]):
        factor = np.random.uniform(-0.0005, 0.0005)
        temp[i][0] += factor
    temp[0] = chromosome
    return temp


# TODO: Should this be read from file? That is, will the file overfit.txt be in evaluations or should it be hard-coded? ASK A TA...
with open("overfit.txt", "r") as f:
    initial_chromosome = json.load(f)

parents = get_init(initial_chromosome)
parent_fitness = get_fitness(parents)
children = parents[: POPULATION_SIZE-MATE_POOL_SIZE]
children_fitness = parent_fitness[: POPULATION_SIZE-MATE_POOL_SIZE]
parents = parents[POPULATION_SIZE-MATE_POOL_SIZE:]
parent_fitness = parent_fitness[POPULATION_SIZE-MATE_POOL_SIZE:]

for gen in range(MAX_GEN+1):
    if gen == 8:
        FACTOR = 1
        MUTATION_SIZE = 3
        SELECT_TOP_PARENTS = 3
    # if gen % 3 == 0 and gen != 0:
        MATE_POOL_SIZE += 2
    if gen == 17:
        MATE_POOL_SIZE = 15
    parent_index = np.argsort(-1*parent_fitness)
    parents = parents[parent_index]
    parent_fitness = parent_fitness[parent_index]
    selected_parents = parents[: SELECT_TOP_PARENTS]
    selected_parent_fitness = parent_fitness[: SELECT_TOP_PARENTS]
    rest = np.concatenate((parents[SELECT_TOP_PARENTS:], children[:]), axis=0)
    rest_fitness = np.concatenate(
        (parent_fitness[SELECT_TOP_PARENTS:], children_fitness[:]), axis=0)
    rest_index = np.argsort(rest_fitness*-1)
    rest = rest[rest_index]
    rest_fitness = rest_fitness[rest_index]
    pool = np.concatenate(
        (selected_parents, rest[: MATE_POOL_SIZE-SELECT_TOP_PARENTS]))
    pool_fitness = np.concatenate(
        (selected_parent_fitness, rest_fitness[: MATE_POOL_SIZE-SELECT_TOP_PARENTS]))
    print(
        f'gen: {gen} best:{np.max(pool_fitness)}')
    next_children = roulette_selective_breed(pool, pool_fitness)
    next_children_fitness = get_fitness(next_children)
    children_sort = np.argsort(-1*next_children_fitness)
    next_children = next_children[children_sort]
    next_children_fitness = next_children_fitness[children_sort]
    parents = np.concatenate((parents, children))
    parent_fitness = np.concatenate((parent_fitness, children_fitness))
    parent_index = np.argsort(-1*parent_fitness)
    parents = parents[parent_index]
    parent_fitness = parent_fitness[parent_index]
    parent_fitness = parent_fitness[: MATE_POOL_SIZE]
    parents = parents[: MATE_POOL_SIZE]
    parent_fitness = parent_fitness[: MATE_POOL_SIZE]
    children = next_children
    children_fitness = next_children_fitness
print("Parents:")
print(parents)
print("Children:")
print(children)
print("Parent Fitness:")
print(parent_fitness)
print("Children Fitness")
print(children_fitness)
print("BEST !:", minVal, minguy)
print(requests)
