import time
import argparse

def print_pretty(grid):
    '''
    Just a helper function to have a pretty sudoku grid output
    :param grid:
    :return:
    '''
    for i in range(len(grid)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(len(grid[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(grid[i][j])
            else:
                print(str(grid[i][j]) + " ", end="")


def is_empty(grid):
    '''
    A function to check if current grid position is empty
    :param grid:
    :return: i as row, j as column as a tuple
    '''
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)

    return None

def validation(grid, number, position):

    # Validate row
    for i in range(len(grid[0])):
        if grid[position[0]][i] == number and position[1] != i:
            return False

    # Validate column
    for i in range(len(grid)):
        if grid[i][position[1]] == number and position[0] != i:
            return False

    # Validate 3x3 box
    # Check in which box we are in - upper left box is 0 0 - bottom right box is 3 3
    x_box = position[1] // 3
    y_box = position[0] // 3

    for i in range(y_box * 3, y_box * 3 + 3):
        for j in range(x_box * 3, x_box * 3 + 3):
            if grid[i][j] == number and (i,j) != position:
                return False

    return True


def backtrack(grid):
    '''
    The actual backtracking algorithm with runs until a solution was found
    :param grid:
    :return:
    '''
    empty = is_empty(grid)
    if not empty:
        return True
    else:
        row, column = empty

    # Try to put the numbers into the board
    for i in range(1,10):
        if validation(grid, i, (row, column)):
            grid[row][column] = i

            if backtrack(grid):
                return True

            grid[row][column] = 0
            
    return False


def validate_file(grid):
    '''
    A very simple function to check if the text file has a valid structure
    :param grid:
    :return:
    '''
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            if not 0 <= grid[i][j] <= 9:
                print("No valid structure. Only integer values between 0 and 9 are allowed.")
                exit()


parser = argparse.ArgumentParser(description="Sudoku Solver")
parser.add_argument('--file', help='Textfile with Sudoku grid')
args = parser.parse_args()



with open(args.file) as f:
    board = [list(map(int,line.split())) for line in f]


validate_file(board)
start = time.time()
backtrack(board)
print("\nSolution was found after {} seconds \n".format(round(time.time() - start)))
print_pretty(board)