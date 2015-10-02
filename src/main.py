import time
from cp.cp import CP
from cp.variable import Variable
from cp.constraints.all_different_constraint import AllDifferentConstraint


def read_sudoku():
    with open("1000 sudokus.txt") as file:
        sudokus = []
        for sudoku in file:
            sudokus.append(sudoku.rstrip().split(","))
    return sudokus


def make_variables(sudoku):
    variable_array = []
    var_num = 1
    for cell in sudoku[0]:
        if cell == ".":
            variable_array.append(Variable("var%d" % var_num, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
        else:
            variable_array.append(Variable("var%d" % var_num, [int(cell)]))
        var_num += 1
    return variable_array


def create_sudoku_constraints(variables):
    constaints_array = []
    constraint_num = 1
    # get all the variables per row
    for i in range(0, 82, 9):
        constaints_array.append(AllDifferentConstraint("name%d" % constraint_num, variables[i:i + 9]))
        constraint_num += 1
        if i + 9 >= 81:
            break
    # get all the variables per column
    for colom in range(0, 9):
        colom_vars = []
        for cell in range(colom, 81, 9):
            colom_vars.append(variables[cell])
        constaints_array.append(AllDifferentConstraint("name%d" % constraint_num, colom_vars))
        constraint_num += 1
    # quit a complected loop to get the indexes of every block
    # maybe we van split up this code or rewrite it, for now it works 
    # get all the variables per block
    row_start = 0
    row_end = 26
    for row_block in range(0, 3):
        column_start = 0
        column_end = 2
        for column_block in range(0, 3):
            block_vars = []
            for i in range(0, 82):
                if (column_start <= i % 9 <= column_end) and (row_start <= i <= row_end):
                    block_vars.append(variables[i])
            constaints_array.append(AllDifferentConstraint("name%d" % constraint_num, block_vars))
            constraint_num += 1
            column_start += 3
            column_end += 3
        row_start += 27
        row_end += 27
    return constaints_array


sudokus = read_sudoku()

root_start = time.time()
sudokus_to_solve = 1000
total_splits = 0
total_backtracks = 0
for j in range(sudokus_to_solve):
    variables = make_variables(sudokus[j])
    constraints = create_sudoku_constraints(variables)

    cp = CP()
    cp.variables = variables
    cp.constraints = constraints
    assignment = cp.search()

    i = 1
    for variable in cp.variables:
        print assignment.get_value(variable),
        if i % 9 == 0:
            print ""
        i += 1

    print "sudoku", j
    print "runtime:", cp.runtime, "seconds."
    print "splits:", cp.splits
    print "backtracks:", cp.backtracks
    print "arc generate time:", cp.arc_generate_time
    print "remove inconsistency time:", cp.remove_inconsistency_time
    total_splits += cp.splits
    total_backtracks += cp.backtracks
    root_end = time.time()
    print "total runtime:", root_end - root_start, "seconds."
    print "total splits:", total_splits
    print "total backtracks:", total_backtracks
    print "average runtime:", 1.0 * (root_end - root_start) / (j + 1), "seconds."
    print "average splits:", 1.0 * total_splits / (j + 1)
    print "average backtracks:", 1.0 * total_backtracks / (j + 1)
