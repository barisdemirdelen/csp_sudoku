import heapq
from backtracking_search import BacktrackingSearch
from assignment import Assignment
from arc import Arc
import time


class CP:
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.variables_to_constraints = {}
        self.arcs = set()
        self.splits = 0
        self.backtracks = 0
        self.arc_generate_time = 0
        self.remove_inconsistency_time = 0
        self.runtime = 0
        self.arc = True  # arc consistency
        self.fc = True  # forward checking
        self.mrv = True  # min remaining values
        self.lcv = True  # least constraining value
        self.specific = True  # constraint specific progpagation (alldiff-specific)
        self.md = True  # maximum degree

    def search(self):
        start = time.time()
        self.arcs = set()
        self.splits = 0
        self.backtracks = 0
        self.arc_generate_time = 0
        self.remove_inconsistency_time = 0
        self.runtime = 0
        for variable in self.variables:
            self.variables_to_constraints[variable.name] = []
        for constraint in self.constraints:
            for variable in constraint.variables:
                self.variables_to_constraints[variable.name].append(constraint)

        for variable1 in self.variables:
            self.generate_arcs(variable1, Assignment(), self.arcs)

        backtracking_search = BacktrackingSearch(self)
        assignment = backtracking_search.search()
        end = time.time()
        self.runtime = end - start
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
        if self.specific:
            for constraint in self.constraints:
                if not constraint.constraint_specific_propagation(assignment):
                    return False
        return self.is_consistent(assignment)

    def is_consistent(self, assignment):
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
                current_removed = self.remove_inconsistent_values(arc, assignment)
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
            for constraint in self.variables_to_constraints[variable1.name]:
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
            for constraint in self.variables_to_constraints[variable2.name]:
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
        if self.arc:
            return self.arc_consistency(assignment)
        return True

    def forward_check(self, variable, assignment):
        next_check = set()
        next_check.add(variable)
        while len(next_check) > 0:
            current_variable = next_check.pop()
            for constraint in self.variables_to_constraints[current_variable.name]:
                consistent, deduced_variables = constraint.rule_out(current_variable,
                                                                    current_variable.get_current_domain()[0])
                for variable2 in deduced_variables:
                    assignment.add(variable2, variable2.get_current_domain()[0])
                    next_check.add(variable2)
                if not consistent:
                    return False
        return True

    def select_unassigned_variable(self, assignment):
        # uses min remaining values heuristic

        if not self.mrv:
            for variable in self.variables:
                if not assignment.is_assigned(variable):
                    return variable
            return None

        min_remaining_values = float("inf")
        min_variable = None
        max_degree = 0
        for variable in self.variables:
            if not assignment.is_assigned(variable):
                current_remaining_values = len(variable.get_current_domain())
                if current_remaining_values <= min_remaining_values:
                    if self.md and current_remaining_values == min_remaining_values:
                        # max degree heuristic
                        current_degree = self.get_variable_degree(variable, assignment)
                        if current_degree >= max_degree:
                            max_degree = self.get_variable_degree(variable, assignment)
                            min_variable = variable
                            min_remaining_values = current_remaining_values
                    else:
                        max_degree = self.get_variable_degree(variable, assignment)
                        min_variable = variable
                        min_remaining_values = current_remaining_values
        return min_variable

    def get_variable_degree(self, variable, assignment):
        constrained_variables = set()
        for constraint in self.variables_to_constraints[variable.name]:
            for variable2 in constraint.variables:
                if variable != variable2 and not assignment.is_assigned(variable2):
                    constrained_variables.add(variable2)
        return len(constrained_variables)

    def order_domain_values(self, variable):
        # uses least constraining value heuristic
        if not self.lcv:
            return list(variable.get_current_domain())

        ordered_domain = []
        for value in variable.get_current_domain():
            rule_out = 0
            for constraint in self.variables_to_constraints[variable.name]:
                for variable2 in constraint.variables:
                    if variable != variable2:
                        rule_out += constraint.get_number_of_rule_outs(variable2, value)
            ordered_domain.append((value, rule_out))
        ordered_domain = heapq.nsmallest(len(ordered_domain), ordered_domain, key=lambda e: e[1])
        for i in range(len(ordered_domain)):
            ordered_domain[i] = ordered_domain[i][0]

        return ordered_domain

    def assign_givens(self, assignment):
        for variable in self.variables:
            if len(variable.get_current_domain()) == 1:
                assignment.add(variable, variable.get_current_domain()[0])
