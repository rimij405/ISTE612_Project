"""
# data.py
# @author Ian Effendi
#
# Utility function related to serializing and deserializing data.
"""
from typing import Any, List, Dict, Tuple, Optional, Callable, TextIO, BinaryIO, Union

import sys, json, csv, attr

###########################
# LOCAL DEFINITIONS
###########################

@attr.s
class CallableDict(object):
    """CallableDict contains a lookup table and decorator function for registering functions."""
    callbacks: Dict[str, Callable[..., Any]] = attr.ib(factory=dict)
    
    def callback(self, f: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator function used to associate a function with this instance's callable dictionary.

        :param f: Function to retrieve or store.
        :type f: Callable[..., Any]
        :return: Return callback function.
        :rtype: Callable[..., Any]
        """
        return self.callbacks.setdefault()
        
    def get(self, key: str, default: Callable[..., Any] = lambda _: 'Invalid function key.'):
        """Get function from the dictionary of callbacks by its key (function name).

        :param key: Function name.
        :type key: str
        :param default: Default function to return if missing callback for key, defaults to lambda_:'Invalid function key.'
        :type default: Callable[..., Any], optional
        :return: Return callback associated with key.
        :rtype: Callable[..., Any]
        """
        return self.callbacks.get(key, default)

loaders = CallableDict()
writers = CallableDict()

###########################
# DATA LOADERS
###########################

@loaders.callback
def load_json():


###########################
# DATA WRITERS
###########################

###########################
# UTILITY FUNCTIONS
###########################

# def to_json(data: Any, file: Optional[Union[TextIO, BinaryIO]] = sys.stdout, converter: Optional[Callable[..., Any]] = lambda value : value, **kwargs: Optional[Any]) -> None:
    """Dump contents into a JSON-format compatible stream.

    :param data: Data to dump.
    :type data: Any
    :param file: Stream IO to dump contents into, defaults to sys.stdout.
    :type file: Union[TextIO, BinaryIO]
    :param converter: Conversion function that prepares data for dumping, defaults to lambda value: value
    :type converter: Callable[..., Any], optional
    """
    # return json.dump(converter(data), file, **kwargs)

# def dumps(data: Any, converter: Optional[Callable[..., Any]] = lambda value : value, **kwargs: Optional[Any]) -> str:
    """Stringify contents of data file into a JSON-formatted object.

    :param data: Data to format.
    :type data: Any
    :param converter: Conversion function that prepares data for dumping, defaults to lambda value: value
    :type converter: Optional[Callable[..., Any]], optional
    :return: Returns stringified JSON content.
    :rtype: str
    """
    # return json.dumps(converter(data), **kwargs)