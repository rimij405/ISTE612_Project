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
    
    def register(self, f: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator function used to associate a function with this instance's callable dictionary.

        :param f: Function to retrieve or store.
        :type f: Callable[..., Any]
        :return: Return callback function.
        :rtype: Callable[..., Any]
        """
        return self.callbacks.setdefault(f.__name__, f)
        
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

###########################
# DATA STRINGIFIERS
###########################

stringifiers = CallableDict()

###########################
# DATA LOADERS
###########################

loaders = CallableDict()

@loaders.register
def from_json(file: Union[TextIO, BinaryIO], transformer: Callable[..., Any] = None, **kwargs: Any) -> Any:
    data = json.load(file, **kwargs)
    return transformer(data) if transformer and callable(transformer) else data

@loaders.register
def from_csv(file: Union[TextIO, BinaryIO], transformer: Callable[..., Any] = None, **kwargs: Any) -> Any:
    reader = csv.DictReader(file, **kwargs)
    data = [ row for row in reader ]
    return transformer(data) if transformer and callable(transformer) else data

@loaders.register
def from_tsv(file: Union[TextIO, BinaryIO], transformer: Callable[..., Any] = None, **kwargs: Any) -> Any:
    reader = csv.DictReader(file, **kwargs, dialect=csv.excel_tab)
    data = [ row for row in reader ]
    return transformer(data) if transformer and callable(transformer) else data

###########################
# DATA WRITERS
###########################

writers = CallableDict()

@writers.register
def to_json(data: Any, file: Union[TextIO, BinaryIO], transformer: Callable[..., Any] = lambda data: data, **kwargs: Any) -> None:
    json.dump(transformer(data), file, **kwargs)
    
@writers.register
def to_csv(data: Any, file: Union[TextIO, BinaryIO], transformer: Callable[..., Any] = lambda data: data, fieldnames: List[str] = None, include_header: bool = True, **kwargs: Any) -> None:
    writer = csv.DictWriter(file, fieldnames=fieldnames, **kwargs)
    if include_header:
        writer.writeheader()
    writer.writerows(transformer(data))

@writers.register
def to_tsv(data: Any, file: Union[TextIO, BinaryIO], transformer: Callable[..., Any] = lambda data: data, fieldnames: List[str] = None, include_header: bool = True, **kwargs: Any) -> None:
    writer = csv.DictWriter(file, dialect=csv.excel_tab, fieldnames=fieldnames, **kwargs)
    if include_header:
        writer.writeheader()
    writer.writerows(transformer(data))
    
###########################
# UTILITY FUNCTIONS
###########################

def load(file: Union[TextIO, BinaryIO], format: str, transformer: Callable[..., Any] = lambda data: data, **kwargs: Any) -> Any:
    loader = loaders.get(format)
    return loader(file, transformer=transformer, **kwargs)

def dump(data: Any, file: Union[TextIO, BinaryIO], format: str, transformer: Callable[..., Any] = lambda data: data, **kwargs: Any) -> None:
    writer = writers.get(format)
    return writer(data, file, transformer=transformer, **kwargs)

