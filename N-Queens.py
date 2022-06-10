from ga import *
import cython
from chess import *
from performance_functions import performance_evaluation


def main():
    genetic_algorithm()
    # performance_evaluation(100)
    # state = [[0, 7], [1, 0], [2, 6], [3, 3], [4, 1], [5, 4], [6, 2], [7, 5]]
    # print(state)
    # print(count_safe_pieces(state, TABLE_SIZE, PIECE))
    # print_board(state)
    # state = remove_attacking_pieces(state, TABLE_SIZE, PIECE)
    # print_board(state)


if __name__ == '__main__':
    main()
