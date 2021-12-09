"""typical docstring"""

from contextlib import contextmanager


class Indenter():
    """typical docstring"""

    def __init__(self, indent_str: str = " " * 4, indent_level: int = 0):
        """typical docstring"""
        self._indent_str = indent_str
        self._indent_level = indent_level - 1

    @contextmanager
    def print(self, message: str):
        """typical docstring"""
        print(self._indent_str * self._indent_level + message)

    def inclev(self):
        """typical docstring"""
        self._indent_level += 1

    def declev(self):
        """typical docstring"""
        self._indent_level -= 1

    def __enter__(self):
        """docstring"""
        self.inclev()
        return self

    def __exit__(self, *exc):
        """docstring"""
        self.declev()
        return self
