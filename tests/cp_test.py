import unittest
from src.cp.cp import CP
from src.cp.variable import Variable
from src.cp.constraints.not_equals_constraint import NotEqualsConstraint


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