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

    def shift_to(self, shifts, target_row, target_col):
        """Shift the current board's bits based on the provided shifts to align with the given position (target_row, target_col)."""
        shifted_board = BitBoard(self.N)
        for (row_shift, col_shift) in shifts:
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
        
        # Initialize the 8 different bitboards for each knight move
        self.knight_move_boards = [BitBoard(N) for _ in self.knight_shifts]
        
        # Precompute the possible moves for each knight move direction
        self.precompute_knight_moves()

    def precompute_knight_moves(self):
        """Precompute the possible moves for each knight move direction."""
        for idx, (row_shift, col_shift) in enumerate(self.knight_shifts):
            if 0 <= row_shift < self.N and 0 <= col_shift < self.N:
                self.knight_move_boards[idx].set_bit(row_shift, col_shift)

    def knight_moves_from(self, row, col):
        """Generate possible moves for a knight at a given position."""
        moves = BitBoard(self.N)
        
        # For each knight move direction, shift the precomputed move board to the target position
        for move_board in self.knight_move_boards:
            knight_moves = move_board.shift_to(self.knight_shifts, row, col)
            moves.bitboard |= knight_moves.bitboard
            
        return moves

    def pawn_moves_from(self, row, col):
        """Generate possible capture moves for a pawn at a given position."""
        moves = BitBoard(self.N)
        
        # Capture squares for white pawn
        capture_shifts = [(-1, -1), (-1, 1)]  # Diagonal moves for capture

        for (row_shift, col_shift) in capture_shifts:
            capture_row = row + row_shift
            capture_col = col + col_shift
            # Set the bit at the capture position if it is within the board's boundaries
            if 0 <= capture_row < self.N and 0 <= capture_col < self.N:
                moves.set_bit(capture_row, capture_col)
                
        return moves

    def rook_moves_from(self, row, col):
        """Generate possible moves for a rook at a given position using bitboards."""
        moves = BitBoard(self.N)
        
        position = moves._get_position(row, col)
        occupied = self.black_board.bitboard | self.white_board.bitboard
        same_color = self.white_board.bitboard  # Assuming white rook for simplicity
        rook_bit = 1 << position
        
        # Helper function to generate rook moves
        def spread(bit, shift_func, max_steps):
            for _ in range(max_steps):
                bit = shift_func(bit)
                if bit & same_color:  # Stop if it's the same color piece
                    break
                moves.bitboard |= bit
                if bit & occupied:  # Stop if any piece is encountered
                    break

        # Calculate the distances to each boundary from the current position
        top_boundary = self.N - 1 - row
        bottom_boundary = row
        left_boundary = col
        right_boundary = self.N - 1 - col

        # North
        spread(rook_bit, lambda b: (b << self.N), top_boundary)
        
        # South
        spread(rook_bit, lambda b: (b >> self.N), bottom_boundary)
        
        # East
        spread(rook_bit, lambda b: (b << 1), right_boundary)
        
        # West
        spread(rook_bit, lambda b: (b >> 1), left_boundary)
        
        return moves

    def bishop_moves_from(self, row, col):
        """Generate possible moves for a bishop at a given position using bitboards."""
        moves = BitBoard(self.N)
        
        position = moves._get_position(row, col)
        occupied = self.black_board.bitboard | self.white_board.bitboard
        same_color = self.white_board.bitboard  # Assuming white bishop for simplicity
        bishop_bit = 1 << position
        
        # Helper function to generate bishop moves
        def spread(bit, shift_func, max_steps):
            for _ in range(max_steps):
                bit = shift_func(bit)
                if bit & same_color:  # Stop if it's the same color piece
                    break
                moves.bitboard |= bit
                if bit & occupied:  # Stop if any piece is encountered
                    break
        
        # Calculate the distances to each boundary from the current position
        top_boundary = self.N - 1 - row
        bottom_boundary = row
        left_boundary = col
        right_boundary = self.N - 1 - col

        # North-East
        spread(bishop_bit, lambda b: (b << (self.N + 1)), min(top_boundary, right_boundary))
        
        # North-West
        spread(bishop_bit, lambda b: (b << (self.N - 1)), min(top_boundary, left_boundary))
        
        # South-East
        spread(bishop_bit, lambda b: (b >> (self.N - 1)), min(bottom_boundary, right_boundary))
        
        # South-West
        spread(bishop_bit, lambda b: (b >> (self.N + 1)), min(bottom_boundary, left_boundary))
        
        return moves

    def queen_moves_from(self, row, col):
        return self.bishop_moves_from(row, col) | self.rook_moves_from(row, col)

def main():
    N = 8
    chessboard = ChessBoard(N)
    
    piece_positions = [ (0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]

    for (row,col) in piece_positions:
        moves = chessboard.knight_moves_from(row,col)
        moves.visualize()
        moves = chessboard.rook_moves_from(row,col)
        moves.visualize()
        moves = chessboard.bishop_moves_from(row,col)
        moves.visualize()
        moves = chessboard.queen_moves_from(row,col)
        moves.visualize()
        moves = chessboard.pawn_moves_from(row,col)
        moves.visualize()


    print("test done")

if __name__ == "__main__":
         main()