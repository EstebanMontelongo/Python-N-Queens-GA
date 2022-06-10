"""
Here you can play with these hyper parameters, to try and get a better solution
"""
# All the pieces
QUEEN = 'bQ'
KNIGHT = 'bK'
BISHOP = 'bB'
ROOK = 'bR'
# Hyper parameters
TABLE_SIZE = 20
POP_SIZE = 100
INIT_SIZE = 1000
NUM_PARENTS = 2
NUM_GENERATIONS = 100
MUTATE_CHANCE = 0.95
PIECE = KNIGHT

# Extra
K = int((TABLE_SIZE - 1)/2)
CHROMOSOME_MAX = {
                    QUEEN: TABLE_SIZE,
                    BISHOP: 2 * TABLE_SIZE - 2,
                    ROOK: TABLE_SIZE,
                    KNIGHT: int((TABLE_SIZE * TABLE_SIZE) / 2) if (TABLE_SIZE % 2 == 0) else int(2*(K*K + K) + 1)
                  }

"""
Best values for 50 size
    TABLE_SIZE = 50
    POP_SIZE = 100
    INIT_SIZE = 1000
    NUM_PARENTS = 4
    NUM_GENERATIONS = 50000
    MUTATE_CHANCE = 0.95
"""
