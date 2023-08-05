"""Main module."""

from collections.abc import Iterable

try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass

from itertools import tee

def _iterable(obj):
    '''
    Is obj iterable?
    '''
    return isinstance(obj, Iterable)

def _pairwise(iterable):
    '''
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    '''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

def popsingleton(
    container,
    catch_empty=False,
    catch_overfull=False,
    default=None,
):
    '''
    Extract the value of a single-element iterator.
    Raise exceptions or return default value if iterator is not single-element.
    '''
    try:
        res, = container
        return res
    except ValueError:
        if not _iterable(container):
            raise TypeError(container, 'is not iterable')
        elif container and not catch_overfull:
            raise ValueError(container, 'is overfull')
        elif not container and not catch_empty:
            raise ValueError(container, 'is empty')

        return default



def pophomogeneous(
    container,
    catch_empty=False,
    catch_heterogeneous=False,
    default=None,
):
    '''
    Extract the value of a homogeneous iterator.
    Raise exceptions or return default value if iterator is not homogeneous.
    '''

    handle1, handle2 = tee(container)
    res = default

    if not _iterable(handle1):
        raise TypeError(handle1, 'is not iterable')
    elif not container and not catch_empty:
        raise ValueError(handle1, 'is empty')
    elif container and all(
        a == b
        for a, b in _pairwise(handle1)
    ):
        res = next(handle2)
    elif container and not catch_heterogeneous:
        raise ValueError(handle1, 'is heterogeneous')

    return res
