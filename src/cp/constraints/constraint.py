from abc import ABCMeta, abstractmethod


class Constraint:
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.variables = []
        self.name = name

    @abstractmethod
    def test_constraint(self, assignment):
        pass

    @abstractmethod
    def test_constraint_for_two(self, variable1, value1, variable2, value2):
        pass

    @abstractmethod
    def get_number_of_rule_outs(self, variable1, value2):
        pass

    @abstractmethod
    def rule_out(self, variable, value):
        pass

    @abstractmethod
    def constraint_specific_propagation(self, assignment):
        pass
