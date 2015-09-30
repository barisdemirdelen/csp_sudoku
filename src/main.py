import unittest

from cp.cp import CP
from cp.variable import Variable
from cp.constraints.not_equals_constraint import NotEqualsConstraint
from cp.constraints.all_different_constraint import AllDifferentConstraint


def read_sudoku():
	with open("1000 sudokus.txt") as file:
	    sudokus = []
	    for sudoku in file:
	        sudokus.append(sudoku.rstrip().split(","))
	return sudokus

def make_variables(sudokus):
	sudoku = sudokus[0]; #just for testing at the moment, in the end this has to be all the sudoku's :)
	variable_array = [];
	var_num = 1
	for cell in sudoku[0]:
		if cell == ".":
			variable_array.append(Variable("var%d"%var_num, [1, 2, 3, 4, 5, 6, 7, 8, 9])) 
		else:
			variable_array.append(Variable("var%d"%var_num, [int(cell)])) 
		var_num += 1
	return variable_array


def created_sudoku_constraints(variables):
	constaints_array = []
	constraint_num = 1
	for i in range(0,82,9):
		constaints_array.append( AllDifferentConstraint("name%d"%constraint_num, variables[i:i+9]))
		constraint_num += 1 
		if i+9 >= 81:
			break
	for column in range(0,9):
		column_vars = []
		for cell in range(column,81,9):
			colom_vars.append(variables[cell])
		constaints_array.append( AllDifferentConstraint("name%d"%constraint_num, column_vars))
		constraint_num += 1
	#for row in range(0,8)


	



sudokus = read_sudoku()
variables = make_variables(sudokus)
#constraints =  created_sudoku_constraints(variables)

row_start = 0
row_end = 26
for row_block in range(0,3):
	column_start = 0
	column_end = 2
	for column_block in range(0,3):
		array = []
		for i in range(0,82):
			if ((i%9 >= column_start and i%9 <= column_end) and ( i >= row_start and i <= row_end)):
				array.append(i)
		print array  
		column_start += 3
		column_end += 3
	row_start += 26
	row_end += 26			


    

