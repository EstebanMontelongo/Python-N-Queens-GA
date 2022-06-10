import pygame as p
from constants import *

""" 
Displaying the chess board I got help from this youtube video: https://www.youtube.com/watch?v=EnYui0e73Rs
Queen png image from: https://www.pngfind.com/download/bJmmbw_chess-queen-png-download-king-crown-icon-png/
"""


def print_board(state):
    # Initializing game constants
    global WIDTH, HEIGHT, DIMENSIONS, SQ_SIZE, MAX_FPS, IMAGES

    DIMENSIONS = TABLE_SIZE
    WIDTH = HEIGHT = 768
    SQ_SIZE = HEIGHT // DIMENSIONS
    MAX_FPS = 15
    IMAGES = {'bQ': p.transform.scale(p.image.load("bQ.png"), (SQ_SIZE, SQ_SIZE)),
              'bB': p.transform.scale(p.image.load("bB.png"), (SQ_SIZE, SQ_SIZE)),
              'bK': p.transform.scale(p.image.load("bK.png"), (SQ_SIZE, SQ_SIZE)),
              'bR': p.transform.scale(p.image.load("bR.png"), (SQ_SIZE, SQ_SIZE))
              }
    # Initialize game stuff
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState(state)
    running = True

    # Loop & draw board until user presses exit
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        if not running:
            p.display.quit()


def draw_game_state(screen, gs):
    # draw squares on the board
    draw_board(screen)
    # draw pieces on the board
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color((240, 217, 181)), p.Color((181, 136, 99))]

    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[c][r]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


class GameState:
    def __init__(self, state):
        self.state = state
        self.board = set_state(self.state, PIECE, TABLE_SIZE)


def set_state(state, piece_type, table_size):
    board = [[[] for i in range(table_size)] for i in range(table_size)]

    # Set all cells to empty
    for r in range(table_size):
        for c in range(table_size):
            board[r][c] = '--'
    # Place pieces in cell is valid
    for i in range(len(state)):
        x, y = state[i][0], state[i][1]
        if x >= 0 and y >= 0:
            board[x][y] = piece_type
    # print(board)
    return board


def piece_logic(row, row2, col, col2, piece, table_size):
    logic_dict = {'bQ': col == col2 or abs(row - row2) == abs(col - col2),
                  'bB': abs(row - row2) == abs(col - col2),
                  'bR': (row == row2 and col == col2) or col == col2 or row == row2,
                  'bK':
                      (
                              ((row == row2 and col == col2) if
                               (0 <= row <= table_size and 0 <= col <= table_size) else False) or
                              (((row + 2) == row2 and (col - 1) == col2) if
                               (0 <= (row + 2) <= table_size and 0 <= (col - 1) <= table_size) else False) or
                              (((row - 2) == row2 and (col - 1) == col2) if
                               (0 <= (row - 2) <= table_size and 0 <= (col - 1) <= table_size) else False) or
                              (((row + 2) == row2 and (col + 1) == col2) if
                               (0 <= (row + 2) <= table_size and 0 <= (col + 1) <= table_size) else False) or
                              (((row - 2) == row2 and (col + 1) == col2) if
                               (0 <= (row - 2) <= table_size and 0 <= (col + 1) <= table_size) else False) or
                              (((row + 1) == row2 and (col + 2) == col2) if
                               (0 <= (row + 1) <= table_size and 0 <= (col + 2) <= table_size) else False) or
                              (((row - 1) == row2 and (col + 2) == col2) if
                               (0 <= (row - 1) <= table_size and 0 <= (col + 2) <= table_size) else False) or
                              (((row + 1) == row2 and (col - 2) == col2) if
                               (0 <= (row + 1) <= table_size and 0 <= (col - 2) <= table_size) else False) or
                              (((row - 1) == row2 and (col - 2) == col2) if
                               (0 <= (row - 1) <= table_size and 0 <= (col - 2) <= table_size) else False)
                      )

                  }
    return logic_dict[piece]


# removes the queens that are under attack for displaying a solution
def remove_attacking_pieces(state, table_size, piece):
    print("original" + str(state))
    state_copy = state.copy()
    for i in range(0, len(state)):
        xy_pos_1 = state[i]
        for j in range(i + 1, len(state)):
            xy_pos_2 = state[j]
            x1, x2, y1, y2 = xy_pos_1[0], xy_pos_2[0], xy_pos_1[1], xy_pos_2[1]
            # checks is other queens are under attack, if so remove the current queen
            if piece_logic(x1, x2, y1, y2, piece, table_size):
                state_copy[i][0] = -1
                state_copy[i][1] = -1
                break

    print("copy" + str(state_copy))
    return state_copy


# Check if piece is attacking another piece
def count_safe_pieces(state, table_size, piece):
    safe_pieces = 0
    for i in range(0, len(state)):
        safe = True
        xy_pos_1 = state[i]
        # checks if pieces are under attack
        for j in range(i + 1, len(state)):
            xy_pos_2 = state[j]
            x1, x2, y1, y2 = xy_pos_1[0], xy_pos_2[0], xy_pos_1[1], xy_pos_2[1]
            if piece_logic(x1, x2, y1, y2, piece, table_size):
                safe = False
                break
        if safe:
            safe_pieces += 1
    return safe_pieces

