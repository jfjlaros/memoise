#!/usr/bin/env python

from memoise.memoise import Cache
import time

def fib(n):
    if n < 2:
        return n

    return fib(n - 1) + fib(n - 2)
#fib

@Cache()
def fib_c(n):
    if n < 2:
        return n

    return fib_c(n - 1) + fib_c(n - 2)
#fib_c

def benchmark(n):
    start = time.time()
    result = fib(n)
    print "fib(%i) took %f seconds with result %i" % (n, time.time() - start,
        result)
    start = time.time()
    result = fib_c(n)
    print "fib_c(%i) took %f seconds with result %i" % (n, time.time() - start,
        result)
#benchmark

benchmark(33)
