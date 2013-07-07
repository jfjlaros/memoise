#!/usr/bin/env python

import shelve
import time

class Cache(object):
    """
    """
    name = 'test.db'
    refresh = 2
    timeout = 5

    def __init__(self, func):
        """
        """
        self.func = func
        self.key = "%s.%s" % (func.__module__, func.func_name)
        self.cache = shelve.open(self.name)
    #__init__

    def __call__(self, *args, **kwargs):
        """
        """
        now = int(time.time())
        refresh = now + self.refresh
        timeout = now + self.timeout

        # Purge timed out entries.
        for key in self.cache:
            if self.cache[key][0] < now or self.cache[key][1] < now:
                del self.cache[key]

        # Update the cache.
        key = self.key + str(args + tuple(sorted(kwargs.items())))
        if key in self.cache:       # Refresh the entry.
            entry = self.cache[key] # Use this instead of writeback.
            entry[0] = refresh
            self.cache[key] = entry
        #if
        else:                       # Add a new entry.
            print "new"
            self.cache[key] = [refresh, timeout, self.func(*args, **kwargs)]
        self.cache.sync()

        return self.cache[key][2]
    #__call__
#Cache

def f():
    pass

@Cache
def add(a, b, x=1, opt=0):
    return a + b + x + opt

@Cache
def subst(a, b):
    return a - b

print add(12, 4, x=1, opt=1)
print add(12, 4, opt=1, x=1)
print add(12, 4)
print subst(12, 4)
print subst(12, 4)
