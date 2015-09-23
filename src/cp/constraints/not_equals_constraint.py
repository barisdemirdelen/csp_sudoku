from constraint import Constraint


class NotEqualsConstraint(Constraint):
    def __init__(self, variable1, variable2):
        super(NotEqualsConstraint, self).__init__()
        self.variables = [variable1, variable2]

    def test_constraint(self, variable, value, assignment):
        if variable in self.variables:
            other_variable = self.variables[0]
            if variable == self.variables[0]:
                other_variable = self.variables[1]
            if assignment.get_value(other_variable) == value:
                return False
        return True
