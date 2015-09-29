from constraint import Constraint


class AllDifferentConstraint(Constraint):
    def __init__(self, name, variables):
        super(AllDifferentConstraint, self).__init__(name)
        self.variables = variables

    def test_constraint(self, assignment):
        values = set()
        for variable in self.variables:
            if assignment.is_assigned(variable):
                value = assignment.get_value(variable)
                if value in values:
                    return False
                values.add(value)
        return True
