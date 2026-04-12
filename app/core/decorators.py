import functools
from typing import Callable, TypeVar, ParamSpec, Concatenate, Any
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


def info_log(info: list[Any]) -> Callable[Concatenate[Self, P], T]:
    def wrapper(func: Callable[Concatenate[Self, P], T]) -> T:
        @functools.wraps(func)
        def wrapped(self: Self, *args: P.args, **kwargs: P.kwargs) -> T:
            logger.info(info[0])
            result = func(self, *args, **kwargs)
            logger.info(info[-1])
            return result
        return wrapped
    return wrapper