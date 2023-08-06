import asyncio
import functools
from typing import Coroutine, Callable


async def async_wrap(hub, func: Callable, *args, **kwargs) -> Coroutine:
    """
    Wrap a serial call so that it becomes async if configuration allows
    """
    if (
        hub.OPT.idem.wrap_serial_calls
        and not asyncio.iscoroutinefunction(func)
        and not hub.OPT.idem.session_backend.startswith("aio")
    ):
        hub.log.trace(f"Wrapping serial call with async: {func.__name__}")
        ret = hub.pop.Loop.run_in_executor(
            None, functools.partial(func, *args, **kwargs)
        )
    else:
        ret = func(*args, **kwargs)

    if asyncio.iscoroutine(ret) or asyncio.isfuture(ret):
        ret = await ret

    return ret
