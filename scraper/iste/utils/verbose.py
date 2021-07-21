"""
# verbose.py
# @author Ian Effendi
#
# Prepares verbose printer decorator.
"""
from typing import Any, List, Dict, Callable
from argparse import Namespace
from functools import wraps

import attr

# Export verbosity levels.
levels = attr.make_class('Levels', {
                            "NONE": attr.ib(default=0),
                            "LOW":  attr.ib(default=1),
                            "HIGH": attr.ib(default=2)
                        })()

def logger(cargs: Namespace, threshold: int = 0) -> Callable:
    """Decorator factory for creating verbose threshold printers."""
    if threshold is None:
        threshold = 0
    @wraps(print)
    def wrapper(*args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """Forward arguments to print() method, if verbose threshold exceeded.
        """
        # Check again if verbosity is changed during runtime.
        if cargs.verbose and cargs.verbose >= threshold:
            print(*args, **kwargs)
    # Return wrapped printer if threshold met; else pass lambda.
    return wrapper if (cargs.verbose and cargs.verbose >= threshold) else lambda _ : 0