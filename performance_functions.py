from ga import *
import time
import matplotlib.pyplot as plt


# Takes the average over N runs as the table size increases and plots the results
def table_size_performance(num_iterations):
    table_size_variations = [5, 10, 15, 20]
    curr_time = [0] * len(table_size_variations)
    avg_time = []

    # Run that values n times and take an average for better estimation
    for n in range(num_iterations):
        print(make_ordinal(n + 1) + ' Table Size Run... ')
        for i in range(len(table_size_variations)):
            tic = time.perf_counter()
            genetic_algorithm_performance_eval(table_size_variations[i], POP_SIZE, NUM_PARENTS, MUTATE_CHANCE,
                                               INIT_SIZE)
            toc = time.perf_counter()
            curr_time[i] += (toc - tic)
    print('Table Size Testing Done. ')
    print()

    # Take average
    for time_ in curr_time:
        avg_time.append(time_ / num_iterations)

    # plot
    plt.plot(table_size_variations, avg_time)
    plt.xlabel('Table Size')
    plt.ylabel('Time (Seconds)')

    # displaying the title
    plt.title("Table Size vs Time (Seconds)")

    # show the graph
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()


# Takes the average over N runs as the population size increases and plots the results
def pop_size_performance(num_iterations):
    pop_size_variations = [50, 100, 150, 200]
    curr_time = [0] * len(pop_size_variations)
    avg_time = []

    # Run that values n times and take an average for better estimation
    for n in range(num_iterations):
        print(make_ordinal(n + 1) + ' Population Size Run... ')
        for i in range(len(pop_size_variations)):
            tic = time.perf_counter()
            genetic_algorithm_performance_eval(TABLE_SIZE, pop_size_variations[i], NUM_PARENTS, MUTATE_CHANCE,
                                               INIT_SIZE)
            toc = time.perf_counter()
            curr_time[i] += (toc - tic)
    print('Population Size Testing Done. ')
    print()

    # Take average
    for time_ in curr_time:
        avg_time.append(time_ / num_iterations)

    # plot
    plt.plot(pop_size_variations, avg_time)
    plt.xlabel('Population Size')
    plt.ylabel('Time (Seconds)')

    # displaying the title
    plt.title("Population Size vs Time (Seconds)")

    # show the graph
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()


# Takes the average over N runs as the parent size increases and plots the results
def parent_size_performance(num_iterations):
    parent_size_variations = [2, 3, 4, 5, 6, 7]
    curr_time = [0] * len(parent_size_variations)
    avg_time = []

    # Run that values n times and take an average for better estimation
    for n in range(num_iterations):
        print(make_ordinal(n + 1) + ' Number of Parents Run... ')
        for i in range(len(parent_size_variations)):
            tic = time.perf_counter()
            genetic_algorithm_performance_eval(TABLE_SIZE, POP_SIZE, parent_size_variations[i], MUTATE_CHANCE,
                                               INIT_SIZE)
            toc = time.perf_counter()
            curr_time[i] += (toc - tic)
    print('Number of Parents Testing Done. ')
    print()

    # Take average
    for time_ in curr_time:
        avg_time.append(time_ / num_iterations)

    # plot
    plt.plot(parent_size_variations, avg_time)
    plt.xlabel('Number of Parents')
    plt.ylabel('Time (Seconds)')

    # displaying the title
    plt.title("Number of Parents vs Time (Seconds)")

    # show the graph
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()


# Takes the average over N runs as the mutation probability increases and plots the results
def mutation_prob_performance(num_iterations):
    mutation_prob_variations = [0.25, 0.45, 0.65, 0.85, 0.95]
    curr_time = [0] * len(mutation_prob_variations)
    avg_time = []

    # Run that values n times and take an average for better estimation
    for n in range(num_iterations):
        print(make_ordinal(n + 1) + ' Mutation Probability Run... ')
        for i in range(len(mutation_prob_variations)):
            tic = time.perf_counter()
            genetic_algorithm_performance_eval(TABLE_SIZE, POP_SIZE, NUM_PARENTS, mutation_prob_variations[i],
                                               INIT_SIZE)
            toc = time.perf_counter()
            curr_time[i] += (toc - tic)

    print('Mutation Probability Testing Done. ')
    print()

    # Take average
    for time_ in curr_time:
        avg_time.append(time_ / num_iterations)

    # plot
    plt.plot(mutation_prob_variations, avg_time)
    plt.xlabel('Mutation Probability')
    plt.ylabel('Time (Seconds)')

    # displaying the title
    plt.title("Mutation Probability vs Time (Seconds)")

    # show the graph
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()


# Takes the average over N runs as the mutation probability increases and plots the results
def init_pop_performance(num_iterations, variations=[100, 1000, 2500, 5000, 10000]):
    init_pop_variations = variations
    curr_time = [0] * len(init_pop_variations)
    avg_time = []

    # Run that values n times and take an average for better estimation
    for n in range(num_iterations):
        print(make_ordinal(n + 1) + ' Initial Population Run... ')
        for i in range(len(init_pop_variations)):
            tic = time.perf_counter()
            genetic_algorithm_performance_eval(TABLE_SIZE, POP_SIZE, NUM_PARENTS, MUTATE_CHANCE, init_pop_variations[i])
            toc = time.perf_counter()
            curr_time[i] += (toc - tic)

    print('Initial Population Testing Done. ')
    print()

    # Take average
    for time_ in curr_time:
        avg_time.append(time_ / num_iterations)

    # plot
    plt.plot(init_pop_variations, avg_time)
    plt.xlabel('Initial Population')
    plt.ylabel('Time (Seconds)')

    # displaying the title
    plt.title("Initial Population vs Time (Seconds)")

    # show the graph
    plt.show()

    plt.clf()
    plt.cla()
    plt.close()


# This function is used for the performance evaluation, removed the printing so it doesn't clutter the screen
def genetic_algorithm_performance_eval(table_size, pop_size, num_parents, mutate_prob, init_pop, piece):
    new_population = create_population(init_pop, table_size, piece)

    best_result = -1
    best_state = []

    for generation in range(NUM_GENERATIONS):

        # Find the fitness for each chromosome in the population
        fitness = cal_pop_fitness(new_population, table_size)

        # Select the best parents in the population for mating
        parents = select_best(new_population, fitness, num_parents)

        # Generate the crossover
        offspring = cross_over(parents, pop_size)

        # Adding variation using random mutation
        offspring_mutation = mutate(offspring, mutate_prob, piece)

        # The best result in the current population
        curr_state = select_best(new_population, fitness)
        curr_result = count_safe_pieces(curr_state[0], table_size, piece)
        if best_result < curr_result:
            best_result = curr_result
            best_state = curr_state[0]

        # exit loop if best result is equal to size of board
        if best_result == table_size:
            break

        # Creating new population based on a random number of surviving parents and their offspring
        number_surviving = np.random.randint(1, len(parents))
        parents_fitness = cal_pop_fitness(parents, table_size)
        best_parents = select_best(parents, parents_fitness, number_surviving)
        new_population[0:] = best_parents
        new_population += offspring_mutation


# Takes as input the number of times to run the program to get a average run time, the higher the more accurate
# but also the more time it take to run
def performance_evaluation(num_iterations):
    # table_size_performance(num_iterations)
    # pop_size_performance(num_iterations)
    # parent_size_performance(num_iterations)
    mutation_prob_performance(num_iterations)
    # init_pop_performance(num_iterations)
