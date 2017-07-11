"""Tests for the memoise library.
"""
import time

from memoise import Cache


def inc():
    """Function with a static variable.
    """
    if not hasattr(inc, 'x'):
        inc.x = 0
    inc.x += 1

    return inc.x


@Cache()
def cached_inc():
    """Function with a static variable.
    """
    if not hasattr(cached_inc, 'x'):
        cached_inc.x = 0
    cached_inc.x += 1

    return cached_inc.x


@Cache(ignore=['a'])
def add(a, b):
    return a + b


@Cache(ignore=['a', 'd'])
def f(a, b, c=2, d=3):
    return '{} {} {} {}'.format(a, b, c, d)


@Cache(timeout=2)
def current_time():
    return time.time()


class TestLibrary(object):
    def setup(self):
        Cache().flush()

    def test_normal(self):
        # Normal for a function with a static variable.
        assert inc() == 1
        assert inc() == 2

    def test_cached(self):
        # Normal for a function with a static variable.
        assert cached_inc() == 1
        assert cached_inc() == 1

    def test_kwargs_1(self):
        assert f(0, 1) == '0 1 2 3'

    def test_kwargs_2(self):
        assert f(0, 1, 2, 3) == '0 1 2 3'

    def test_kwargs_3(self):
        assert f(0, 1, d=3, c=2) == '0 1 2 3'

    def test_kwargs_4(self):
        assert f(d=3, c=2, b=1, a=0) == '0 1 2 3'

    def test_ignore_1(self):
        assert add(1, 2) == 3
        assert add(2, 2) == 3

    def test_ignore_2(self):
        assert f(0, 1) == '0 1 2 3'
        assert f(1, 1) == '0 1 2 3'

    def test_ignore_3(self):
        assert f(0, 1, 2, 3) == '0 1 2 3'
        assert f(0, 1, d=1, c=2) == '0 1 2 3'

    def test_timeout_1(self):
        g_old = current_time()
        time.sleep(0.1)
        assert g_old == current_time()

    def test_timeout_2(self):
        g_old = current_time()
        time.sleep(2.1)
        assert g_old != current_time()
