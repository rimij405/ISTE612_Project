class State:
    def __init__(self, state, abbreviation, code, population):
        self.state = state
        self.abbreviation = abbreviation
        self.code = code
        self.population = population
        
    def data(self):
        data = {
            'state': self.state,
            'abbr': self.abbreviation,
            'code': self.code,
            'pop': self.population      
        }
        return data