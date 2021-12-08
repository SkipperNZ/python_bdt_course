"""typical docstring"""
import functools
from contextlib import ContextDecorator


def verbose(func):
    """typical docstring"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("before function call")
        outcome = func(*args, **kwargs)
        print("after function call")
        return outcome
    return wrapper


def repeater(count: int):
    """typical docstring"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(count):
                func(*args, **kwargs)
        return wrapper
    return decorator


class verbose_context(ContextDecorator):
    """typical docstring"""

    def __enter__(self):
        print("class: before function call")
        return self

    def __exit__(self, *exc):
        print("class: after function call")
        return False
