import pylibmc


class Cache(object):
    """Memoisation method with the following properties:

    - Easy to enable per function via a decorator.
    - The module, function name and the arguments are used as key.
    - The retention time can be altered via the decorator.
    """
    host = '127.0.0.1'
    port = '11211'

    def __init__(self, timeout=86400, ignore=[], hash=[], key=''):
        """Constructor.

        :arg str name: File name of the persistent object database.
        :arg int refresh: Timeout for unused entries.
        :arg int timeout: Timeout for used entries.
        :arg list ignore: List of positions of parameters and keywords to ignore.
        :arg list ignore: List of positions of parameters and keywords to hash.
        :arg str key: Prefix for generating the key.
        """
        self.cache = pylibmc.Client(['{}:{}'.format(self.host, self.port)])
        self.timeout = timeout
        self.ignore = ignore
        self.hash = hash
        self.key = key

    def __call__(self, func):
        """Entry point.

        :arg function func: A function.
        """
        def wrapper(*args, **kwargs):
            """Wrapper function that does cache administration.
            """
            ignored_args = []
            other_args = []

            for i in range(len(args)):
                if i not in self.ignore:
                    if i in self.hash:
                        other_args.append(
                            (type(args[i]).__name__, hash(args[i])))
                    else:
                        other_args.append((type(args[i]).__name__, args[i]))
                else:
                    ignored_args.append(type(args[i]).__name__)

            for i in sorted(kwargs.items()):
                if i[0] not in self.ignore:
                    if i in self.hash:
                        other_args.append(
                            (type(i[1]).__name__, i[0], hash(i[1])))
                    else:
                        other_args.append((type(i[1]).__name__, i[0], i[1]))
                else:
                    ignored_args.append((type(i[1]).__name__, i[0]))

            key = (
                '{}_{}.{}{}'.format(
                    self.key, func.__module__, func.func_name,
                    str(tuple(ignored_args + other_args)))
            ).encode('hex')

            result = self.cache.get(key)
            if not result:
                result = func(*args, **kwargs)
                self.cache.add(key, result, time=self.timeout)

            return result

        return wrapper
