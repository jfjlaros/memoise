#!/usr/bin/env python

import shelve
import time

class Cache(object):
    """
    Memoisation method with the following properties:

    - Easy to enable per function via a decorator.
    - The module, function name and the arguments are used as key.
    - Timeout based on last use.
    - Maximum retention time, independent of last use.
    - Both timeout and retention time can be altered in the decorator.
    - The cache is synchronised to a file on disk (shelve).
    """
    def __init__(self, name="test.db", refresh=2, timeout=5):
        """
        Constructor.

        @arg name: File name of the persistent object database.
        @type name: str
        @arg refresh: Timeout for unused entries.
        @type refresh: int
        @arg timeout: Timeout for used entries.
        @type timeout: int
        """
        self.cache = shelve.open(name)
        self.refresh = refresh
        self.timeout = timeout
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
            now = int(time.time())
            refresh = now + self.refresh
            timeout = now + self.timeout

            # Purge timed out entries.
            for key in self.cache:
                if self.cache[key][0] < now or self.cache[key][1] < now:
                    del self.cache[key]

            key = "%s.%s%s" % (func.__module__, func.func_name,
                str(args + tuple(sorted(kwargs.items()))))
            if key in self.cache:       # Refresh the entry.
                entry = self.cache[key] # Use this instead of writeback.
                entry[0] = refresh
                self.cache[key] = entry
            #if
            else:                       # Add a new entry.
                self.cache[key] = [refresh, timeout, func(*args, **kwargs)]
            self.cache.sync()

            return self.cache[key][2]
        #wrapper

        return wrapper
    #__call__
#Cache