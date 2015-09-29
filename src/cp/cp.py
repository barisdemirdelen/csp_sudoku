from backtracking_search import BacktrackingSearch
from assignment import Assignment


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
        arcs = []
        for variable1 in self.variables:
            for variable2 in self.variables:
                if variable1 != variable2:
                    for constraint in self.constraints:
                        if variable1 in constraint.variables and variable2 in constraint.variables:
                            arcs.append([variable1, variable2, constraint])

        while len(arcs) > 0:
            arc = arcs.pop()
            self.remove_inconsistent_values(arc)

    def remove_inconsistent_values(self, arc):
        removed = False
        variable1 = arc[0]
        variable2 = arc[1]
        constraint = arc[2]
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
        # write a min remaining values heuristic here
        for variable in self.variables:
            if not assignment.is_assigned(variable):
                return variable
        return None

    def order_domain_values(self, variable):
        # write a least constraining value heuristic here
        return list(variable.domain)
