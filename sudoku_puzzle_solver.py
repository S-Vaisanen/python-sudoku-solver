"""Sudoku solver.

Solves Sudoku puzzles using logical elimination and DFS algorithm.

Created by Simo Väisänen. Requires Python 3.0 or a later version. GUI
implemented using Tkinter.
"""

import tkinter as tk
import time
from copy import deepcopy
guess_counter = 0  # This variable keeps track of the amounts of guesses.

# matrix represents the squares of the Sudoku puzzle. Each list corresponds to
# a row of numbers of the Sudoku puzzle. matrix[0] corresponds to the top row
# of numbers. matrix[8] corresponds to the bottom row of numbers.

matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def replace_matrix_zeros(list_1):
    """Replaces zeros in a row with a list containing numbers 1-9.

    A row of numbers is represented by a list in matrix. Matrix[0] represents
    the top row and matrix[8] the bottom.

    A zero value in a list in matrix (the 9 lists in matrix represent the 9
    rows of the Sudoku puzzle) implies that the user has not specified a value
    for a square of the puzzle. This function replaces each zero integer value
    in a list in matrix with a list of numbers from 1-9 (i.e. this inserts
    lists inside the 9 lists of matrix where applicable). This is used to
    initialize matrix with each square where the user has not specified a
    digit with a list containing digits 1-9 as the set of potential solutions.
    This is used in conjunction with init_matrix(). These lists containing
    numbers 1-9 form the basis for the logical elimination process and the
    guessing and backtracking part of the DFS algorithm where applicable.
    """
    for i in range(9):
        if list_1[i] == 0:
            list_1[i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def init_matrix():
    """Initializes matrix.

    This is used in conjunction with replace_matrix_zeros() to replace all
    zero-values in the 9 lists of matrix.

    Each list in matrix corresponds to a row of numbers of the Sudoku Puzzle.
    matrix[0] represents the top row; matrix[8] represents the bottom row.
    This function iterates through the lists in matrix calling
    replace_matrix_zeros() in order to replace any zero value with a list
    containing numbers 1-9.
    """
    for list1 in matrix:
        replace_matrix_zeros(list1)


def horizontal(x, y):
    """Eliminates duplicate digits horizontally.

    This function removes duplicate digits which occur horizontally in
    relation to a square of the Sudoku puzzle. A square refers here to one of
    the 81 squares of the Sudoku puzzle. The 9 rows of the Sudoku puzzle are
    represented by 9 lists inside matrix. A square is represented by either
    an integer or a list inside one of the 9 lists of matrix. If the set of
    potential solutions of a square contains a single digit, then this digit
    will be removed from the sets of potential solutions of squares which
    occur in the same row as the square in question.

    The function examines an item in a list inside matrix using x and y
    coordinates, i.e. it determines whether matrix[y][x] contains an integer
    or a list. If it does contain an integer, it will then iterate through the
    data representing the same row (i.e. it will iterate through the same list
    in matrix) and remove this integer from any lists (if found) inside this
    list of matrix.

    Args:
        x: int, legitimate values: 0-8, represents the horizontal
        coordinate of matrix (matrix[y][x]).
        y: int, legitimate values: 0-8, represents the vertical
        coordinate of matrix (matrix[y][x]).

    Returns:
        counter: int

        A return value of zero implies that nothing has been removed, which
        may have implications for the backtracking logic of the algorithm.
        Any higher value signifies that lists were shortened, the implication
        being that the puzzle has not been solved yet or that the algo has
        not hit a 'dead end'.
    """
    counter = 0
    if isinstance(matrix[y][x], int):
        remove = matrix[y][x]
        for x2 in range(9):
            if (isinstance(matrix[y][x2], list) and
                    remove in matrix[y][x2]):
                matrix[y][x2].remove(remove)
                counter += 1
                if len(matrix[y][x2]) == 1:
                    matrix[y][x2] = matrix[y][x2][0]
                    # Performance time tends to be improved
                    # when returning counter here.
                    return counter
    return counter


def implement_horizontal():
    """Iterates through matrix calling horizontal().

    horizontal() removes duplicate digits from a horizontal point of view in
    relation to a given coordinate-pair x and y (i.e. in relation to a single
    square in the Sudoku puzzle). implement_horizontal() iterates
    systematically through every coordinate pair in matrix (i.e. it goes
    through every square in the Sudoku puzzle).

    Returns:
        counter: int

        A return value of zero implies that nothing has been removed, which
        may have implications for the backtracking logic of the algorithm.
        Any higher value signifies that lists were shortened, the implication
        being that the puzzle has not been solved yet or that the algo has
        not hit a 'dead end'.
    """
    counter = 0
    for y in range(9):
        for x in range(9):
            counter += horizontal(x, y)
    return counter


def vertical(x, y):
    """Eliminates duplicate digits vertically.

    This function removes duplicate digits which occur vertically in relation
    to a square of the Sudoku puzzle. A square refers here to one of the 81
    squares of the Sudoku puzzle. The 9 rows of the Sudoku puzzle are
    represented by 9 lists in matrix. A square is represented by either an
    integer or a list in one of the 9 lists of matrix. The data for a column
    is obtained by accessing the 9 lists of matrix at at a given index value
    (0 to 8). If the set of potential solutions of a square contains a single
    digit, then this digit will be removed from the sets of potential
    solutions of squares which occur in the same column as the square in
    question.

    The function examines an item in a list inside matrix using x and y
    coordinates, i.e. it determines whether matrix[y][x] contains an integer
    or a list. If it does contain an integer, it will then iterate through the
    data representing the same column (i.e. it will iterate through the 9
    lists of matrix at a given index value) and remove this integer from any
    lists (if found) inside these lists of matrix.

    Args:
        x: int, legitimate values: 0-8, represents the horizontal
        coordinate of matrix (matrix[y][x]).
        y: int, legitimate values: 0-8, represents the vertical
        coordinate of matrix (matrix[y][x]).

    Returns:
        counter: int

        A return value of zero implies that nothing has been removed, which
        may have implications for the backtracking logic of the algorithm.
        Any higher value signifies that lists were shortened, the implication
        being that the puzzle has not been solved yet or that the algo has
        not hit a 'dead end'.
    """
    counter = 0
    if isinstance(matrix[y][x], int):
        remove = matrix[y][x]
        for y2 in range(9):
            if (isinstance(matrix[y2][x], list) and
                    remove in matrix[y2][x]):
                matrix[y2][x].remove(remove)
                counter += 1
                if len(matrix[y2][x]) == 1:
                    matrix[y2][x] = matrix[y2][x][0]
                    # Performance time tends to be improved when returning
                    # counter here.
                    return counter
    return counter


def implement_vertical():
    """Iterates through matrix calling vertical().

    vertical() removes duplicate values from a vertical point of view in
    relation to a given coordinate-pair x and y (i.e. in relation to a single
    square in the Sudoku puzzle).

    implement_vertical() iterates systematically through every coordinate pair
    in matrix (i.e. it goes through every square in the Sudoku puzzle).

    Returns:
        counter: int

        A return value of zero implies that nothing has been removed, which
        may have implications for the backtracking logic of the algorithm.
        Any higher value signifies that lists were shortened, the implication
        being that the puzzle has not been solved yet or that the algo has
        not hit a 'dead end'.
    """
    counter = 0
    for x in range(9):
        for y in range(9):
            counter += vertical(x, y)
    return counter


# Below nine_sector_coordinate_tuples ends up being a list of 9 lists
# containing coordinate pair tuples. Each list inside
# nine_sector_coordinate_tuples represents one of 9 "sectors" of the Sudoku
# puzzle. A sector refers here to a 3 x 3 square area in which numbers 1-9,
# as per the rules of Sudoku, are allowed to occur only once. The tuple
# coordinate pairs inside each list refer to the individual squares inside a
# sector.


FIRST = [0, 1, 2]
SECOND = [3, 4, 5]
THIRD = [6, 7, 8]

ALL_COMBINATIONS = [FIRST, SECOND, THIRD]
nine_sectors_coordinate_tuples = []
single_sector_coordinate_tuples = []

for x_coordinates in ALL_COMBINATIONS:
    for y_coordinates in ALL_COMBINATIONS:
        for x_coordinate in x_coordinates:
            for y_coordinate in y_coordinates:
                single_sector_coordinate_tuples.append(
                    (x_coordinate, y_coordinate))
                if len(single_sector_coordinate_tuples) == 9:
                    nine_sectors_coordinate_tuples.append(
                        single_sector_coordinate_tuples)
                    single_sector_coordinate_tuples = []


def sectors():
    """ Eliminates duplicate digits sector wise.

    This function removes duplicate digits which occur sector wise in relation
    to a square of the Sudoku puzzle. A square refers here to one of the 81
    squares of the Sudoku puzzle. A sector refers here to the 9 regions of 3 x
    3 squares where, as per the rules of Sudoku, numbers 1-9 are allowed to
    occur only once. This function removes duplicate digits in all sectors.

    The 9 rows of the Sudoku puzzle are represented by 9 lists of matrix. A
    square is represented by either an integer or a list in one of the 9 lists
    of matrix. If the set of potential solutions of a square contains a single
    digit, then this digit will be removed from the sets of potential solutions
    of squares which occur in the same sector as the square in question.

    The function examines an item in a list inside matrix using x and y
    coordinates, (nine_sector_coordinate_tuples contains lists of tuples which
    correspond to the 9 sectors of the Sudoku puzzle), i.e. it determines
    whether matrix[y][x] contains an integer or a list. If it does contain an
    integer, it will then iterate through the data representing the same sector
    (i.e. it will iterate through the 9 lists of matrix using coordinate tuples
    contained in nine_sector_coordinate_tuples) and remove this integer from
    any lists (if found) inside these lists of matrix.

    Returns:
        counter: int

        A return value of zero implies that nothing has been removed, which
        may have implications for the backtracking logic of the algorithm.
        Any higher value signifies that lists were shortened, the implication
        being that the puzzle has not been solved yet or that the algo has
        not hit a 'dead end'.
    """
    counter = 0
    for sector in nine_sectors_coordinate_tuples:
        for coordinate_pair in sector:
            x, y = coordinate_pair
            if isinstance((matrix[y][x]), int):
                # The int stored in remove will potentially
                # be removed from matrix corresponding to that
                # sector.
                remove = matrix[y][x]
                for coordinate_pair2 in sector:
                    x2, y2 = coordinate_pair2
                    if (isinstance(matrix[y2][x2], list)
                            and remove in matrix[y2][x2]):
                        matrix[y2][x2].remove(remove)
                        counter += 1
                        if len(matrix[y2][x2]) == 1:
                            matrix[y2][x2] = matrix[y2][x2][0]
                            # affects performance time
                            return counter
    return counter


def count_hor():
    """Checks whether matrix has been solved horizontally.

    Returns True if matrix has been solved horizontally. Otherwise returns
    False.
    """
    for y in range(9):
        res = 0
        for x in range(9):
            if isinstance(matrix[y][x], int):
                res += matrix[y][x]
            else:
                return False
        if res != 45:
            return False
    return True


def count_ver():
    """Checks whether matrix has been solved vertically.

    Returns True if matrix has been solved vertically. Otherwise returns
    False.
    """
    for x in range(9):
        res = 0
        for y in range(9):
            if isinstance(matrix[y][x], int):
                res += matrix[y][x]
            else:
                # return 'list'
                return False
        if res != 45:
            return False
    return True


def count_sec():
    """Checks whether matrix has been solved sector wise.

    Returns True if matrix has been solved sector wise. Otherwise returns
    False.
    """
    for co_pair_list in nine_sectors_coordinate_tuples:
        result = 0
        for co_tuple in co_pair_list:
            y, x = co_tuple
            if isinstance(matrix[y][x], int):
                result += matrix[y][x]
        if result != 45:
            return False
    return True


# Below a Depth First Search algorithm using stack (FIFO – first in first out)
# is implemented. The stack is implemented using previous_matrixes (list). If
# the script cannot resolve the puzzle using logical elimination any further
# (i.e. functions implement_horizontal(), implement_vertical() and sectors()
# all return zero), then the Depth First Search algorithm takes over (i.e. the
# algorithm chooses one of the values in a list inside the 9 lists of matrix
# and replaces the list by that int - basically the algo 'guesses'). If the
# algorithm is capable of traversing in the depthward direction (ie within the
# 9 lists representing Sudoku rows in matrix, there are lists instead of
# exclusively int values), then a further step in depthward direction is taken
# and recorded (new matrix is pushed into previous_matrixes). In the
# alternative, the algorithm has to backtrack (matrix is popped from
# previous_matrixes). Information about the search is recorded in
# guess_container. After a step in depthward direction is taken, the algorithm
# returns to logical elimination (ie it calls implement_horizontal(),
# implement_vertical() and sectors()).

# previous_matrixes is simply a list containing matrix lists from previous
# vertexes.

# guess_container has the following structure:

# [[(x,y), int, int]]

# In other words, guess_container is a list of lists. Information about each
# new step in depthward direction is appended to it. Inside each list, the
# first item is a tuple representing the coordinates in relation to a list
# within matrix regarding to which a guess was made (ie in relation to which
# depthward traversal took / takes place).

# The second item (int) records the index position of the depthward step in
# relation to the list within matrix. The other int records the length of the
# list within matrix. When the algorithm takes a step in depthwise direction,
# a list in the relevant coordinate is replaced by the applicable int value.

# The algorithm backtracks if the logical elimination process cannot be
# continued, and there are no lists left within the 9 lists of matrix (i.e.
# the 9 lists of matrix corresponding to Sudoku rows only contain integers),
# yet the puzzle has not been solved correctly. After backtracking, it will
# take the following index within the list containing the previous vertex as a
# new guess, provided the list has not been searched through already (ie
# maximum index has not been reached already - and hence the length of the list
# is recorded). Any list that has been searched through already is popped out
# of both previous_matrixes and guess_container. Thus previous_matrixes and 
# guess_container recording the traversal of DFT always remain synchronized.


def list_counter_func():
    """Counts the amount of lists within the 9 lists (rows) of matrix.

    Each row of numbers in the Sudoku puzzle is represented by a list in
    matrix; ie matrix[0] to matrix[8] represent the rows of the Sudoku puzzle
    from the top to bottom. These rows in turn have 9 places for values as per
    the rules of Sudoku. The lists (matrix[0] to matrix[8]) representing the
    rows can contain int values and / or lists. The existence of an int value
    implies that a solution for that square has been found (or that the square
    was initialized by the user with that value). However, if there is a list,
    further work is required by the algorithm. This function counts the number
    of lists (ie squares which have not been solved) and returns the amount of
    such lists.
    """
    counter = 0
    for row in matrix:
        for item in row:
            if isinstance(item, list):
                counter += 1
    return counter


# initialize guess_container list, which keeps track of DFS
guess_container = []

# When the DFT algorith takes a depthward step, matrix is appended to
# previous_matrixes, so that backtracking is possible.

previous_matrixes = []


def guess(mode):
    """Takes a step in depthward direction.

    This function is called when logical elimination cannot be pursued
    further. This function implements a step in the DFS algorithm in depthward
    direction. If the function argument "mode" equals to "new", the shortest
    list in matrix is identified, and a DFS search is pursued in relation to
    that list. However, if the argument equals to "backtrack", it follows that
    backtracking has occurred prior to calling this function, and therefore,
    the next item in the list relating to the previous vertex point will be
    chosen as the DFS algo depthward step. This function will only be called
    with mode being 'backtrack' when backtrack() has been called prior, which
    ensures that there are always more items in the list in question.

    Args:
        mode: str
    """
    global guess_counter
    guess_counter += 1

    if mode == 'new':
        # Here, coordinate_pair will point to the shortest list in matrix.
        coordinate_pair = find_shortest_list()
        if isinstance(coordinate_pair, tuple):
            x, y = coordinate_pair
            list_length = len(matrix[y][x])
            guess_index = 0
            # A new guess is always at index zero,
            # hence guess_index is at zero.
            guess_container.append([coordinate_pair, guess_index, list_length])
        else:
            return

    # In 'backtrack' mode, the previous item in guess_container is examined
    # to implement a step in depthward direction, i.e. the next item in the
    # list will be picked. Previous entry in guess_container will be replaced
    # by information about the new step.
    elif mode == 'backtrack':
        # coordinate pair is obtained from previous vertex
        coordinate_pair = guess_container[-1][0]
        x, y = coordinate_pair
        previous_guess_index = guess_container[-1][1]
        guess_index = previous_guess_index + 1
        # Now the guess is going to relate to the next item in the list
        # which has not been previously searched.
        list_length = len(matrix[y][x])
        # Remove previous item in guess container; add new.
        # guess_container keeps track of the DFS.
        guess_container.pop(-1)
        guess_container.append([coordinate_pair, guess_index, list_length])

    # In order to preserve the unique state of matrix vs the previous vertex
    # points, it is necessary to use deepcopy(). Thus each list in matrix and
    # each item within the lists in matrix (representing the squares of the
    # Sudoku puzzle) and the previous vertex points of it stored in
    # previous_matrixes point to unique memory addresses.

    deep_copy = deepcopy(matrix)
    if mode == 'new':
        previous_matrixes.append(deep_copy)
    new_guess_value = matrix[y][x][guess_index]
    # a list in matrix[y][x] is replaced by int, and hence a step depthwards
    # in the DFS is taken.
    matrix[y][x] = new_guess_value


def backtrack():
    """Pops the last item in previous_matrixes and guess_container.

    This function is called when logical elimination cannot be carried
    further, and the 9 lists in matrix (representing the rows of the Sudoku
    puzzle) do not contain any lists (and therefore contain only integers);
    yet the solution has not been found, and therefore backtracking is
    necessary.

    This function pops the last item in guess_container and previous_matrixes
    provided that the list representing a square in Sudoku puzzle has been
    fully searched. The popping is performed inside a loop until a list is
    found where the last item within the list (representing a square in the
    Sudoku puzzle) has not been searched.
    """
    global matrix
    # global keyword is necessary as matrix list potentially redeclared,
    # i.e not merely updated.
    loop = True
    while loop:
        if guess_container[-1][1] + 1 == guess_container[-1][2]:
            # if the highest index of the list is already reached,
            # remove previous_matrixes[-1] and guess_container[-1]
            previous_matrixes.pop(-1)
            guess_container.pop(-1)
        elif guess_container[-1][1] + 1 != guess_container[-1][2]:
            # in the alternative, continue from the logical point
            # (i.e. next item in the list) in the previous vertex.
            deep_copy2 = deepcopy(previous_matrixes[-1])
            matrix = deep_copy2
            loop = False


def find_shortest_list():
    """Finds the shortest list within 9 lists of matrix.

    Matrix consists of 9 lists (corresponding to Sudoku rows; index values 0
    to 8), and inside these lists there are 9 items (index values 0 to 8),
    which correspond to Sudoku columns. These items can either be of type list
    or int. If there are lists left within the 9 matrix lists, this function
    will find either the shortest list or one of the shortest lists and return
    a coordinate pair tuple corresponding to it. Finding the shortest list is
    necessary to keep the algorithm effective if and when the algo executes
    Depth First Search.

    Returns:
        tuple: xy_tuple
    """
    shortest = 9
    xy_tuple = (100, 100)
    for y in range(9):
        for x in range(9):
            if isinstance(matrix[y][x], list):
                if len(matrix[y][x]) < shortest:
                    shortest = len(matrix[y][x])
                    xy_tuple = (x, y)
                    if shortest == 1:
                        pass
    if xy_tuple != (100, 100):
        return xy_tuple
    return None


def solve():
    """Main control part of the DFS algorithm."""
    global guess_counter
    start_time = time.time()
    global matrix
    init_matrix()  # initializes matrix
    loop = True
    # Main control part of DFS below.
    while loop:
        if guess_counter > 100000:
            # This ensures that the script does not end up being stuck in an
            # infinite loop when there is no solution to the puzzle.
            guess_counter = 0
            loop = False
            # An error message gets displayed.
            max_guess_mgs()

        # Removes integers from lists inside lists of matrix using a logical
        # elimination process. The amount of integers removed from lists
        # within the 9 lists of matrix are stored respectively in a, b and c.
        a = sectors()
        b = implement_vertical()
        c = implement_horizontal()

        if a + b + c == 0:
            # if so, logical elimination cannot be continued.
            if list_counter_func() == 0:
                # The lists within matrix (representing rows of the Sudoku
                # puzzle) contain no lists, i.e. there are only integers, and
                # so, either the puzzle has been solved correctly, but if not,
                # backtracking will be implemented.
                if count_hor() and count_ver() and count_sec():
                    end_time = time.time()
                    perf_duration = end_time - start_time
                    print('Performance duration: ', perf_duration, 'sec.')
                    guess_counter = 0
                    loop = False
                    msg = message()
                    solved_msg(msg)
                else:
                    backtrack()
                    # this leads to backtracking
                    guess('backtrack')

            else:
                # In the alternative, there are lists within the 9 lists of
                # matrix, and a depthward step will be taken.
                guess('new')
                # Traverses depthward.


# BELOW IS TKINTER PART

window = tk.Tk()
window.title("SUDOKU SOLVER")
window.grid_columnconfigure(3, minsize=30)
window.grid_columnconfigure(7, minsize=30)
window.grid_rowconfigure(3, minsize=30)
window.grid_rowconfigure(7, minsize=30)
window.grid_rowconfigure(11, minsize=30)


# row zero

VALUES = ('-', 1, 2, 3, 4, 5, 6, 7, 8, 9)

spin_r0_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_0.grid(column=0, row=0, padx=10, pady=10)

spin_r0_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_1.grid(column=1, row=0, padx=10, pady=10)

spin_r0_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_2.grid(column=2, row=0, padx=10, pady=10)

spin_r0_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_3.grid(column=4, row=0, padx=10, pady=10)

spin_r0_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_4.grid(column=5, row=0, padx=10, pady=10)

spin_r0_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_5.grid(column=6, row=0, padx=10, pady=10)

spin_r0_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_6.grid(column=8, row=0, padx=10, pady=10)

spin_r0_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_7.grid(column=9, row=0, padx=10, pady=10)

spin_r0_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r0_8.grid(column=10, row=0, padx=10, pady=10)

# row one

spin_r1_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_0.grid(column=0, row=1, padx=10, pady=10)

spin_r1_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_1.grid(column=1, row=1, padx=10, pady=10)

spin_r1_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_2.grid(column=2, row=1, padx=10, pady=10)

spin_r1_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_3.grid(column=4, row=1)

spin_r1_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_4.grid(column=5, row=1, padx=10, pady=10)

spin_r1_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_5.grid(column=6, row=1, padx=10, pady=10)

spin_r1_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_6.grid(column=8, row=1, padx=10, pady=10)

spin_r1_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_7.grid(column=9, row=1, padx=10, pady=10)

spin_r1_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r1_8.grid(column=10, row=1, padx=10, pady=10)

# row two

spin_r2_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_0.grid(column=0, row=2, padx=10, pady=10)

spin_r2_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_1.grid(column=1, row=2, padx=10, pady=10)

spin_r2_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_2.grid(column=2, row=2, padx=10, pady=10)

spin_r2_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_3.grid(column=4, row=2, padx=10, pady=10)

spin_r2_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_4.grid(column=5, row=2, padx=10, pady=10)

spin_r2_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_5.grid(column=6, row=2, padx=10, pady=10)

spin_r2_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_6.grid(column=8, row=2, padx=10, pady=10)

spin_r2_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_7.grid(column=9, row=2, padx=10, pady=10)

spin_r2_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r2_8.grid(column=10, row=2, padx=10, pady=10)

# row three

spin_r3_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_0.grid(column=0, row=4, padx=10, pady=10)

spin_r3_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_1.grid(column=1, row=4, padx=10, pady=10)

spin_r3_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_2.grid(column=2, row=4, padx=10, pady=10)

spin_r3_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_3.grid(column=4, row=4, padx=10, pady=10)

spin_r3_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_4.grid(column=5, row=4, padx=10, pady=10)

spin_r3_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_5.grid(column=6, row=4, padx=10, pady=10)

spin_r3_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_6.grid(column=8, row=4, padx=10, pady=10)

spin_r3_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_7.grid(column=9, row=4, padx=10, pady=10)

spin_r3_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r3_8.grid(column=10, row=4, padx=10, pady=10)

# row four

spin_r4_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_0.grid(column=0, row=5, padx=10, pady=10)

spin_r4_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_1.grid(column=1, row=5, padx=10, pady=10)

spin_r4_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_2.grid(column=2, row=5, padx=10, pady=10)

spin_r4_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_3.grid(column=4, row=5, padx=10, pady=10)

spin_r4_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_4.grid(column=5, row=5, padx=10, pady=10)

spin_r4_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_5.grid(column=6, row=5, padx=10, pady=10)

spin_r4_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_6.grid(column=8, row=5, padx=10, pady=10)

spin_r4_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_7.grid(column=9, row=5, padx=10, pady=10)

spin_r4_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r4_8.grid(column=10, row=5, padx=10, pady=10)

# row five

spin_r5_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_0.grid(column=0, row=6, padx=10, pady=10)

spin_r5_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_1.grid(column=1, row=6, padx=10, pady=10)

spin_r5_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_2.grid(column=2, row=6, padx=10, pady=10)

spin_r5_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_3.grid(column=4, row=6, padx=10, pady=10)

spin_r5_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_4.grid(column=5, row=6, padx=10, pady=10)

spin_r5_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_5.grid(column=6, row=6, padx=10, pady=10)

spin_r5_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_6.grid(column=8, row=6, padx=10, pady=10)

spin_r5_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_7.grid(column=9, row=6, padx=10, pady=10)

spin_r5_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r5_8.grid(column=10, row=6, padx=10, pady=10)

# row six

spin_r6_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_0.grid(column=0, row=8, padx=10, pady=10)

spin_r6_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_1.grid(column=1, row=8, padx=10, pady=10)

spin_r6_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_2.grid(column=2, row=8, padx=10, pady=10)

spin_r6_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_3.grid(column=4, row=8, padx=10, pady=10)

spin_r6_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_4.grid(column=5, row=8, padx=10, pady=10)

spin_r6_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_5.grid(column=6, row=8, padx=10, pady=10)

spin_r6_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_6.grid(column=8, row=8, padx=10, pady=10)

spin_r6_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_7.grid(column=9, row=8, padx=10, pady=10)

spin_r6_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r6_8.grid(column=10, row=8, padx=10, pady=10)

# row seven

spin_r7_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_0.grid(column=0, row=9, padx=10, pady=10)

spin_r7_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_1.grid(column=1, row=9, padx=10, pady=10)

spin_r7_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_2.grid(column=2, row=9, padx=10, pady=10)

spin_r7_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_3.grid(column=4, row=9, padx=10, pady=10)

spin_r7_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_4.grid(column=5, row=9, padx=10, pady=10)

spin_r7_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_5.grid(column=6, row=9, padx=10, pady=10)

spin_r7_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_6.grid(column=8, row=9, padx=10, pady=10)

spin_r7_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_7.grid(column=9, row=9, padx=10, pady=10)

spin_r7_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r7_8.grid(column=10, row=9, padx=10, pady=10)

# row eight

spin_r8_0 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_0.grid(column=0, row=10, padx=10, pady=10)

spin_r8_1 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_1.grid(column=1, row=10, padx=10, pady=10)

spin_r8_2 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_2.grid(column=2, row=10, padx=10, pady=10)

spin_r8_3 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_3.grid(column=4, row=10, padx=10, pady=10)

spin_r8_4 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_4.grid(column=5, row=10, padx=10, pady=10)

spin_r8_5 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_5.grid(column=6, row=10, padx=10, pady=10)

spin_r8_6 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_6.grid(column=8, row=10, padx=10, pady=10)

spin_r8_7 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_7.grid(column=9, row=10, padx=10, pady=10)

spin_r8_8 = tk.Spinbox(window, values=VALUES, width=3)

spin_r8_8.grid(column=10, row=10, padx=10, pady=10)


def message():
    """Returns a string containing the solved puzzle."""
    msg = ""
    for y in range(9):
        if y == 3:
            msg += '\n'
        if y == 6:
            msg += '\n'
        for x in range(9):
            msg += str(matrix[y][x])
            if x == 2:
                msg += '  '
            if x == 5:
                msg += '  '
        msg += "\n"
    return msg


def solved_msg(msg):
    """Displays a solution to the puzzle.

    Args:
        msg: str
    """
    popup = tk.Tk()
    # popup.geometry('350x500')
    popup.wm_title("SUDOKU SOLVED!")
    label = tk.Label(popup, text=msg, font=("Helvetica", 20))
    label.pack(side="top", fill="x", padx=60, pady=50)
    label2 = tk.Label(popup, text="Created by Simo Väisänen.",
                      font=("Helvetica", 10))
    label2.pack(side="bottom", fill="x", padx=30, pady=30)
    B1 = tk.Button(popup, text="OK",
                   font=("Helvetica", 20), command=popup.destroy)
    B1.pack(padx=30, pady=30)
    popup.mainloop()


def max_guess_mgs():
    """Maximum reached.

    Displays a message that the algorithm has reached the maximum permitted
    amount of guesses and that no solution was found.
    """
    popup2 = tk.Tk()
    popup2.wm_title("Maximum reached")
    MAXIMUM_MESSAGE = """Maximum amount of guesses \nreached.
     There is probably\n no solution to the puzzle."""
    label = tk.Label(popup2, text=MAXIMUM_MESSAGE, font=("Helvetica", 10))
    label.pack(side="top", fill="x", padx=30, pady=30)
    B3 = tk.Button(popup2, text="OK",
                   font=("Helvetica", 10), command=popup2.destroy)
    B3.pack(padx=20, pady=20)
    popup2.mainloop()


def reset():
    """"Resets the squares into zeros."""
    # row zero
    spin_r0_0.delete(0, "end")
    spin_r0_0.insert(0, '-')
    spin_r0_1.delete(0, "end")
    spin_r0_1.insert(0, '-')
    spin_r0_2.delete(0, "end")
    spin_r0_2.insert(0, '-')
    spin_r0_3.delete(0, "end")
    spin_r0_3.insert(0, '-')
    spin_r0_4.delete(0, "end")
    spin_r0_4.insert(0, '-')
    spin_r0_5.delete(0, "end")
    spin_r0_5.insert(0, '-')
    spin_r0_6.delete(0, "end")
    spin_r0_6.insert(0, '-')
    spin_r0_7.delete(0, "end")
    spin_r0_7.insert(0, '-')
    spin_r0_8.delete(0, "end")
    spin_r0_8.insert(0, '-')
    # row one
    spin_r1_0.delete(0, "end")
    spin_r1_0.insert(0, '-')
    spin_r1_1.delete(0, "end")
    spin_r1_1.insert(0, '-')
    spin_r1_2.delete(0, "end")
    spin_r1_2.insert(0, '-')
    spin_r1_3.delete(0, "end")
    spin_r1_3.insert(0, '-')
    spin_r1_4.delete(0, "end")
    spin_r1_4.insert(0, '-')
    spin_r1_5.delete(0, "end")
    spin_r1_5.insert(0, '-')
    spin_r1_6.delete(0, "end")
    spin_r1_6.insert(0, '-')
    spin_r1_7.delete(0, "end")
    spin_r1_7.insert(0, '-')
    spin_r1_8.delete(0, "end")
    spin_r1_8.insert(0, '-')
    # row two
    spin_r2_0.delete(0, "end")
    spin_r2_0.insert(0, '-')
    spin_r2_1.delete(0, "end")
    spin_r2_1.insert(0, '-')
    spin_r2_2.delete(0, "end")
    spin_r2_2.insert(0, '-')
    spin_r2_3.delete(0, "end")
    spin_r2_3.insert(0, '-')
    spin_r2_4.delete(0, "end")
    spin_r2_4.insert(0, '-')
    spin_r2_5.delete(0, "end")
    spin_r2_5.insert(0, '-')
    spin_r2_6.delete(0, "end")
    spin_r2_6.insert(0, '-')
    spin_r2_7.delete(0, "end")
    spin_r2_7.insert(0, '-')
    spin_r2_8.delete(0, "end")
    spin_r2_8.insert(0, '-')
    # row three
    spin_r3_0.delete(0, "end")
    spin_r3_0.insert(0, '-')
    spin_r3_1.delete(0, "end")
    spin_r3_1.insert(0, '-')
    spin_r3_2.delete(0, "end")
    spin_r3_2.insert(0, '-')
    spin_r3_3.delete(0, "end")
    spin_r3_3.insert(0, '-')
    spin_r3_4.delete(0, "end")
    spin_r3_4.insert(0, '-')
    spin_r3_5.delete(0, "end")
    spin_r3_5.insert(0, '-')
    spin_r3_6.delete(0, "end")
    spin_r3_6.insert(0, '-')
    spin_r3_7.delete(0, "end")
    spin_r3_7.insert(0, '-')
    spin_r3_8.delete(0, "end")
    spin_r3_8.insert(0, '-')
    # row four
    spin_r4_0.delete(0, "end")
    spin_r4_0.insert(0, '-')
    spin_r4_1.delete(0, "end")
    spin_r4_1.insert(0, '-')
    spin_r4_2.delete(0, "end")
    spin_r4_2.insert(0, '-')
    spin_r4_3.delete(0, "end")
    spin_r4_3.insert(0, '-')
    spin_r4_4.delete(0, "end")
    spin_r4_4.insert(0, '-')
    spin_r4_5.delete(0, "end")
    spin_r4_5.insert(0, '-')
    spin_r4_6.delete(0, "end")
    spin_r4_6.insert(0, '-')
    spin_r4_7.delete(0, "end")
    spin_r4_7.insert(0, '-')
    spin_r4_8.delete(0, "end")
    spin_r4_8.insert(0, '-')
    # row five
    spin_r5_0.delete(0, "end")
    spin_r5_0.insert(0, '-')
    spin_r5_1.delete(0, "end")
    spin_r5_1.insert(0, '-')
    spin_r5_2.delete(0, "end")
    spin_r5_2.insert(0, '-')
    spin_r5_3.delete(0, "end")
    spin_r5_3.insert(0, '-')
    spin_r5_4.delete(0, "end")
    spin_r5_4.insert(0, '-')
    spin_r5_5.delete(0, "end")
    spin_r5_5.insert(0, '-')
    spin_r5_6.delete(0, "end")
    spin_r5_6.insert(0, '-')
    spin_r5_7.delete(0, "end")
    spin_r5_7.insert(0, '-')
    spin_r5_8.delete(0, "end")
    spin_r5_8.insert(0, '-')
    # row six
    spin_r6_0.delete(0, "end")
    spin_r6_0.insert(0, '-')
    spin_r6_1.delete(0, "end")
    spin_r6_1.insert(0, '-')
    spin_r6_2.delete(0, "end")
    spin_r6_2.insert(0, '-')
    spin_r6_3.delete(0, "end")
    spin_r6_3.insert(0, '-')
    spin_r6_4.delete(0, "end")
    spin_r6_4.insert(0, '-')
    spin_r6_5.delete(0, "end")
    spin_r6_5.insert(0, '-')
    spin_r6_6.delete(0, "end")
    spin_r6_6.insert(0, '-')
    spin_r6_7.delete(0, "end")
    spin_r6_7.insert(0, '-')
    spin_r6_8.delete(0, "end")
    spin_r6_8.insert(0, '-')
    # row seven
    spin_r7_0.delete(0, "end")
    spin_r7_0.insert(0, '-')
    spin_r7_1.delete(0, "end")
    spin_r7_1.insert(0, '-')
    spin_r7_2.delete(0, "end")
    spin_r7_2.insert(0, '-')
    spin_r7_3.delete(0, "end")
    spin_r7_3.insert(0, '-')
    spin_r7_4.delete(0, "end")
    spin_r7_4.insert(0, '-')
    spin_r7_5.delete(0, "end")
    spin_r7_5.insert(0, '-')
    spin_r7_6.delete(0, "end")
    spin_r7_6.insert(0, '-')
    spin_r7_7.delete(0, "end")
    spin_r7_7.insert(0, '-')
    spin_r7_8.delete(0, "end")
    spin_r7_8.insert(0, '-')
    # row eight
    spin_r8_0.delete(0, "end")
    spin_r8_0.insert(0, '-')
    spin_r8_1.delete(0, "end")
    spin_r8_1.insert(0, '-')
    spin_r8_2.delete(0, "end")
    spin_r8_2.insert(0, '-')
    spin_r8_3.delete(0, "end")
    spin_r8_3.insert(0, '-')
    spin_r8_4.delete(0, "end")
    spin_r8_4.insert(0, '-')
    spin_r8_5.delete(0, "end")
    spin_r8_5.insert(0, '-')
    spin_r8_6.delete(0, "end")
    spin_r8_6.insert(0, '-')
    spin_r8_7.delete(0, "end")
    spin_r8_7.insert(0, '-')
    spin_r8_8.delete(0, "end")
    spin_r8_8.insert(0, '-')


def update_values():
    """Transfers values from the widget into matrix."""
    # row zero
    matrix[0][0] = spin_r0_0.get()
    matrix[0][1] = spin_r0_1.get()
    matrix[0][2] = spin_r0_2.get()
    matrix[0][3] = spin_r0_3.get()
    matrix[0][4] = spin_r0_4.get()
    matrix[0][5] = spin_r0_5.get()
    matrix[0][6] = spin_r0_6.get()
    matrix[0][7] = spin_r0_7.get()
    matrix[0][8] = spin_r0_8.get()

    # row one
    matrix[1][0] = spin_r1_0.get()
    matrix[1][1] = spin_r1_1.get()
    matrix[1][2] = spin_r1_2.get()
    matrix[1][3] = spin_r1_3.get()
    matrix[1][4] = spin_r1_4.get()
    matrix[1][5] = spin_r1_5.get()
    matrix[1][6] = spin_r1_6.get()
    matrix[1][7] = spin_r1_7.get()
    matrix[1][8] = spin_r1_8.get()

    # row two
    matrix[2][0] = spin_r2_0.get()
    matrix[2][1] = spin_r2_1.get()
    matrix[2][2] = spin_r2_2.get()
    matrix[2][3] = spin_r2_3.get()
    matrix[2][4] = spin_r2_4.get()
    matrix[2][5] = spin_r2_5.get()
    matrix[2][6] = spin_r2_6.get()
    matrix[2][7] = spin_r2_7.get()
    matrix[2][8] = spin_r2_8.get()

    # row three
    matrix[3][0] = spin_r3_0.get()
    matrix[3][1] = spin_r3_1.get()
    matrix[3][2] = spin_r3_2.get()
    matrix[3][3] = spin_r3_3.get()
    matrix[3][4] = spin_r3_4.get()
    matrix[3][5] = spin_r3_5.get()
    matrix[3][6] = spin_r3_6.get()
    matrix[3][7] = spin_r3_7.get()
    matrix[3][8] = spin_r3_8.get()

    # row four
    matrix[4][0] = spin_r4_0.get()
    matrix[4][1] = spin_r4_1.get()
    matrix[4][2] = spin_r4_2.get()
    matrix[4][3] = spin_r4_3.get()
    matrix[4][4] = spin_r4_4.get()
    matrix[4][5] = spin_r4_5.get()
    matrix[4][6] = spin_r4_6.get()
    matrix[4][7] = spin_r4_7.get()
    matrix[4][8] = spin_r4_8.get()

    # row five
    matrix[5][0] = spin_r5_0.get()
    matrix[5][1] = spin_r5_1.get()
    matrix[5][2] = spin_r5_2.get()
    matrix[5][3] = spin_r5_3.get()
    matrix[5][4] = spin_r5_4.get()
    matrix[5][5] = spin_r5_5.get()
    matrix[5][6] = spin_r5_6.get()
    matrix[5][7] = spin_r5_7.get()
    matrix[5][8] = spin_r5_8.get()

    # row six
    matrix[6][0] = spin_r6_0.get()
    matrix[6][1] = spin_r6_1.get()
    matrix[6][2] = spin_r6_2.get()
    matrix[6][3] = spin_r6_3.get()
    matrix[6][4] = spin_r6_4.get()
    matrix[6][5] = spin_r6_5.get()
    matrix[6][6] = spin_r6_6.get()
    matrix[6][7] = spin_r6_7.get()
    matrix[6][8] = spin_r6_8.get()

    # row seven
    matrix[7][0] = spin_r7_0.get()
    matrix[7][1] = spin_r7_1.get()
    matrix[7][2] = spin_r7_2.get()
    matrix[7][3] = spin_r7_3.get()
    matrix[7][4] = spin_r7_4.get()
    matrix[7][5] = spin_r7_5.get()
    matrix[7][6] = spin_r7_6.get()
    matrix[7][7] = spin_r7_7.get()
    matrix[7][8] = spin_r7_8.get()

    # row eight
    matrix[8][0] = spin_r8_0.get()
    matrix[8][1] = spin_r8_1.get()
    matrix[8][2] = spin_r8_2.get()
    matrix[8][3] = spin_r8_3.get()
    matrix[8][4] = spin_r8_4.get()
    matrix[8][5] = spin_r8_5.get()
    matrix[8][6] = spin_r8_6.get()
    matrix[8][7] = spin_r8_7.get()
    matrix[8][8] = spin_r8_8.get()
    legitimate_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for y in range(9):
        for x in range(9):
            if matrix[y][x] not in legitimate_values:
                matrix[y][x] = 0
            else:
                matrix[y][x] = int(matrix[y][x])

    zero_counter = 0

    # If matrix is full of zeros or empty, it will be initialized with 1 in
    # the top left corner.
    for list1 in matrix:
        for number in list1:
            if number == 0:
                zero_counter += 1
    if zero_counter == 81:
        matrix[0][0] = 1

    global guess_counter
    guess_counter = 0
    solve()


B = tk.Button(window, text="Solve", command=update_values)
B.grid(column=4, row=12, padx=10, pady=10)
B2 = tk.Button(window, text="Reset", command=reset)
B2.grid(column=6, row=12, padx=10, pady=10)
window.mainloop()
