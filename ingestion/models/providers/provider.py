class Provider:
    def __init__(self, **kwargs):
        self.provider = kwargs.get('provider', None)
        self.service = kwargs.get('service', 'Unknown')
        self.address = kwargs.get('address', {})
        self.keywords = kwargs.get('keywords', [])
        
    def data(self):
        data = {
            'provider': self.provider,
            'service': self.service,
            'address': self.address,
            'keywords': self.keywords
        }
        return data