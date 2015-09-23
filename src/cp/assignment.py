class Assignment:
    def __init__(self):
        self.assignments = {}

    def add(self, variable, value):
        self.assignments[variable.name] = value

    def remove(self, variable):
        self.assignments.pop(variable.name)

    def get_value(self, variable):
        if self.is_assigned(variable):
            return self.assignments[variable.name]
        return None

    def is_assigned(self, variable):
        return variable.name in self.assignments
