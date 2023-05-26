import time
from functools import wraps


def async_timeit(method):
    @wraps(method)
    async def timed(self, *args, **kw):
        ts = time.time()
        result = await method(self, *args, **kw)
        te = time.time()
        elapsed = te - ts
        self.logger.info(f"{method.__name__} took: {elapsed:2.2f} sec")
        return result

    return timed
