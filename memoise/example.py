#!/usr/bin/env python

from memoise.memoise import Cache

@Cache()
def add(a, b, x=1, opt=0):
    return a + b + x + opt

@Cache(timeout=10)
def subst(a, b):
    return a - b

print add(12, 4, x=1, opt=1)
print add(12, 4, opt=1, x=1)
print add(12, 4)
print subst(12, 4)
print subst(12, 4)
