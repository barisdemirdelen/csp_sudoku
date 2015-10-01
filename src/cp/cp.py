from backtracking_search import BacktrackingSearch
from assignment import Assignment
from arc import Arc
import time


class CP:
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.arcs = set()
        self.splits = 0
        self.backtracks = 0
        self.arc_generate_time = 0
        self.remove_inconsistency_time = 0
        self.runtime = 0

    def search(self):
        self.arcs = set()
        self.splits = 0
        self.backtracks = 0
        self.arc_generate_time = 0
        self.remove_inconsistency_time = 0
        self.runtime = 0
        start = time.time()
        for variable1 in self.variables:
            self.generate_arcs(variable1, Assignment(), self.arcs)

        backtracking_search = BacktrackingSearch(self)
        assignment = backtracking_search.search()
        end = time.time()
        self.runtime = end-start
        return assignment

    def is_complete(self, assignment):
        for variable in self.variables:
            if not assignment.is_assigned(variable):
                return False
        return True

    def constraint_propagation(self, assignment):
        if not self.check_consistency(assignment):
            return False
        self.assign_givens(assignment)
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
        arcs = set(self.arcs)
        removed_count = 0
        removed_from = set()
        first = True
        while len(removed_from) > 0 or first:
            first = False
            for variable1 in removed_from:
                self.generate_arcs_to(variable1, assignment, arcs)
            removed_from = set()
            while len(arcs) > 0:
                arc = arcs.pop()
                current_removed = self.remove_inconsistent_values(arc,assignment)
                removed_count += current_removed
                if current_removed > 0:
                    if len(arc.variable1.get_current_domain()) == 0:
                        return False
                    removed_from.add(arc.variable1)
                    # print removed_count, "values removed in", end - start
        return True

    def generate_arcs(self, variable1, assignment, arcs):
        start = time.time()
        if not assignment.is_assigned(variable1):
            for constraint in self.constraints:
                if variable1 in constraint.variables:
                    for variable2 in constraint.variables:
                        if not assignment.is_assigned(variable2):
                            if variable1 != variable2:
                                arcs.add(Arc(variable1, variable2, constraint))
        end = time.time()
        self.arc_generate_time += end - start
        return arcs

    def generate_arcs_to(self, variable2, assignment, arcs):
        start = time.time()
        if not assignment.is_assigned(variable2):
            for constraint in self.constraints:
                if variable2 in constraint.variables:
                    for variable1 in constraint.variables:
                        if not assignment.is_assigned(variable1):
                            if variable1 != variable2:
                                arcs.add(Arc(variable1, variable2, constraint))
        end = time.time()
        self.arc_generate_time += end - start
        return arcs

    def remove_inconsistent_values(self, arc, assignment):
        start = time.time()
        if assignment.is_assigned(arc.variable1):
            return 0
        removed_count = 0
        variable1 = arc.variable1
        variable2 = arc.variable2
        constraint = arc.constraint
        values1 = variable1.get_current_domain()
        for value1 in values1:
            found = False
            values2 = variable2.get_current_domain()
            for value2 in values2:
                if constraint.test_constraint_for_two(variable1, value1, variable2, value2):
                    found = True
                    break
            if not found:
                variable1.get_current_domain().remove(value1)
                removed_count += 1
        end = time.time()
        self.remove_inconsistency_time += end - start
        return removed_count

    def check_consistency(self, assignment):
        return self.arc_consistency(assignment)

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
