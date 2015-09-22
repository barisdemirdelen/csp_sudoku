from abc import ABCMeta, abstractmethod


class Constraint:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.variables = []

    @abstractmethod
    def test_constraint(self, variable, value, assignment):
        pass
