import numpy as np
import client as ta
import json
SECRET = 'z60uCu1jsJeEi4n96iH7qwpMMnvIO1BEdnbC38CokXIn9y9lSR'
MUTATION_SIZE = 5
MUTATION_RANGE = 1
POPULATION_SIZE = 30
SELECT_TOP_PARENTS = 4
SELECT_TOP_KIDS = 3
MATE_POOL_SIZE = 15
MAX_GEN = 12
FACTOR = 1
SUM_FACTOR = 1
initial_chromosome = []
minVal = None
minguy = None
requests = 0


def mutate_children(children):
    children = np.array(children)
    for i in range(len(children)):
        noise = np.random.uniform(1e-15*children[i], 1.2*children[i])
        indices = np.random.choice(np.arange(
            children[i].size), replace=False, size=MUTATION_SIZE)

        children[indices] = noise[indices]
    return np.clip(children, -10, 10)


def get_fitness(chromosomes):
    global minVal
    global minguy
    global requests
    fitness = []
    print()
    print("Errors:>>")
    print()
    print("XXXXX-----XXXXX")
    for chromosome in chromosomes:
        ta_answer = ta.get_errors(SECRET, list(chromosome))
        requests += 1
        # ta_answer = [np.random.uniform(
        #   10000, 1000000), np.random.uniform(10000, 100000)]
        if minVal == None:
            minVal = ta_answer
            minguy = chromosome
        else:
            if ((minVal[0] + (FACTOR*minVal[1]))) + abs(minVal[0]-minVal[1])*SUM_FACTOR > (((FACTOR*ta_answer[1]) + ta_answer[0])) + abs(ta_answer[0]-ta_answer[1])*SUM_FACTOR:
                minVal = ta_answer
                minguy = chromosome
        fitness.append(
            1e15/(((ta_answer[0] + FACTOR * ta_answer[1])) + abs(ta_answer[0]-ta_answer[1])*SUM_FACTOR))

        print(
            f'kid: {chromosome} train error: {ta_answer[0]}, validation error: {ta_answer[1]}')
        print()
    print("XXXXX-----XXXXX")
    print()
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
    print()
    print("----")
    print(f'{parent1}x{parent2}---->')
    child1 = np.where(parent1 <= parent2, np.random.uniform(
        parent1-a*d, parent2+b*d), np.random.uniform(parent2-b*d, parent2+a*d))
    child2 = np.where(parent1 <= parent2, np.random.uniform(
        parent1-a*d, parent2+b*d), np.random.uniform(parent2-b*d, parent2+a*d))
    print(f'{child1}+{child2}')
    print('----')
    print()
    return child1, child2


def roulette_selective_breed(selected_population, selected_fitness):
    print()
    print("XXXX-XXXX")
    print("Russian Roullette begins >>>")
    print()
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
        if par_num1 == par_num2:
            par_num2 = (par_num1 + 1) % np.shape(selected_population)[0]
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
    print()
    print("Roullette Ends")
    print("XXXX-XXXX")
    print()
    return mutate_children(np.array(children))


def get_init(chromosome):
    chromosome = np.array(chromosome)
    temp = [chromosome
            for i in range(POPULATION_SIZE)]
    for i in range(len(temp)):
        noise = np.random.normal(chromosome, 0.4 - chromosome)
        indices = np.random.choice(np.arange(
            temp[i].size), replace=False, size=len(temp[i])-MUTATION_SIZE)
        noise[indices] = chromosome[indices]
        temp[i] = noise
    temp[0] = chromosome
    temp = np.array(temp)
    return temp


def get_init2(chromosome):
    chromosome = np.array(chromosome)
    temp = [chromosome
            for i in range(POPULATION_SIZE)]
    for i in range(len(temp)):
        zeroes = np.array([0]*11)
        indices = np.random.choice(np.arange(
            temp[i].size), replace=False, size=6)
        zeroes[indices] = chromosome[indices]
        temp[i] = zeroes
    temp[0] = chromosome
    temp = np.array(temp)
    return mutate_children(temp)


parents = []
try:
    with open("overfit.txt", "r") as f:
        initial_chromosome = np.array(json.load(f))
except:
    print("No overfit...")
    initial_chromosome = np.array([0.0, -1.45799022e-12, -2.28980078e-13,  4.62010753e-11, -1.75214813e-10, -
                                   1.83669770e-15,  8.52944060e-16,  2.29423303e-05, -2.04721003e-06, -1.59792834e-08,  9.98214034e-10])
