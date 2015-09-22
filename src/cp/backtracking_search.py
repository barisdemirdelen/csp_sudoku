from assignment import Assignment


class BacktrackingSearch:
    def __init__(self, cp):
        self.cp = cp
        self.assignment = None

    def search(self):
        self.assignment = Assignment()
        self._recursive_search()

    # dumb backtracking search
    def _recursive_search(self):
        if self.cp.is_complete(self.assignment):
            return self.assignment
        variable = self.cp.select_unassigned_variable(self.assignment)
        ordered_values = self.cp.order_domain_values(variable)

        for value in ordered_values:
            if self.cp.is_consistent(variable, value, self.assignment):
                self.assignment.add(variable, value)
                result = self._recursive_search()
                if result is not None:
                    return result
                self.assignment.remove(variable)
        return None
