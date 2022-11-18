import asyncio

from loguru import logger
from functools import wraps, partial


def restart_on_failure(func):
    """
    Restart the function on failure
    """

    @wraps(func)
    async def run(*args):
        while True:
            try:
                await func(*args)
            except Exception as e:
                logger.error(e)

    return run


def to_async(func):
    """
    Convert a synchronous function to an asynchronous function
    """

    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


def round_by(x, base, scaler: float = 1e4):
    """
    Round the number x by increment of base
    """
    x *= scaler
    base *= scaler
    x_rounded = base * round(x / base)

    return x_rounded / scaler
