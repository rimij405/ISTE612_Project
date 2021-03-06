"""
# iste.utils.__init__.py
# @author Ian Effendi
#
# Initializes utils sub-package.
"""
from typing import Any, Dict, Callable

def logged(callback: Callable) -> Callable:
    """Decorate a callback function to print a message prior to execution.

    :param callback: Callback function to execute
    :type callback: FunctionType
    :return: Return wrapped callback.
    :rtype: FunctionType
    """
    def wrapped(*args: Any, message: str = None, logger: Callable = None, **kwargs: Any) -> Any:
        """Print message prior to executing passed function.

        :param message: Message to print, defaults to None
        :type message: str, optional
        :param logger: Logger to print message with, defaults to None
        :type logger: FunctionType, optional
        :return: Returns result of passed function.
        :rtype: Any
        """
        log = logger if logger else lambda _ : 0
        if message:
            log(message)
        return callback(*args, logger=logger, **kwargs)
    return wrapped