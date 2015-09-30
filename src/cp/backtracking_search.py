from assignment import Assignment


class BacktrackingSearch:
    def __init__(self, cp):
        self.cp = cp
        self.assignment = None

    def search(self):
        self.assignment = Assignment()
        return self._recursive_search()

    # dumb backtracking search
    def _recursive_search(self):
        print "assigned", len(self.assignment.assignments)
        if self.cp.is_complete(self.assignment):
            return self.assignment
        variable = self.cp.select_unassigned_variable(self.assignment)
        ordered_values = self.cp.order_domain_values(variable)

        for value in ordered_values:
            if value not in variable.get_current_domain():
                continue
            self.assignment.add(variable, value)
            for variable2 in self.cp.variables:
                variable2.add_domain_step()

            variable.set_current_domain([value])

            if self.cp.is_consistent(self.assignment):
                result = self._recursive_search()
                if result is not None:
                    return result
            for variable in self.cp.variables:
                variable.remove_domain_step()
            self.assignment.remove(variable)
        print "backtracking"
        return None
