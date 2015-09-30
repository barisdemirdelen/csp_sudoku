from backtracking_search import BacktrackingSearch
from assignment import Assignment
from arc import Arc
import time


class CP:
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.arcs = set()

    def search(self):
        self.arcs = set()
        for variable1 in self.variables:
            self.arcs = self.generate_arcs(variable1, self.arcs)

        backtracking_search = BacktrackingSearch(self)
        return backtracking_search.search()

    def is_complete(self, assignment):
        for variable in self.variables:
            if not assignment.is_assigned(variable):
                return False
        return True

    def is_consistent(self, assignment):
        self.check_consistency(assignment)
        for variable in self.variables:
            if len(variable.get_current_domain()) == 0:
                return False
            if assignment.is_assigned(variable):
                if assignment.get_value(variable) not in variable.get_current_domain():
                    return False
        for constraint in self.constraints:
            if not constraint.test_constraint(assignment):
                return False
        return True

    def arc_consistency(self, assignment):
        start = time.time()
        arcs = set(self.arcs)
        removed_count = 0
        removed_from = set()
        first = True
        while len(removed_from) > 0 or first:
            first = False
            """for variable1 in removed_from:
                self.generate_arcs(variable1, arcs)"""
            removed_from = set()
            while len(arcs) > 0:
                arc = arcs.pop()
                current_removed = self.remove_inconsistent_values(arc, assignment)
                removed_count += current_removed
                """if current_removed > 0:
                    removed_from.add(arc.variable1)"""
        end = time.time()
        print removed_count, "values removed in", end - start

    def generate_arcs(self, variable1, arcs):
        for constraint in self.constraints:
            if variable1 in constraint.variables:
                for variable2 in constraint.variables:
                    if variable1 != variable2:
                        arcs.add(Arc(variable1, variable2, constraint))
        return arcs

    def remove_inconsistent_values(self, arc, assignment):
        removed_count = 0
        variable1 = arc.variable1
        variable2 = arc.variable2
        constraint = arc.constraint
        values1 = variable1.get_current_domain()
        remove1 = True
        if assignment.is_assigned(variable1):
            remove1 = False
        for value1 in values1:
            found = False
            assignment.add(variable1, value1)
            values2 = variable2.get_current_domain()
            remove2 = True
            if assignment.is_assigned(variable2):
                remove2 = False
            for value2 in values2:
                assignment.add(variable2, value2)
                if constraint.test_constraint(assignment):
                    found = True
                    if remove2:
                        assignment.remove(variable2)
                    break
                if remove2:
                    assignment.remove(variable2)

            if not found:
                variable1.get_current_domain().remove(value1)
                removed_count += 1
            if remove1:
                assignment.remove(variable1)
        return removed_count

    def check_consistency(self, assignment):
        self.arc_consistency(assignment)

    def select_unassigned_variable(self, assignment):
        # uses min remaining values heuristic

        """for variable in self.variables:
            if not assignment.is_assigned(variable):
                return variable
        return None"""

        min_remaining_values = float("inf")
        min_variable = None
        for variable in self.variables:
            if not assignment.is_assigned(variable):
                current_remaining_values = len(variable.get_current_domain())
                if current_remaining_values <= min_remaining_values:
                    if current_remaining_values == min_remaining_values:
                        # a degree heuristic may be written here
                        pass
                    min_variable = variable
                    min_remaining_values = current_remaining_values
        return min_variable

    def order_domain_values(self, variable):
        # uses least constraining value heuristic
        return list(variable.get_current_domain())
        """ordered_domain = []
        rule_out_list = []

        for value in variable.get_current_domain():
            rule_out = 0
            for constraint in self.constraints:
                if variable in constraint.variables:
                    for variable2 in self.variables:
                        if variable != variable2:
                            rule_out += constraint.get_number_of_rule_outs(variable2, value)
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
        return ordered_domain"""

    def assign_givens(self, assignment):
        for variable in self.variables:
            if len(variable.get_current_domain()) == 1:
                assignment.add(variable, variable.get_current_domain()[0])
