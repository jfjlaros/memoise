#!/usr/bin/env python

import pylibmc
import pickle

class Cache(object):
    """
    Memoisation method with the following properties:

    - Easy to enable per function via a decorator.
    - The module, function name and the arguments are used as key.
    - The retention time can be altered via the decorator.
    """
    host = "127.0.0.1"
    port = "11211"

    def __init__(self, timeout=86400, ignore=0):
        """
        Constructor.

        @arg name: File name of the persistent object database.
        @type name: str
        @arg refresh: Timeout for unused entries.
        @type refresh: int
        @arg timeout: Timeout for used entries.
        @type timeout: int
        @arg ignore: Ignore the first {ignore} amount of variables.
        @type ignore: int
        """
        self.cache = pylibmc.Client(["%s:%s" % (self.host, self.port)])
        self.timeout = timeout
        self.ignore = ignore
    #__init__

    def __call__(self, func):
        """
        Entry point.

        @arg func: A function.
        @type func: function
        """
        def wrapper(*args, **kwargs):
            """
            Wrapper function that does cache administration.
            """
            i_args = map(lambda x: type(x).__name__, args[:self.ignore])
            o_args = map(lambda x: (type(x).__name__, x), args[self.ignore:])
            k_args = map(lambda x: (type(x[1]).__name__, x[0], x[1]),
                sorted(kwargs.items()))

            key = ("%s.%s%s" % (func.__module__, func.func_name,
                str(args[self.ignore:] +
                tuple(sorted(kwargs.items()))))).encode("hex")
            print key.decode("hex")

            print i_args + o_args + k_args
            print pickle.dumps(args[0])

            if not self.cache.get(key):
                self.cache.add(key, func(*args, **kwargs), time=self.timeout)

            return self.cache.get(key)
        #wrapper

        return wrapper
    #__call__
#Cache
