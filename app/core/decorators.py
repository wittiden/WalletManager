import functools
from collections.abc import Callable
from typing import Concatenate, ParamSpec, TypeVar

from loguru import logger

T = TypeVar('T')
Self = TypeVar('Self')
P = ParamSpec('P')


def debug_log(func: Callable[Concatenate[Self, P], T]) -> Callable[Concatenate[Self, P], T]:
    @functools.wraps(func)
    def wrapped(self: Self, *args: P.args, **kwargs: P.kwargs) -> T:
        logger.debug('start - {}', func.__name__)
        result = func(self, *args, **kwargs)
        logger.debug('end - {}', func.__name__)
        return result

    return wrapped


def info_log(strat_info: str | None, end_info: str | None) -> Callable[Concatenate[Self, P], T]:
    def wrapper(func: Callable[Concatenate[Self, P], T]) -> T:
        @functools.wraps(func)
        def wrapped(self: Self, *args: P.args, **kwargs: P.kwargs) -> T:
            if strat_info is not None:
                logger.info(strat_info)
            result = func(self, *args, **kwargs)
            if end_info is not None:
                logger.info(end_info)
            return result

        return wrapped

    return wrapper
