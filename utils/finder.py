# finder.py
# Author: Ian Effendi
# 
# Assortment of utility functions for finding elements in a list-like structure.
from typing import Any, List, Union, Tuple, Callable

def has_key(x: Any, key: Any) -> bool:
    """
    Check for existence of attribute 'key' on x.
    :returns: bool, True if conditions are met.
    """
    try:
        if x[key]:
            return True
        return False
    except:
        return False
        
def has_value(x: Any, value: Any, key: Any = None) -> bool:
    """
    Check if x is value. If key is provided, check if x has attribute key with value.
    :returns: bool, True if conditions are met.
    """
    if key:
        try:
            if x[key] == value:
                return True
            return False
        except:
            return False
    else:
        return x == value

# _one functions.

def index_of(arr: List[Any], predicate: Union[Any, Callable[[Any], bool]]) -> Tuple[int, Any]:
    """
    Find the index of first match.
    :returns: -1 if match is not found.
    """
    try:
        for i in range(len(arr)):
            if predicate(arr[i]):
                return i, arr[i]
    except:
        for i in range(len(arr)):
            if arr[i] == predicate:
                return i, arr[i]
    return -1, None

def find_one(li: List[Any], predicate: Union[Any, Callable[[Any], bool]]) -> Union[Any, None]:
    """
    Find first element in list-like that makes the predicate resolve to True.
    :returns: None if match is not found.
    """
    try:
        for x in li:
            if predicate(x):
                return x
    except:
        for x in li:
            if x == predicate:
                return x
    return None

def match_any(li: List[Any], value: Any, key: Any = None) -> bool:
    """
    Find any element in list-like that makes the predicate resolve to True.
    :returns: bool, True if any in the list meet the conditions.
    """
    if find_one(li, lambda x: has_value(x=x, value=value, key=key)):
        return True
    return False

# _many() functions.

def index_all(arr: List[Any], predicate: Union[Any, Callable[[Any], bool]]) -> List[int]:
    """
    Find the indices of all matches.
    :returns: Empty list if no matches are found.
    """
    try:
        indices = [i for i in range(len(arr)) if predicate(arr[i])]
    except:
        indices = [i for i in range(len(arr)) if arr[i] == predicate]
    return indices

def find_many(li: List[Any], predicate: Union[Any, Callable[[Any], bool]]) -> List[Any]:
    """
    Find all elements in list-like that makes the predicate resolve to True.
    :returns: List. List will be empty if match is not found.
    """
    try:
        matches = [x for x in li if predicate(x)]
    except:
        matches = [x for x in li if x == predicate]
    return matches

def match_all(li: List[Any], value: Any, key: Any = None) -> bool:
    """
    Find all elements in list-like that makes the predicate resolve to True.
    :returns: bool, True if all in the list meet the conditions.
    """
    results = find_many(li, lambda x: has_value(x=x, value=value, key=key))
    if results and len(results) == len(li):
        return True
    return False
