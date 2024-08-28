"""
Module containing the 'Threshold' class, allowing for defining of a new
threshold with a name, description, minimum and maximum.

Class
-----
Threshold:
    Class to create a 'Threshold' object, with variables name, description,
    minimum and maximum.

Class Methods
-------------
_init_(self, name, description, minimum=None, maximum=None):
    Method that is called every time an object is created from this class.
    Allows passing of args for name, description, minimum and maximum.

name(self):
    Returns a value for 'name' of a Threshold object.

description(self):
    Returns a value for 'description' of a Threshold object.

minimum(self):
    Returns a value for 'minimum' of a Threshold object.

maximum(self):
    Returns a value for 'maximum' of a Threshold object.

__repr__(self):
    Returns a string representation of a Threshold object.
"""
import logging

logger = logging.getLogger(__name__)


class Threshold:
    def __init__(self, name, description, minimum=None, maximum=None):
        self._name = name
        self._description = description

        if minimum is not None and maximum is not None:
            logger.error("Both Minimum and Maximum thresholds found "
                         f"for {self._name}")
            raise ValueError("Only one requirement allowed for Threshold, "
                             "either minimum or maximum")

        if minimum is None and maximum is None:
            logger.error(f"Neither Minimum or Maximum threshold found "
                         f"for {self._name}")
            raise ValueError("At least one value must be set for minimum or "
                             "maximum")

        self._minimum = minimum
        self._maximum = maximum

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    def __repr__(self):
        return f'Threshold({self.name},{self.description},' \
               f'{self.minimum if self.minimum is not None else self.maximum})'
