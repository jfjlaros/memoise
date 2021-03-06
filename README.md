# Memoisation
*[Memoisation](https://en.wikipedia.org/wiki/Memoization) is an optimization
technique used primarily to speed up computer programs by storing the results
of expensive function calls and returning the cached result when the same
inputs occur again.* -- Wikipedia

This memoisation implementation uses a memory object caching system to return
the result of previous function calls. A *decorator* is used to enable this per
function. Apart from this basic functionality, this library offers the
following:

- Configurable retention time of cached results.
- Per function list of formal parameters to ignore, this can be useful when
  working with references.
- Results are cached using a hash of the following information as key:
  - An optional key.
  - The name of the module,
  - The name of the function.
  - The type and name of every parameter.
  - The value of non-ignored parameters.

## Installation
First install the dependencies:

    apt-get install memcached libmemcached-dev

Via Pypi:

    pip install memoise

Installation from source:

    git clone https://github.com/jfjlaros/memoise.git
    cd memoise
    pip install .

## Usage
First import the `Cache` class from the library:

```python
from memoise import Cache
```

Use the `@Cache()` decorator to enable memoisation for a specific function. The
decorator accepts the following optional arguments:

- `timeout`: Retention time of cached results in seconds.
- `ignore`: List of formal parameter positions and keywords to ignore.
- `key`: Prefix of the key under which the cached result is stored.


### Examples
Suppose we have the following function that calculates the `n`-th Fibonacci
number:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Even for modest inputs, this implementation will be slow because of the
repeated calculation of the same numbers. To illustrate, calculating `fib(33)`,
requires 11,405,773 function calls to be made.

The performance of this can be improved upon by *caching* the results with the
`@Cache()` decorator as follows:

```python
@Cache()
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```

Now only 34 function calls are made, which significantly speeds up the
calculation.

Parameters can be ignored by using the `ignore` keyword:

```python
@Cache(ignore=['a', 'd'])
def f(a, b, c=2, d=3)
    print a, d
    return b + c
```
