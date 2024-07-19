global width
global height
global cell_size
global moves


def print_board(board):
    global width, height, cell_size
    print(" " + ("-" * (width * (cell_size + 1) + 3)))
    for i in range(height, 0, -1):
        row = f"{i}| {' '.join(board[i])} |"
        print(row)
    print(" " + ("-" * (width * (cell_size + 1) + 3)))
    if cell_size == 1:
        bottom_border = "   "
    elif cell_size == 2:
        bottom_border = "    "
    elif cell_size == 3:
        bottom_border = "      "
    for i in range(1, width + 1):
        bottom_border += str(i) + (" " * cell_size)
    print(bottom_border)


def check_moves(board, knight_position, knight_past_positions, total_check=False):
    global cell_size, moves
    possible_outcomes = 0
    row, column = knight_position
    moves = {
        1: (+2, +1),
        2: (+2, -1),
        3: (+1, +2),
        4: (+1, -2),
        5: (-2, +1),
        6: (-2, -1),
        7: (-1, +2),
        8: (-1, -2)
    }
    # Create a list of the moves possible from the current knight position
    if not total_check:
        for move in moves.values():
            dy, dx = move
            test_row = row + dy
            test_column = column + dx
            test_move = (test_row, test_column)
            if test_move in knight_past_positions:  # If the knight has been to that cell don't check it.
                continue
            elif is_on_board(test_move):
                y, x = test_move
                check_moves(board, test_move, knight_past_positions, total_check=True)
    elif total_check:  # Possible legal moves from each legal move are counted. The cell is then set to the total
        for i, move in enumerate(moves.values(), 1):
            dy, dx = move
            test_row = row + dy
            test_column = column + dx
            test_move = (test_row, test_column)
            if test_move not in knight_past_positions and is_on_board(test_move):
                possible_outcomes += 1
            # Subtract 1 from possible_outcomes if there is a possible move. (Can't move back to where you've been)
            if i == 8 and possible_outcomes > 0:
                board[column][row - 1] = (" " * (cell_size - 1)) + str(possible_outcomes - 1)
            elif i == 8 and possible_outcomes == 0:
                board[column][row - 1] = (" " * (cell_size - 1)) + str(0)
    return possible_outcomes


def is_on_board(user_input):
    global width, height
    y, x = user_input
    try:
        if x < 1 or x > height or y < 1 or y > width:
            return False
        return True
    except ValueError:
        return False


def initialise_board(board):
    global width, height, cell_size
    cell = '_' * cell_size
    for i in range(1, height + 1):
        board[i] = [cell] * width
    return board


def set_cell_size():
    global width, height
    total_cells = width * height
    if total_cells < 10:
        cell_size = 1
        return cell_size
    elif 10 <= total_cells < 100:
        cell_size = 2
        return cell_size
    elif 100 <= total_cells:
        cell_size = 3
        return cell_size


def is_valid_board(user_input):
    try:
        x, y = map(int, user_input.split())
        if x < 1 or y < 1:
            print("Invalid dimensions!")
            return False
        return True
    except ValueError:
        print("Invalid dimensions!")
        return False


def set_board_dimensions():
    global width, height, cell_size
    while True:
        board_dimensions = input("Enter your board dimensions: ")
        if not is_valid_board(board_dimensions):
            continue
        width, height = map(int, board_dimensions.split())
        break
    cell_size = set_cell_size()


def set_past_positions(knight_past_positions, board):
    for y, x in knight_past_positions:
        board[x][y - 1] = (" " * (cell_size - 1)) + "*"


def remaining_moves(knight_position, knight_past_positions):
    global moves
    row, column = knight_position
    for move in moves.values():
        dy, dx = move
        test_row = row + dy
        test_column = column + dx
        test_move = (test_row, test_column)
        if is_on_board(test_move) and test_move not in knight_past_positions:
            return True
    return False

def check_win_loss(knight_past_positions, knight_position):
    global width, height
    if len(knight_past_positions) == width * height:
        print("What a great tour! Congratulations!")
        exit()
    elif not remaining_moves(knight_position, knight_past_positions):
        print(f'No more possible moves!\nYour knight visited {len(knight_past_positions)} squares!')
        exit()


