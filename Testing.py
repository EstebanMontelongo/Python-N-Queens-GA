# This is a general bitboard class.
class BitBoard:

    # Constructor (initialize the object)
    def __init__(self, N):
        self.N = N
        self.bitboard = 0
        # All 8 possible knight moves
        self.knight_shifts = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]

    def _get_position(self, row, col):
        """Convert (row, col) to linear position."""
        return row * self.N + col

    def set_bit(self, row, col):
        """Set a bit at (row, col)."""
        if row < 0 or col < 0 or row >= self.N or col >= self.N:
            return  # Ignore positions outside the board
        position = self._get_position(row, col)
        self.bitboard |= (1 << position)

    def clear_bit(self, row, col):
        """Clear a bit at (row, col)."""
        position = self._get_position(row, col)
        self.bitboard &= ~(1 << position)

    def is_bit_set(self, row, col):
        """Check if a bit at (row, col) is set."""
        position = self._get_position(row, col)
        return (self.bitboard & (1 << position)) != 0

    def shift_to(self, target_row, target_col):
        """Shift the current board's bits to align with the given position (target_row, target_col)."""
        shifted_board = BitBoard(self.N)
        for (row_shift, col_shift) in self.knight_shifts:
            shifted_row = target_row + row_shift
            shifted_col = target_col + col_shift
            # Set the bit at the shifted position if it is within the board's boundaries
            if 0 <= shifted_row < self.N and 0 <= shifted_col < self.N:
                shifted_board.set_bit(shifted_row, shifted_col)
        return shifted_board

    def visualize(self):
        """Visualize the NxN board."""
        for row in range(self.N):
            for col in range(self.N):
                if self.is_bit_set(row, col):
                    print("1", end=" ")
                else:
                    print("0", end=" ")
            print()  # Newline for each row
        print()
    
    def copy(self):
        new_board = BitBoard(self.N)
        new_board.bitboard = self.bitboard
        return new_board

    def __and__(self, other):
        """Bitwise AND between two bitboards."""
        result = BitBoard(self.N)
        result.bitboard = self.bitboard & other.bitboard
        return result

    def __or__(self, other):
        """Bitwise OR between two bitboards."""
        result = BitBoard(self.N)
        result.bitboard = self.bitboard | other.bitboard
        return result

    def __xor__(self, other):
        """Bitwise XOR between two bitboards."""
        result = BitBoard(self.N)
        result.bitboard = self.bitboard ^ other.bitboard
        return result

    def __iand__(self, other):
        self.bitboard &= other.bitboard
        return self

    def __ior__(self, other):
        self.bitboard |= other.bitboard
        return self

    def __ixor__(self, other):
        self.bitboard ^= other.bitboard
        return self

    def __lshift__(self, shift_amount):
        """Left shift the bitboard."""
        result = BitBoard(self.N)
        result.bitboard = self.bitboard << shift_amount
        return result

    def __rshift__(self, shift_amount):
        """Right shift the bitboard."""
        result = BitBoard(self.N)
        result.bitboard = self.bitboard >> shift_amount
        return result

    def __invert__(self):
        """Bitwise NOT operation."""
        result = BitBoard(self.N)
        result.bitboard = ~self.bitboard
        return result

    def __ilshift__(self, shift_amount):
        self.bitboard <<= shift_amount
        return self

    def __irshift__(self, shift_amount):
        self.bitboard >>= shift_amount
        return self

    def __eq__(self, other):
        return self.N == other.N and self.bitboard == other.bitboard

    def __ne__(self, other):
        return not self.__eq__(other)


class ChessBoard:

    def __init__(self, N):
        self.N = N
        self.board_size = N * N

        # Full board pieces
        self.black_board =  BitBoard(N)
        self.white_board =  BitBoard(N)

        # Each bitboard for black pieces
        self.black_queen_board =  BitBoard(N)
        self.black_king_board =  BitBoard(N)
        self.black_bishop_board =  BitBoard(N)
        self.black_pawn_board =  BitBoard(N)
        self.black_rook_board =  BitBoard(N)
        self.black_knight_board =  BitBoard(N)

        # Each bitboard for white pieces
        self.white_queen_board =  BitBoard(N)
        self.white_king_board =  BitBoard(N)
        self.white_bishop_board =  BitBoard(N)
        self.white_pawn_board =  BitBoard(N)
        self.white_rook_board =  BitBoard(N)
        self.white_knight_board =  BitBoard(N)

        # All 8 possible knight moves
        self.knight_shifts = [
            (-2, -1), (-1, -2), (1, -2), (2, -1),
            (2, 1), (1, 2), (-1, 2), (-2, 1)
        ]

        
        # 2D array to store precomputed knight moves for every position
        # Memory O(N^2)
        self.knight_move_boards = [[BitBoard(N) for _ in range(N)] for _ in range(N)]
        
        # Precompute the possible moves for each position on the board
        self.precompute_knight_moves()

    def precompute_knight_moves(self):
        """Precompute the possible moves for each position on the board."""
        for x in range(self.N):
            for y in range(self.N):
                for dx, dy in self.knight_shifts:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < self.N and 0 <= new_y < self.N:
                        self.knight_move_boards[x][y].set_bit(new_x, new_y)

    def knight_moves_from(self, row, col):
        """Return the precomputed moves for a knight at the given position."""
        return self.knight_move_boards[row][col]

def main():
    N = 64
    chessboard = ChessBoard(N)
    
    knight_moves = [ (0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8)]

    for (row,col) in knight_moves:
        moves = chessboard.knight_moves_from(row,col)  # Moves for a knight at position (1, 0)
        moves.visualize()




if __name__ == "__main__":
         main()