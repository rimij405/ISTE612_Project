"""
# filenames.py
# @author Ian Effendi
#
# Contains helper functions for managing on-the-fly generation of filenames at runtime.
"""
import attr

from typing import Any, List, Dict, Tuple, Callable, Union
from argparse import Namespace
from itertools import product

from . import logged

###########################
# UTILITY CLASSES
###########################

@attr.s
class Filename(object):
    sep: str = attr.ib(default="")
    prefix: str = attr.ib(default="")
    suffix: str = attr.ib(default=".txt")
    label: str = attr.ib(default="<label>")
    tags: List[str] = attr.ib(default=[], factory=list, repr=lambda _tags: f'tags={",".join(*_tags)}')
    
    @classmethod
    def from_dict(cls: type, attrs: Dict[str, Union[str, List[str]]]) -> object:
        """Construct a Filename object instance using a Dict.

        :param fields: Attributes.
        :type fields: Union[str, List[str]]]
        :return: Constructed instance.
        :rtype: Filename
        """
        return cls(**attrs)
    
    def get_qualified_filename(self) -> str:
        """Create the qualified filename from the included steps.

        :return: Created filename.
        :rtype: str
        """
        _tags = [ f'<{tag}>' for tag in self.tags ] if self.tags else []
        return self.sep.join([ self.prefix, *_tags, self.label ]) + self.suffix

# Defaults object.
defaults = Filename()

# Template Filename object.
template = Filename(
    sep = "<separator>",
    prefix = "<namespace>",
    suffix = "<extension>",
    label = "<label>",
    tags = [ '<state_code>' ]    
)

###########################
# UTILITY FUNCTIONS
###########################

def make_qualified_filename(attrs: Dict[str, Any]) -> Filename:
    return Filename.from_dict(attrs)

def enumerate_options(options: List[Tuple[str, str, List[str], str]]) -> List[Dict[str, Union[str, List[str]]]]:
    return [ { "prefix": prefix, 
              "label": label, 
              "tags": tags, 
              "suffix": suffix } 
            for (prefix, label, tags, suffix) in options ]

def generate_filenames(labels: List[str], 
                       formats: List[str], 
                       tags: List[List[str]] = None, 
                       prefix: str = None, 
                       sep: str = "", 
                       logger: Callable[[str], None] = None) -> List[Filename]:
    
    # Ensure is list.
    if tags and isinstance(tags, str):
        tags = [ tags ]
    
    # Ensure non-null.
    labels = labels if labels else [ defaults.label ]
    formats = formats if formats else [ defaults.suffix ]
    tags = tags if tags else [ defaults.tags ]
    prefix = prefix if prefix else defaults.prefix
    sep = sep if sep else defaults.sep
    log = logger if logger else lambda _ : 0
    
    # Example: tags = [ ['NY', 'new york'], ['OH', 'ohio'] ] or tags = [ 'NY', 'OH' ]
        
    # Calculate filename permutations in product space
    log("\tCalculating filename permutations from components provided.")
    options: List[Tuple[str, str, List[str], str]] = list(product(*[ prefix, *tags, labels, formats ]))
    
    # Enumerate options.
    log("\tEnumerating filenames from collection of provided options.")
    filenames: List[Filename] = [ Filename.from_dict(attrs) for attrs in enumerate_options(options) ]

    # Print generated filenames.
    log(f'\tGenerated {len(filenames)} filename(s):')
    for filename in filenames:
        log(f'\t\t"{filename.get_qualified_filename()}"')
    
    # Return generated filenames.
    return filenames