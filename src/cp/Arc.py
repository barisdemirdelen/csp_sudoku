class Arc:
    def __init__(self, variable1, variable2, constraint):
        self.variable1 = variable1
        self.variable2 = variable2
        self.constraint = constraint
        self.hash = hash((self.variable1.name, self.variable2.name, self.constraint.name))

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.variable1 == other.variable1
                and self.variable2 == other.variable2
                and self.constraint == other.constraint)

    def __ne__(self, other):
        return not self.__eq__(other)
