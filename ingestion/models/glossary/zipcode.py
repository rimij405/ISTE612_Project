class Zipcode:
    def __init__(self, zipcode, city, county, population):
        self.zipcode = zipcode
        self.city = city
        self.county = county
        self.population = population
        
    def data(self):
        data = {
            'zip': self.zipcode,
            'city': self.city,
            'county': self.county,
            'pop': self.population            
        }
        return data