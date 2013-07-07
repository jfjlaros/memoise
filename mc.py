#!/usr/bin/env python

import shelve
import time

class Cache(object):
    """
    """
    def __init__(self, name="test.db", refresh=2, timeout=5):
        """
        """
        self.cache = shelve.open(name)
        self.refresh = refresh
        self.timeout = timeout
    #__init__

    def __call__(self, func):
        """
        """
        def wrapper(*args, **kwargs):
            """
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

def f():
    pass

@Cache()
def add(a, b, x=1, opt=0):
    return a + b + x + opt

@Cache(refresh=3, timeout=10)
def subst(a, b):
    return a - b

print add(12, 4, x=1, opt=1)
print add(12, 4, opt=1, x=1)
print add(12, 4)
print subst(12, 4)
print subst(12, 4)
