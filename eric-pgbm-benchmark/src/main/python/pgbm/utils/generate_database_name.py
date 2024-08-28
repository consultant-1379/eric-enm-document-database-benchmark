"""
Module containing function that generates a random string id of 5 characters
in length, containing a mix of upper case letters and numbers.

Function
--------
id_generator(chars=string.ascii_uppercase + string.digits):
    Function that imports the 'random' module that provides random generation.
    Returns a concatenated list of 5 uppercase ASCII chars and digits.
"""
import string
from random import choice


def id_generator(chars=string.ascii_uppercase + string.digits):
    return ''.join(choice(chars) for _ in range(5))
