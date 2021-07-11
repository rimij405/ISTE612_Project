"""
# verbose.py
# @author Ian Effendi
#
# Prepares verbose printer decorator.
"""

from typing import Any, List, Dict, FunctionType

from utils.constants import to_namedtuple
from argparse import Namespace

# Export verbosity levels.
levels = to_namedtuple('Levels', {
    "NONE": 0,
    "LOW": 1,
    "HIGH": 2,
})

def logger(cargs: Namespace, threshold: int = 0) -> FunctionType:
    """Decorator factory for creating verbose threshold printers."""
    if threshold is None:
        threshold = 0
    def wrapped_printer(*args: List[Any], **kwargs: Dict[str, Any]) -> None:
        """Forward arguments to print() method, if verbose threshold exceeded.
        """
        # Check again if verbosity is changed during runtime.
        if cargs.verbose and cargs.verbose >= threshold:
            print(*args, **kwargs)
    # Return wrapped printer if threshold met; else pass lambda.
    return wrapped_printer if (cargs.verbose and cargs.verbose >= threshold) else lambda _ : 0