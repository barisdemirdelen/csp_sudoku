from backtracking_search import BacktrackingSearch
from assignment import Assignment
#from arc import Arc


class CP:
    def __init__(self):
        self.variables = []
        self.constraints = []

    def search(self):
        backtracking_search = BacktrackingSearch(self)
        return backtracking_search.search()

    def is_complete(self, assignment):
        for variable in self.variables:
            if not assignment.is_assigned(variable):
                return False
        return True

    def is_consistent(self, assignment):
        self.check_consistency()
        for variable in self.variables:
            if assignment.is_assigned(variable):
                if assignment.get_value(variable) not in variable.domain:
                    return False
        for constraint in self.constraints:
            if not constraint.test_constraint(assignment):
                return False
        return True

    def arc_consistency(self):
        arcs = set()
        for variable1 in self.variables:
            arcs = self.generate_arcs(variable1, arcs)

        while len(arcs) > 0:
            arc = arcs.pop()
            if self.remove_inconsistent_values(arc):
                arcs = self.generate_arcs(arc.variable1, arcs)

    def generate_arcs(self, variable1, arcs):
        for variable2 in self.variables:
            if variable1 != variable2:
                for constraint in self.constraints:
                    if variable1 in constraint.variables and variable2 in constraint.variables:
                        arcs.add(Arc(variable1, variable2, constraint))
        return arcs

    def remove_inconsistent_values(self, arc):
        removed = False
        variable1 = arc.variable1
        variable2 = arc.variable2
        constraint = arc.constraint
        for value1 in variable1.domain:
            found = False
            assignment = Assignment()
            assignment.add(variable1, value1)
            for value2 in variable2.domain:
                assignment.add(variable2, value2)
                if constraint.test_constraint(assignment):
                    found = True
                    assignment.remove(variable2)
                    break
                assignment.remove(variable2)

            if not found:
                variable1.domain.remove(value1)
                removed = True
        return removed

    def check_consistency(self):
        self.arc_consistency()

    def select_unassigned_variable(self, assignment):
        # uses min remaining values heuristic

        min_remaining_values = float("inf")
        min_variable = None
        for variable in self.variables:
            if not assignment.is_assigned(variable):
                current_remaining_values = len(variable.domain)
                if current_remaining_values <= min_remaining_values:
                    if current_remaining_values == min_remaining_values:
                        # a degree heuristic may be written here
                        pass
                    min_variable = variable
                    min_remaining_values = current_remaining_values
        return min_variable

    def order_domain_values(self, variable):
        # uses least constraining value heuristic

        ordered_domain = []
        rule_out_list = []

        for value in variable.domain:
            rule_out = 0
            for constraint in self.constraints:
                for variable2 in self.variables:
                    if variable != variable2:
                        rule_out = rule_out + constraint.get_number_of_rule_outs(variable2, value)
            found = False
            for i in range(len(ordered_domain)):
                if rule_out_list[i] > rule_out:
                    rule_out_list.insert(i, rule_out)
                    ordered_domain.insert(i, value)
                    found = True
                    break
            if not found:
                rule_out_list.append(rule_out)
                ordered_domain.append(value)
        return ordered_domain
