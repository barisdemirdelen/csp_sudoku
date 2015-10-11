This is the CPS-solver project of Maurits Bleeker and Baris Demirdelen.

For instructions to run the program go to the map source, there is a readme file that explains how to run the program. 

If you want to edit the CSP go to the file src/main.py.

There are three functions that are problem specific for solving a sudoku puzzle.

def read_sudoku(filename):
	- reads in the input file and makes a array with strings for every sudoku

def make_variables(sudoku):
	- for every char in the string (that is a cell) make a variable and it’s domain, if the char is equal to “.” the domain is 0..9 else the value of the char.

def create_sudoku_constraints(variables):
	- creates the all different constraints for every row column and block (3x3). when  	adjusting this to change the problem be really careful with indexing, in 		particular when creating the the alldiff constraint for a 3x3 box. The input of 	this function is an array with length 81. On index 0 is the cell in the left 		uppercorner, on index 80 is the cell on the bottom rightcorner.

  
