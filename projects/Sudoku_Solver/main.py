from typing import List, Tuple, Optional

# Type alias for a 9x9 Sudoku board
Board = List[List[int]]  


def read_board_from_file(filename: str) -> Board:
    """
    Reads a Sudoku puzzle from a text file.
    Each line in the file should contain 9 comma-separated integers.
    Returns a 9x9 board as a list of lists of integers.
    Raises ValueError if the board dimensions are invalid.
    """
    board = []
    with open(filename, 'r') as f:
        for line in f:
            row = list(map(int, line.strip().split(',')))
            if len(row) != 9:
                raise ValueError(f"Invalid row length: {row}")
            board.append(row)
    if len(board) != 9:
        raise ValueError("Invalid board height.")
    return board


def write_board_to_file(board: Board, filename: str) -> None:
    """
    Writes a Sudoku puzzle to a text file.
    Each row is written as a comma-separated string of numbers.
    """
    with open(filename, 'w') as f:
        for row in board:
            f.write(",".join(str(num) for num in row) + "\n")


def is_valid_board(board: Board) -> bool:
    """
    Checks whether the initial board has any conflicting numbers.
    Ensures no duplicates in any row, column, or 3x3 subgrid.
    Returns True if the board is valid, False otherwise.
    """
    for i in range(9):
        # Check for duplicate numbers in each row
        row = [num for num in board[i] if num != 0]
        if len(row) != len(set(row)):
            return False
        # Check for duplicate numbers in each column
        col = [board[r][i] for r in range(9) if board[r][i] != 0]
        if len(col) != len(set(col)):
            return False

    # Check for duplicate numbers in each 3x3 subgrid
    for box_row in range(3):
        for box_col in range(3):
            nums = []
            for i in range(3):
                for j in range(3):
                    num = board[box_row*3 + i][box_col*3 + j]
                    if num != 0:
                        nums.append(num)
            if len(nums) != len(set(nums)):
                return False

    return True


def find_empty(board: Board) -> Optional[Tuple[int, int]]:
    """
    Searches the board for the next empty cell (represented by 0).
    Returns a tuple (row, col) of the empty cell's position.
    Returns None if no empty cells are left.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def is_valid_move(board: Board, row: int, col: int, num: int) -> bool:
    """
    Checks whether placing a number at a specific cell is valid.
    Ensures no conflicts in the corresponding row, column, or 3x3 subgrid.
    Returns True if the move is allowed, False otherwise.
    """
    # Check row
    if any(board[row][x] == num for x in range(9)):
        return False

    # Check column
    if any(board[y][col] == num for y in range(9)):
        return False

    # Check 3x3 subgrid
    box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_start_row + i][box_start_col + j] == num:
                return False

    return True


def solve_sudoku(board: Board) -> bool:
    """
    Solves the Sudoku puzzle using a recursive backtracking algorithm.
    Modifies the board in-place.
    Returns True if a solution is found, False if the puzzle is unsolvable.
    """
    empty = find_empty(board)
    if not empty:
        # No empty cells left; puzzle is solved
        return True

    row, col = empty

    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num  # Tentatively place number

            if solve_sudoku(board):
                return True  # Found a valid solution path

            board[row][col] = 0  # Undo move and backtrack

    # No valid number could be placed in this cell; trigger backtracking
    return False


if __name__ == "__main__":
    # Input and output file names
    input_file = "sudoku_input3.txt"
    output_file = "sudoku_output3.txt"

    try:
        # Read the puzzle from input file
        puzzle = read_board_from_file(input_file)
    except Exception as e:
        print(f"Failed to read puzzle: {e}")
        exit(1)

    # Validate the initial puzzle for conflicts
    if not is_valid_board(puzzle):
        print("Invalid Sudoku puzzle — conflicting numbers detected.")
        exit(1)

    # Attempt to solve the puzzle
    if solve_sudoku(puzzle):
        # Write the solved puzzle to output file
        write_board_to_file(puzzle, output_file)
        print(f"Puzzle solved successfully! Solution written to {output_file}")
    else:
        # No solution exists for the given puzzle
        print("No solution exists for the provided puzzle.")
