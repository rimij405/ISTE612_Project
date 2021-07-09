import json

class JSONReader():
    
    def __init__():
        """Prepare the JSON reader."""
        
    def parseFile(fileURI, encoding='utf-8'):
        with open(fileURI, encoding) as jsonFile:
            data = json.load(jsonFile)
            return data
    
    def parse(content):
        return json.dumps(content)