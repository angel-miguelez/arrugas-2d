# -*- coding: utf-8 -*-

class Singleton(type):
    """
    Class to hold just one instance of every other class which makes use of this pattern
    """

    # Map from class to class instance
    _instances = {}

    def __call__(cls, *args, **kwargs):

        # If the class has not an instance yet, create it
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        # Return the instance of the class
        return cls._instances[cls]
