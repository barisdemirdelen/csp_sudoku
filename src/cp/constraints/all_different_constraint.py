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

    def test_constraint_for_two(self, variable1, value1, variable2, value2):
        return value1 != value2

    def get_number_of_rule_outs(self, variable1, value2):
        rule_out = 0
        if variable1 in self.variables:
            if value2 in variable1.get_current_domain():
                rule_out = 1
        return rule_out