def add_tuples(t1, t2):
    return tuple(a + b for a, b in zip(t1, t2))


def is_L_move(knight_past_positions, knight_position):
    global moves
    last_y, last_x = knight_past_positions[-1]
    y, x = knight_position
    for move in moves.values():
        if add_tuples((last_y, last_x), move) == (y, x):
            return True
    return False



def set_knight_position(knight_past_positions, initialising=False):
    prompt = "Enter the knight's starting position: " if initialising else "Enter your next move: "

    while True:
        knight_position = input(prompt)
        try:
            y, x = map(int, knight_position.split())
            if is_on_board((y, x)):
                if initialising or (is_L_move(knight_past_positions, (y, x)) and (y, x) not in knight_past_positions):
                    return y, x
                else:
                    print("Invalid position!" if initialising else "Invalid move!", end='')
            else:
                print("Invalid position!" if initialising else "Invalid move!", end='')
        except ValueError:
            print("Invalid position!" if initialising else "Invalid move!", end='')


def is_safe(x, y, test_board):
    global width, height
    if 0 <= x < height and 0 <= y < width and test_board[x][y] == -1:
        return True
    return False

def solve_kt(board, test_board, pos, curr_x, curr_y):
    global width, height, cell_size
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    if pos == ((width * height) + 1):
        return True

    # Try all next moves from the current coordinate x, y
    for i in range(8):
        new_x = curr_x + move_x[i]
        new_y = curr_y + move_y[i]
        if is_safe(new_x, new_y, test_board):
            # This will need a condition for when pos is double-digit
            test_board[new_x][new_y] = pos
            if solve_kt(board, test_board, pos + 1, new_x, new_y):
                return True
            # Backtracking
            test_board[new_x][new_y] = -1
    return False

def main():
    global width, height, cell_size
    knight_past_positions = []
    board = {}
    pos = 2

    # Set up the board initially and get the starting position
    set_board_dimensions()
    test_board = [[-1 for i in range(width)] for i in range(height)]
    y, x = set_knight_position(knight_past_positions, initialising=True)
    # Do you want to try the puzzle? (y) Yes
    try:
        choice = str(input('Do you want to try the puzzle?'))
        # Yes if the user wants to try it
        if choice == 'y':
            # Check if the board has a solution
            if not solve_kt(board, test_board, pos, x, y):
                print('No solution exists!')
                exit()
        # No, the user wants the computer to display the solution
        elif choice == 'n':
            test_board[x - 1][y - 1] = 1
            if not solve_kt(board, test_board, pos, x - 1, y - 1):
                print('No solution exists!')
                exit()
            else:
                board = initialise_board(board)
                for i in range(1, height + 1):
                    for j in range(0, width):
                        adj = len(str(test_board[height - i][j]))
                        if adj == 1:
                            board[(height + 1) - i][j] = (" " * (cell_size - 1)) + str(test_board[height - i][j])
                        elif adj == 2:
                            board[(height + 1) - i][j] = (" " * (cell_size - 2)) + str(test_board[height - i][j])
                        elif adj == 3:
                            board[(height + 1) - i][j] = (" " * (cell_size - 3)) + str(test_board[height - i][j])
                print("Here's the solution!")
                print_board(board)
                exit()
        else:
            print("Invalid choice! Please enter 'y' or 'n'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    knight_position = (y, x)

    # Main loop of the functionality
    while True:
        board = initialise_board(board)
        board[x][y - 1] = (" " * (cell_size - 1)) + "X"
        check_moves(board, knight_position, knight_past_positions)
        set_past_positions(knight_past_positions, board)
        print_board(board)
        knight_past_positions.append(knight_position)
        if check_win_loss(knight_past_positions, knight_position):
            exit()
        y, x = set_knight_position(knight_past_positions)
        knight_position = (y, x)


#
# Repeat until there are no moves
# If the player has won tell them. If they have lost print the number of moves they tried.


if __name__ == "__main__":
    main()