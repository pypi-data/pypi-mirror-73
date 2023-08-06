from pprint import pprint


def printout(func):
    def wrapper(*args, **kw):
        print('--------------------------')
        print(f'Function: {func.__name__}:')
        print('--------------------------')
        print(f'Return value:')
        print('--------------------------')
        rv = func(*args, **kw)
        pprint(rv)
        print('--------------------------')
        return rv
    return wrapper


