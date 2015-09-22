from backtracking_search import BacktrackingSearch


class CP:
    def __init__(self):
        self.variables = []
        self.constraints = []

    def search(self):
        backtracking_search = BacktrackingSearch(self)
        backtracking_search.search()

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment.assignments:
                return False
        return True

    def is_consistent(self, variable, value, assignment):
        self.check_consistency()
        for constraint in self.constraints:
            if variable in constraint.variables:
                if not constraint.test_constraint(variable, value, assignment):
                    return False
        return True

    def check_consistency(self):
        pass

    def remove_inconsistent_values(self, arc):
        pass

    def select_unassigned_variable(self, assignment):
        # write a min remaining values heuristic here
        for variable in self.variables:
            if variable not in assignment.assignments:
                return variable
        return None

    def order_domain_values(self, variable):
        # write a least constraining value heuristic here
        pass
