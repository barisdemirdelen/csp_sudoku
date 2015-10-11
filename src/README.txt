This is the CSP Solver project of Baris Demirdelen and Maurits Bleeker.
Main program will solve Sudoku's from input file and write the solutions to the output file.
To run the program type in command line:

python main.py input_file.txt output_file.txt

For test example:

python main.py 1000_sudokus.txt output_file.txt


There are three functions that are problem specific for solving a Sudoku puzzle.

def read_sudoku(filename):
	- Reads in the input file and makes a array with strings for every sudoku

def make_variables(sudoku):
	- For every char in the string make a variable and its domain, if the char is equal to "." the domain is 0..9 else the value of the char.

def create_sudoku_constraints(variables):
	- creates the all different constraints for every row, column and block (3x3). 
	When adjusting this to change the problem be really careful with indexing, in particular when creating the the alldiff constraint for a 3x3 box.
	The input of this function is an array with length 81.
	On index 0 is the cell in the left upper corner, on index 80 is the cell on the bottom right corner.

  