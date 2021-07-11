"""
# duplicates.py
# @author Ian Effendi
#
# Deduplicate an arbitrary amount of elements from a List-like.
"""

from typing import Any, List, Set, FunctionType

from . import logged

@logged
def deduplicate(array: List[Any], logger: FunctionType = None) -> Set:
    """Deduplicate arbitrary amount of items in a list.
        
    :param array: Array to deduplicate.
    :type array: List[Any]
    :param logger: Logger that can be optionally used to print messages.
    :type logger: FunctionType
    :raises argparse.ArgumentError: Raised if required argument is missing.
    :return: Return deduplicated collection.
    :rtype: Set
    """
    log = logger if logger else lambda _ : 0
    if not array:
        log("\tSkipping. Nothing to deduplicate with empty collection.")
        return set()
    else:
        log(f'\t[In]: {array}')
        items = set(array)
        response = f'\t[Out]: {items}.'
        diff = len(array) - len(items)
        if(diff != 0):
            response += f' Removed {diff} duplicate(s).'
        else:
            response += f' Arguments unchanged. No duplicates to remove.'
        log(response)
        return items
    