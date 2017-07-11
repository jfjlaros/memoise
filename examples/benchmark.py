#!/usr/bin/env python

import time

from memoise import Cache


def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@Cache()
def fib_c(n):
    if n < 2:
        return n
    return fib_c(n - 1) + fib_c(n - 2)


def benchmark(n):
    start = time.time()
    result = fib(n)
    print "fib({}) took {} seconds with result {}".format(
        n, time.time() - start, result)
    start = time.time()
    result = fib_c(n)
    print "fib_c({}) took {} seconds with result {}".format(
        n, time.time() - start, result)


def main():
    benchmark(33)


if __name__ == '__main__':
    main()
