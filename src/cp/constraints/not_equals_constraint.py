from constraint import Constraint


class NotEqualsConstraint(Constraint):
    def __init__(self, name, variable1, variable2):
        super(NotEqualsConstraint, self).__init__(name)
        self.variables = [variable1, variable2]

    def test_constraint(self, assignment):
        if assignment.is_assigned(self.variables[0]) and assignment.is_assigned(self.variables[1]):
            return assignment.get_value(self.variables[0]) != assignment.get_value(self.variables[1])
        return True

    def test_constraint_for_two(self, variable1, value1, variable2, value2):
        return value1 != value2

    def get_number_of_rule_outs(self, variable1, value2):
        rule_out = 0
        if variable1 in self.variables:
            for value1 in variable1.domain:
                if value1 == value2:
                    rule_out += 1
                    break
        return rule_out

    def rule_out(self, variable, value):
        deduced_variables = []
        for variable2 in self.variables:
            if variable != variable2:
                if value in variable2.get_current_domain():
                    variable2.get_current_domain().remove(value)
                    if len(variable2.get_current_domain()) == 0:
                        return False, deduced_variables
                    if len(variable2.get_current_domain()) == 1:
                        deduced_variables.append(variable2)
        return True, deduced_variables

    def constraint_specific_propagation(self, assignment):
        return True
