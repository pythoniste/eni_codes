"""Example using meta-classes"""

import types
from time import time


class Timer(type):
    """This class allow to make every method of the class print their execution time"""

    def __new__(mcs, name, bases, dct):
        """Override the __new__ method to change the class methods on the fly"""

        def wrapper(method_name, method):
            """Define a new method that will replace the original one"""

            def timeit(self, *args, **kwargs):
                """This is the final method that will replace the method"""

                # register the time before calling the original method
                t = time()
                # calling the original method
                result = method(self, *args, **kwargs)
                # comparing the actual time to the one registered to get the duration of the original method call
                print(f"Appel de {method_name}:\t{time() - t}")
                # returning the result of the method
                return result

            # changing the metadata of the new method, so it match the original one.
            timeit.__name__ = method.__name__
            timeit.__doc__ = method.__doc__
            timeit.__dict__ = method.__dict__

            # return the new method
            return timeit

        d = {}
        for item_name, item_slot in dct.items():
            # we iterate over all item of the class
            if type(item_slot) is types.FunctionType:
                # if the item is a method, we replace it using the wrapper
                d[item_name] = wrapper(item_name, item_slot)
            else:
                # else, we change noting
                d[item_name] = item_slot

        # Now, we are building our class with all its method being timed.
        return type.__new__(mcs, name, bases, d)
