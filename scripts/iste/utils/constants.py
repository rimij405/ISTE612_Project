"""
# constants.py
# @author Ian Effendi
#
# Expose utility functions for freezing dictionary objects into 'Constant' named Tuples.
"""

from collections import namedtuple
from typing import Any, Union, List, Set, Dict, Tuple, Type

def Schema(label: str, keys: List[str]) -> Type[Tuple]:
    """Create named Tuple subclass.

    :param label: Label to give namedtuple instance.
    :type label: str
    :param keys: Keys to give namedtuple instance.
    :type keys: List[str]
    :return: Named Tuple subclass with schema settings.
    :rtype: Type[Tuple]
    """
    return namedtuple(label, keys)

def to_namedtuple(label: str, data: Dict[str, Any]) -> Tuple:
    """Create instance of named Tuple subclass.
    
    :param label: Label to give namedtuple instance.
    :type label: str
    :param data: Data to populate subclass.
    :type data: Dict[str, Any]
    :return: Named Tuple subclass instance.
    :rtype: Tuple
    """
    orderedKeys = list(data.keys())
    return Schema(label, orderedKeys)(*[data.get(key) for key in orderedKeys])

def freeze(data: Dict[str, Any]) -> Tuple:
    """Create instance of named Tuple subclass from a Dictionary instance.
    
    :param data: Data to populate subclass.
    :type data: Dict[str, Any]
    :return: Named Tuple subclass instance.
    :rtype: Tuple
    """
    return to_namedtuple('Constants', data)