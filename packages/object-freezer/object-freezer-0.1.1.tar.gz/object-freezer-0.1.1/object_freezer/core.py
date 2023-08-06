import collections

__all__ = [
    'ishashable',
    'freeze',
    'deepfrozendict'
]

class UnhashableError(Exception):
    def __init__(self, msg):
        self.msg = msg

def ishashable(obj):
    '''Returns if obj is hashable without modifying it

    Parameters
    ----------
    obj : any
        Python object of any type

    Returns
    -------
    bool
        whether the object is hashable
    '''
    # NOTE: `return isinstance(obj, collections.Hashable)` does not work.
    # e.g. `isinstance((1, [1, 2]), collections.Hashable)` returns `True`,
    # but it is not hashable since it is a hashable type with a *unhashable* element.
    try:
        hash(obj)
    except TypeError:
        return False
    else:
        return True

def freeze(obj, custom_conversions=None):
    '''Convert a object to a hashable

    Parameters
    ----------
    obj : any
        Python object of any type
    custom_conversions : dict
        key is type, value is conversion function. Applied in key order.

    Returns
    -------
    hashable
        Hashable equivalent of the object

    Raises
    ------
    UnhashableError
        When the object cannot be converted to a hashable

    Supported conversion
    - set -> frozenset
    - list -> tuple
    - dict -> deepfrozendict
    '''
    if ishashable(obj):
        ret = obj
    elif isinstance(obj, set):
        # Elements in a set are guaranteed to be hashable.
        ret = frozenset(obj)
    elif isinstance(obj, dict):
        ret = deepfrozendict(obj, custom_conversions=custom_conversions)
    elif isinstance(obj, (list, tuple)):
        ret = tuple(freeze(e) for e in obj)
    elif custom_conversions is not None:
        for otype, conv in custom_conversions.items():
            if isinstance(obj, otype):
                ret = conv(obj)
                break
    else:
        raise UnhashableError('Object {} cannot be converted to a hashable.'.format(repr(obj)))

    if not ishashable(ret):
        raise UnhashableError('Object {} cannot be converted to a hashable.'.format(repr(ret)))

    return ret


# Implementation of deepfrozendict is based on frozendict:
# https://github.com/slezica/python-frozendict

try:
    from collections import OrderedDict
except ImportError:  # python < 2.7
    OrderedDict = NotImplemented

iteritems = getattr(dict, 'iteritems', dict.items) # py2-3 compatibility

class deepfrozendict(collections.Mapping):
    """
    An immutable wrapper around dictionaries that implements the complete :py:class:`collections.Mapping`
    interface. It can be used as a drop-in replacement for dictionaries where immutability is desired.
    """

    dict_cls = dict

    def __init__(self, *args, **kwargs):
        if 'custom_conversions' in kwargs:
            self._custom_conversions = kwargs.pop('custom_conversions')
        else:
            self._custom_conversions = None
        _raw_dict = self.dict_cls(*args, **kwargs)

        # Hopefully this operation does not change hidden property of _raw_dict such as key order...
        self._dict = self.dict_cls({key: freeze(value, custom_conversions=self._custom_conversions) for key, value in _raw_dict.items()})

        self._hash = None

    def __getitem__(self, key):
        return self._dict[key]

    def __contains__(self, key):
        return key in self._dict

    def copy(self, **add_or_replace):
        return self.__class__(self, **add_or_replace)

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self._dict)

    def __hash__(self):
        if self._hash is None:
            h = 0
            for key, value in iteritems(self._dict):
                h ^= hash((key, value))
            self._hash = h
        return self._hash


class FrozenOrderedDict(deepfrozendict):
    """
    A frozendict subclass that maintains key order
    """

    dict_cls = OrderedDict


if OrderedDict is NotImplemented:
    del FrozenOrderedDict
