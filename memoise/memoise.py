#!/usr/bin/env python

import pylibmc

class Cache(object):
    """
    Memoisation method with the following properties:

    - Easy to enable per function via a decorator.
    - The module, function name and the arguments are used as key.
    - The retention time can be altered via the decorator.
    """
    host = "127.0.0.1"
    port = "11211"

    def __init__(self, timeout=86400, ignore=[], hash=[], key=""):
        """
        Constructor.

        @arg name: File name of the persistent object database.
        @type name: str
        @arg refresh: Timeout for unused entries.
        @type refresh: int
        @arg timeout: Timeout for used entries.
        @type timeout: int
        @arg ignore: List of positions of parameters and keywords to ignore.
        @type ignore: list
        @arg ignore: List of positions of parameters and keywords to hash.
        @type ignore: list
        @arg key: Prefix for generating the key.
        @type key: str
        """
        self.cache = pylibmc.Client(["%s:%s" % (self.host, self.port)])
        self.timeout = timeout
        self.ignore = ignore
        self.hash = hash
        self.key = key
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
            ignored_args = []
            other_args = []

            for i in range(len(args)):
                if i not in self.ignore:
                    if i in self.hash:
                        other_args.append((type(args[i]).__name__,
                            hash(args[i])))
                    else:
                        other_args.append((type(args[i]).__name__, args[i]))
                #if
                else:
                    ignored_args.append(type(args[i]).__name__)
            #for
            for i in sorted(kwargs.items()):
                if i[0] not in self.ignore:
                    if i in self.hash:
                        other_args.append((type(i[1]).__name__, i[0],
                            hash(i[1])))
                    else:
                        other_args.append((type(i[1]).__name__, i[0], i[1]))
                #if
                else:
                    ignored_args.append((type(i[1]).__name__, i[0]))
            #for

            key = ("%s_%s.%s%s" % (self.key, func.__module__, func.func_name,
                str(tuple(ignored_args + other_args)))).encode("hex")

            result = self.cache.get(key)
            if not result:
                result = func(*args, **kwargs)

                self.cache.add(key, result, time=self.timeout)
            #if

            return result
        #wrapper

        return wrapper
    #__call__
#Cache
