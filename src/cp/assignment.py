class Assignment:
    def __init__(self):
        self.assignments = [{}]

    def add(self, variable, value):
        self.assignments[-1][variable.name] = value

    def remove(self, variable):
        del self.assignments[-1][variable.name]

    def get_value(self, variable):
        if self.is_assigned(variable):
            return self.assignments[-1][variable.name]
        return None

    def is_assigned(self, variable):
        return variable.name in self.assignments[-1]

    def get_current_assignemnts(self):
        return self.assignments[-1]

    def add_assignment_step(self):
        self.assignments.append(self.assignments[-1].copy())

    def remove_assignment_step(self):
        self.assignments.pop()
