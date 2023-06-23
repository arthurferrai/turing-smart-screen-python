from functools import wraps


class SpyFunction:
    def __call__(self, *args, **kwargs): ...
    called = False


def spy_call(f) -> SpyFunction:
    @wraps(f)
    def inner(*args, **kwargs):
        inner.called = True
        return f(*args, **kwargs)
    inner.called = False
    return inner
