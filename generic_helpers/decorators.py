class memoize(object):
    """
    'Memoize' decorator.

    Caches a function's return values,
    so that it needn't compute output for the same input twice.

    Use as follows:
    @memoize
    def my_fn(stuff):
        # Do stuff
    """
    def __init__(self, fn):
        self.fn = fn
        self.memocache = {}

    def __call__(self, *args, **kwargs):
        memokey = ( args, tuple( sorted(kwargs.items()) ) )
        if memokey in self.memocache:
            return self.memocache[memokey]
        else:
            val = self.fn(*args, **kwargs)
            self.memocache[memokey] = val
            return val