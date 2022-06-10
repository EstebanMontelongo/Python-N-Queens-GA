from chess import *
from other_tools import *
from constants import *
import random
import numpy as np
# import time

"""
Used the logic from this post 
https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6
and the Local Search Power Point.
"""


# [3, 1, 4, 2]
# [1, 2, 3, 4]
# [3, 2, 4, 1]
# .
# .
# .
# [1, 4, 2, 3]

# create a population with each parent having N chromosomes
def create_population(pop_size, chrom_size, table_size, piece):
    population = []
    left_over = chrom_size - table_size
    for i in range(0, pop_size):
        if piece == 'bQ' or piece == 'bR':
            parentx = list(range(table_size))
            parenty = list(random.sample(range(0, table_size), table_size))
        else:
            parentx = list(random.sample(range(0, table_size), table_size))
            parenty = list(random.sample(range(0, table_size), table_size))
        if left_over != 0:
            parentx += (list(random.choices(list(range(0, table_size)), k=left_over)))
            parenty += (list(random.choices(list(range(0, table_size)), k=left_over)))

        parent = []
        for j in range(len(parentx)):
            parent.append([parentx[j], parenty[j]])

        population.append(parent)
    # for pop in population:
    #    print(pop)

    return population


# [3, 1, 4, 2] Score 1
# [1, 2, 3, 4] Score 2
# [3, 2, 4, 1] Score 3
# .
# .
# .
# [1, 4, 2, 3] Score n

# calculating the fitness score for all the current parents in the population
def cal_pop_fitness(population, table_size):
    fitness = []
    for parent in population:
        fitness.append(count_safe_pieces(parent, table_size, PIECE))
    return fitness


# 1st Score
# 2nd Score
# .
# .
# .
# nth Score

# select the N best parents in the mating pool, return then as a list of parents
def select_best(population, fitness, num_parents=1):
    if len(population) < num_parents:
        print("The number of parents must be smaller or equal to the population size")
        quit()

    parents = []
    temp_fitness = fitness.copy()

    # find N number of best parents, return their indices within the population
    for i in range(num_parents):
        # find current max value
        max_value = max(temp_fitness)
        # find its index in original fitness list and save it
        max_index = temp_fitness.index(max_value)
        parents.append(population[max_index])
        # remove the max value from tmp list to find the next largest fitness score
        temp_fitness[max_index] = -1

    return parents


# [3, 1, 4, 2] parent 1
# [1, 2, 3, 4] parent 2
# children
# [3, 2, 3, 4] child 1
# [1, 1, 4, 2] child 2
# [3, 1, 3, 4] child 3
# .
# .
# .
# [x, x, x, x] child n


# Cross over two random parents with random combination
def cross_over(parents, num_offspring):
    children = []

    # If parent
    if len(parents[0]) == 1 or len(parents) == 1:
        children.append(list([0, 0]))
        return children

    for i in range(num_offspring):
        # Select two random parent indices
        rand_idx1 = np.random.randint(1, len(parents))
        rand_idx2 = np.random.randint(1, len(parents))
        # Select an index to spilt the parent
        c = np.random.randint(1, len(parents[0]))
        # Append the two parents lists based off c index
        child = parents[rand_idx1][0:c] + parents[rand_idx2][c:]
        children.append(child)

    return children


# [3, 1, 3*, 4] child 1 => [3, 1, 2, 4]
# [1, 1, 4, 2] child 2
# [3, 1, 3, 4] child 3
# .
# .
# .
# [x, x, x, x] child n


# Given a mutation probability and a some children
# randomly mutate a chromosome with a random valid chromosome
def mutate(children, mutate_chance, piece, table_size):
    # If mutation probability is met mutate children
    if random.random() <= mutate_chance:
        # Select a random start and end indices to mutate
        for child in children:
            # Select a random child xy index
            rand_xy_idx = random.randint(0, len(child) - 1)
            # Select random y index
            rand_y = random.randint(0, table_size - 1)
            # mutate the selected child xy index
            #   note: if Queen or Rook we don't change the x value,
            #   just the y index
            if piece != 'bQ' and piece != 'bR':
                rand_x = random.randint(0, table_size - 1)
                child[rand_xy_idx][0] = rand_x
            child[rand_xy_idx][1] = rand_y
            # print(children[i])
    return children


def genetic_algorithm():
    new_population = create_population(INIT_SIZE, CHROMOSOME_MAX[PIECE], TABLE_SIZE, PIECE)

    best_result = -1
    best_state = []

    for generation in range(NUM_GENERATIONS):

        # Find the fitness for each chromosome in the population
        fitness = cal_pop_fitness(new_population, TABLE_SIZE)  # Time 0.025

        # Select the best parents in the population for mating
        parents = select_best(new_population, fitness, NUM_PARENTS)  # Time 0.00

        # The best result in the current population ---- Time 0.001 ----
        curr_states = select_best(new_population, fitness)
        curr_result = count_safe_pieces(curr_states[0], TABLE_SIZE, PIECE)
        curr_best_state = curr_states[0]
        if best_result < curr_result:
            # print("Current result " + str(curr_result))
            # print("current_sate[0]= " + str(curr_states[0]))
            best_result = curr_result
            best_state = curr_best_state

        # Fancy printing of generation number
        print(make_ordinal(generation + 1) + ' Generation best result is ' + str(best_result))
        # exit loop if best result is equal to size of board
        if best_result == CHROMOSOME_MAX[PIECE]:
            best_state = curr_best_state
            break

        # Generate the crossover
        offspring = cross_over(parents, POP_SIZE)  # Time 0.001

        # Adding variation using random mutation
        offspring_mutation = mutate(offspring, MUTATE_CHANCE, PIECE, TABLE_SIZE)  # Time 0.0001

        # # Creating new population based on a random number of surviving parents and their offspring
        # # Surviving parents
        # # ----- Total Time 0.03 -----
        # number_surviving = np.random.randint(1, len(parents))
        # # Calculate the fitness score of the best parents
        # parents_fitness = cal_pop_fitness(parents, TABLE_SIZE)
        # # Get the best surviving parents
        # best_parents = select_best(parents, parents_fitness, number_surviving)
        # Delete old population and replace it with best parents and
        # the offspring
        # ---- Total Time 0.001 ----
        new_population[0:] = parents
        new_population += offspring_mutation

    print("Best solution is state : ", best_state)
    print("Best solution fitness : ", best_result)
    best_state = remove_attacking_pieces(best_state, TABLE_SIZE, PIECE)
    print_board(best_state)


# # Use this to test the speed od functions
# # starting time
# start = time.time()
# # end time
# end = time.time()
# # total time taken
# print(f"Runtime of the program is {end - start}")

