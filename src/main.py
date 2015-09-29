import unittest

from cp.cp import CP
from cp.variable import Variable
from cp.constraints.not_equals_constraint import NotEqualsConstraint


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


sudokus = read_sudoku()
variables = make_variables(sudokus)

    

'''

class CPTestCase(unittest.TestCase):
    def setUp(self):
        self.cp = CP()
        self.var1 = Variable("var1", [1, 2])
        self.var2 = Variable("var2", [1])
        self.cp.variables = [self.var1, self.var2]
        self.not_equals = NotEqualsConstraint(self.var1, self.var2)
        self.cp.constraints = [self.not_equals]

    def tearDown(self):
        self.cp = None

    def test_cp(self):
        assignment = self.cp.search()
        self.assertEqual(assignment.get_value(self.var1), 2)
        self.assertEqual(assignment.get_value(self.var2), 1)

if __name__ == '__main__':
    unittest.main()

    '''