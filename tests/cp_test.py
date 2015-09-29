import unittest

from src.cp.cp import CP
from src.cp.variable import Variable
from src.cp.constraints.not_equals_constraint import NotEqualsConstraint
from src.cp.constraints.all_different_constraint import AllDifferentConstraint


class CPTestCase(unittest.TestCase):
    def setUp(self):
        self.cp = CP()
        self.var1 = Variable("var1", [1, 2])
        self.var2 = Variable("var2", [1, 2])
        self.var3 = Variable("var3", [1, 2, 3])
        self.cp.variables = [self.var1, self.var2, self.var3]
        all_different = AllDifferentConstraint("ad-123", [self.var1, self.var2, self.var3])
        self.cp.constraints = [all_different]

    def tearDown(self):
        self.cp = None

    def test_cp(self):
        assignment = self.cp.search()
        self.assertEqual(assignment.get_value(self.var1), 2)
        self.assertEqual(assignment.get_value(self.var2), 1)
        self.assertNotEqual(assignment.get_value(self.var3), 2)


if __name__ == '__main__':
    unittest.main()
