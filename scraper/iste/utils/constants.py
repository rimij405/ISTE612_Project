"""
# constants.py
# @author Ian Effendi
#
# Expose utility functions for freezing dictionary objects into 'Constant' attr classes.
"""
from typing import Any

import attr

def freeze(label: str, *args, **kwargs) -> Any:
    """Generate an immutable structure.

    :param label: Classname to assign to the immutable structure.
    :type label: str
    :param attrs: Attributes to populate class with.
    :type attrs: Union[List[str], Tuple[str, ...], Dict[str, Any]]
    :return: Returns class declaration.
    :rtype: type
    """
    return attr.make_class(label, *args, **kwargs, frozen=True)