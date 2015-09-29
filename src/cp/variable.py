class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.initial_domain = domain
        self.domains = [domain]

    def get_current_domain(self):
        return self.domains[len(self.domains)-1]

    def set_current_domain(self, domain):
        self.domains[len(self.domains)-1] = domain

    def add_domain_step(self):
        self.domains.append(self.get_current_domain())

    def remove_domain_step(self):
        self.domains.pop()