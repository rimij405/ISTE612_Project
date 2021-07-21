"""
# iste.drse.__init__.py
# @author Ian Effendi
#
# Initializes scraper sub-package.
"""
from utils.constants import freeze

import attr

# Test name class.
@attr.s
class Name(object):
    """Forename and surname collection.
    
    :param first: Forename, defaults to "<Forename>"
    :type first: str
    :param last: surname, defaults to "<Surname>"
    :type last: str
    """
    first: str = attr.ib(default="<Forename>")
    last: str  = attr.ib(default="<Surname>")
        
# Test example object.
@attr.s
class Example(object):
    """Example object for testing functions."""    
    name: Name = attr.ib(factory=Name, repr=lambda value: f'{value.first}{value.last}')
    age: int = attr.ib(default=0)
    email: str = attr.ib(default="email@example.com")
    
# Immutable class constants builder.
Constants = freeze('Constants', {
    "program": attr.ib(type=str),
    "bob": attr.ib(factory=Example, type=Example),
    "handy": attr.ib(factory=Example, type=Example),
})

# Instance of runtime constants.
constants = Constants(
    "IRLU <CIL Scraper>",
    Example(Name("Bob", "Builder"), 30, "bob.builder@example.com"),
    Example(Name("Handy", "Manny"), 20, "handy.manny@example.com")
)