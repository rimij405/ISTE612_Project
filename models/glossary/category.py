class Category:
    
    def __init__(self, category, description):
        self.category = category
        self.description = description
        
    def data(self):
        data = {
            'cat': self.category,
            'desc': self.description
        }
        return data