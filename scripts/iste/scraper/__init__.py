"""
# iste.scraper.__init__.py
# @author Ian Effendi
#
# Initializes scraper sub-package.
"""

from utils.constants import freeze

# Create a Constants named Tuple, making a dictionary immutable.
constants = freeze({
    'program': 'IRLU <CIL Scraper>',
    'bob': {     
        "name": { 
            "first": "Bob",
            "last": "Builder",
        },
        "age": 20,
        "email": "bob.builder@example.com"
    },
    "handy": {
        "name": {
            "first": "Handy",
            "last": "Manny",
        },
        "age": 18,
        "email": "handy.manny@example.com"
    }
})