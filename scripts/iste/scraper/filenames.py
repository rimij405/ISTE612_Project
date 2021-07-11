
from typing import Any, List, Dict
from argparse import Namespace
from itertools import product

from utils import logged
from utils.constants import freeze

###########################
# CONSTANTS
###########################

templates = freeze({
    "prefix": "<prefix>",
    "separator": "<sep>",
    "basename": "<basename>",
    "state": "<state_code>",
    "suffix": "<suffix>"        
})

template_filename = templates.separator.join(filter(None, [templates.prefix, templates.state, templates.basename, templates.suffix]))

defaults = freeze({
    "prefix": "iste",
    "separator": "",
    "basename": "<output>",
    "state": "",
    "suffix": ".txt"
})

default_filename = f'{components.defaults.}{}{}{}{}'

###########################
# UTILITY FUNCTIONS
###########################

def make_qualified_filename(
    basename: str, state: str = None,
    prefix: str = None, suffix: str = defaults.suffix,
    sep: str = defaults.separator) -> str:
    """Construct filename using input components.

    :param basename: Basename of the file to output, defaults to "<output>"
    :type basename: str
    :param state: State code to associate with the filename, defaults to None
    :type state: str, optional
    :param prefix: Prefix namespace to associate with the filename, defaults to None
    :type prefix: str, optional
    :param suffix: Extension declaring file format, defaults to ".txt"
    :type suffix: str
    :param sep: Separator character, defaults to ""
    :type sep: str, optional
    :raise ValueError: Raised if missing sep, basename, or suffix.
    :return: Return qualified filename.
    :rtype: str
    """

    # Validate required inputs.
    sep = sep if sep else defaults.separator
    # basename = basename if basename else defaults.basename
    # suffix = suffix if suffix else defaults.suffix
    
    # Error if missing components.
    if not basename or not suffix:
        raise ValueError("Missing minimum requirements to construct qualified filename.")
    
    # Construct joined string from filtered elements.
    components = [ prefix, state, basename ]
    return sep.join(filter(None, components)) + suffix

def to_filename(components: Dict[str, str]) -> str:
    """Convert a Dict-like of components into a qualified filename.

    :param components: [description]
    :type components: Dict[str, str]
    :return: [description]
    :rtype: str
    """
    return make_qualified_filename(
        basename=components.basename,
        
    )

###########################
# VARIABLES
###########################

# Template filename.
TEMPLATE_FILENAME = to_filename(**templates)

# Default filename.
DEFAULT_FILENAME = to_filename(**defaults)

