from constraint import Constraint


class NotEqualsConstraint(Constraint):
    def __init__(self, name, variable1, variable2):
        super(NotEqualsConstraint, self).__init__(name)
        self.variables = [variable1, variable2]

    def test_constraint(self, assignment):
        if assignment.is_assigned(self.variables[0]) and assignment.is_assigned(self.variables[1]):
            return assignment.get_value(self.variables[0]) != assignment.get_value(self.variables[1])
        return True
