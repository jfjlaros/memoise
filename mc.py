#!/usr/bin/env python

import shelve
import time


class Cache(object):
    """
    """
    name = 'test.db'
    timeout = 10

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
        key = self.key + str(args + tuple(sorted(kwargs.items())))
        print key
        #now = int(time.time())
        #expiration = now + self.timeout

        #for key in self.cache.iterkeys():
        #    print key
        #    if self.cache[key][0] < now:
        #        print self.cache[key][0]

        if not key in self.cache:
            print "new"
            self.cache[key] = self.func(*args, **kwargs)
            self.cache.sync()
            #self.cache[key] = [expiration, self.func(*args, **kwargs)]
        #else:
        #    print "update"
        #    self.cache[key][0] = expiration

        print "cache"
        return self.cache[key]
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
