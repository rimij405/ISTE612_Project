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
    tags: List[str] = attr.ib(default=attr.Factory(list), repr=lambda _tags: f'tags={",".join(*_tags)}')
    
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
        return self.sep.join([ self.prefix, *self.tags, self.label ]) + self.suffix

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

def enumerate_options(options: List[Tuple[str, str, str, List[str]]], sep: str = ".") -> List[Dict[str, Union[str, List[str]]]]:
        
    # inner function
    def select_option(prefix: str, label: str, suffix: str, *tags: str) -> Dict[str, Union[str, List[str]]]:
        return { "prefix": prefix,
                "label": label,
                "suffix": suffix,
                "tags": tags,
                "sep": sep }
        
    return [ select_option(*option) for option in options ]

def generate_filenames(labels: List[str], 
                       formats: List[str], 
                       tags: List[List[str]] = None, 
                       prefix: str = None, 
                       sep: str = "", 
                       logger: Callable[[str], None] = None) -> List[Filename]:
    log = logger if logger else lambda _ : 0
    if tags and isinstance(tags, str):
        tags = [ tags ]    
    
    # Ensure non-null.
    labels = labels if labels else [ defaults.label ]
    log(f'\tLabels: {labels}')
    formats = [ f'.{ext}' for ext in formats ] if formats else [ defaults.suffix ]
    log(f'\tFormats: {formats}')
    tags = [ tags ] if tags else [ defaults.tags ]
    log(f'\tTags: {tags}')
    prefix = [ prefix ] if prefix else [ defaults.prefix ]
    log(f'\tprefix: {prefix}')
    sep = sep if sep else defaults.sep
    log(f'\tsep: {sep}')
    
    # Example: tags = [ ['NY', 'new york'], ['OH', 'ohio'] ] or tags = [ 'NY', 'OH' ]
        
    # Calculate filename permutations in product space
    log("\tCalculating filename permutations from components provided:")
    options: List[Tuple[str, str, str, List[str]]] = list(product(*[ prefix, labels, formats, *tags ]))
    
    # Enumerate options.
    log("\tEnumerating filenames from collection of provided options.")
    filenames: List[Filename] = [ Filename.from_dict(attrs) for attrs in enumerate_options(options, sep=sep) ]

    # Print generated filenames.
    log(f'\tGenerated {len(filenames)} filename(s):')
    for filename in filenames:
        log(f'\t\t"{filename.get_qualified_filename()}"')
    
    # Return generated filenames.
    return filenames