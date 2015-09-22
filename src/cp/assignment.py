class Assignment:
    def __init__(self):
        self.assignments = {}

    def add(self, variable, value):
        self.assignments[variable] = value

    def remove(self, variable):
        self.assignments.pop(variable)
