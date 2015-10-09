class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.initial_domain = domain
        self.domains = [domain]
        self.current_domain = domain

    def get_current_domain(self):
        return self.current_domain

    def set_current_domain(self, domain):
        self.current_domain = list(domain)
        self.domains[len(self.domains)-1] = self.current_domain

    def add_domain_step(self):
        self.current_domain = list(self.get_current_domain())
        self.domains.append(self.current_domain)

    def remove_domain_step(self):
        self.domains.pop()
        self.current_domain = self.domains[len(self.domains)-1]