try:
    with open("store.txt", "r") as store:
        dump = json.load(store)
        parents = np.array(dump)
except:
    print("Starting from init...")

if len(parents) == 0:
    print("starting....")
    parents = get_init2(initial_chromosome)
if len(parents) < POPULATION_SIZE:
    new_parents = mutate_children(parents)
    parents = np.concatenate((parents, new_parents))
    parents = parents[:POPULATION_SIZE]
answer = []
answer_fitness = []
parent_fitness = get_fitness(parents)
parent_sort = np.argsort(-1*parent_fitness)
parents = parents[parent_sort]
parent_fitness = parent_fitness[parent_sort]
try:
    with open("output.txt", "r") as f:
        answer = json.load(f)
        answer = np.array(answer)
        answer_fitness = get_fitness(answer)
        print("answer loaded")
except:
    parent_sort = np.argsort(-1*parent_fitness)
    parents = parents[parent_sort]
    parent_fitness = parent_fitness[parent_sort]
    answer = parents[:10]
    answer_fitness = parent_fitness[:10]
children = parents[: POPULATION_SIZE-MATE_POOL_SIZE]
children_fitness = parent_fitness[: POPULATION_SIZE-MATE_POOL_SIZE]
parents = parents[POPULATION_SIZE-MATE_POOL_SIZE:]
parent_fitness = parent_fitness[POPULATION_SIZE-MATE_POOL_SIZE:]
print("---------")
print()
currgen = 90
for gen in range(1, MAX_GEN+1):
    print()
    print(">>>>>>>>>")
    print()
    print(f'GENERATION : {currgen+gen}')
    print()
    parent_index = np.argsort(-1*parent_fitness)
    parents = parents[parent_index]
    parent_fitness = parent_fitness[parent_index]
    selected_parents = parents[: SELECT_TOP_PARENTS]
    selected_parent_fitness = parent_fitness[: SELECT_TOP_PARENTS]
    selected_kids = children[:SELECT_TOP_KIDS]
    selected_kids_fitness = children_fitness[:SELECT_TOP_KIDS]
    rest = np.concatenate(
        (parents[SELECT_TOP_PARENTS:], children[SELECT_TOP_KIDS:]), axis=0)
    rest_fitness = np.concatenate(
        (parent_fitness[SELECT_TOP_PARENTS:], children_fitness[SELECT_TOP_KIDS:]), axis=0)
    rest_index = np.argsort(rest_fitness*-1)
    rest = rest[rest_index]
    rest_fitness = rest_fitness[rest_index]
    pool = np.concatenate(
        (selected_parents, selected_kids, rest[: MATE_POOL_SIZE-SELECT_TOP_PARENTS-SELECT_TOP_KIDS]))
    pool_fitness = np.concatenate(
        (selected_parent_fitness, selected_kids_fitness, rest_fitness[: MATE_POOL_SIZE-SELECT_TOP_PARENTS-SELECT_TOP_KIDS]))
    print(
        f'Best of Pool:{pool[-1]}->{np.max(pool_fitness)}')
    print(f'Current Pool:')
    print(pool)
    print()
    print("....>>>>>....")
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
    answer = np.concatenate((answer, children), axis=0)
    answer_fitness = np.concatenate((answer_fitness, children_fitness), axis=0)
    answer_sort = np.argsort(-1*answer_fitness)
    answer_fitness = answer_fitness[answer_sort]
    answer = answer[answer_sort]
    answer = answer[:10]
    answer_fitness = answer_fitness[:10]
    print(f'Best of Children: {children[-1]}->{children_fitness[-1]}')
print("XXXXXXX--NEXT TIME---XXXXXX")
print("Parents:")
print(parents)
print("Children:")
print(children)
print("Current Toppers:")
print(answer)
print("Their Fitness:")
print(answer_fitness)
print("BEST !:", minVal, minguy)
print(requests)
dump = np.concatenate((parents, children))
dump_fitness = np.concatenate((parent_fitness, children_fitness))
dump_sort = np.argsort(-1*dump_fitness)
dump = dump[dump_sort]
with open("store.txt", "w") as f:
    json.dump(dump.tolist(), f)
with open("output.txt", "w") as f:
    json.dump(answer.tolist(), f)
