"""
Basic utilities.

attrdict is a subclass of dict which allows most items to be accessed
as attributes.  This is similar to a Javascript object, though it requires
more care in python.  If you use keys that are parts of the dict
mplementation, you may get burned.  On the other hand, being able to look
up dict elements with . is a huge improvement over [''].

    >>> foo = attrdict(bar=1)
    >>> foo.bar == foo['bar']
    True

"""

# load a fast JSON lib if possible
try:
    import jsonlib2 as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            import simplejson as json
        except ImportError:
            print >>sys.stderr, 'Unable to import any JSON library'
            raise

# this is modified from the ASPN version to avoid a cyclic reference:
#  see  http://www.mail-archive.com/python-bugs-list@python.org/msg06508.html
# from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/361668
class attrdict(dict):
    """A dict whose items can also be accessed as member variables.

    >>> d = attrdict(a=1, b=2)
    >>> d['c'] = 3
    >>> print d.a, d.b, d.c
    1 2 3
    >>> d.b = 10
    >>> print d['b']
    10

    # but be careful, it's easy to hide methods
    >>> print d.get('c')
    3
    >>> d['get'] = 4
    >>> print d.get('a')
    Traceback (most recent call last):
    TypeError: 'int' object is not callable
    """
    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

