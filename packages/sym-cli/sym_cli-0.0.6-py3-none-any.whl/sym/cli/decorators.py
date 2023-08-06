import shlex, subprocess

from functools import wraps
from os import access, get_exec_path, path, X_OK
from subprocess import SubprocessError
from typing import Any, Callable, cast, Iterator, Sequence, TypeVar

from .errors import CliError
from .helpers.config import Config


# Typing support for decorators is still in need of a lot of work:
# https://github.com/python/mypy/issues/3157. So the current grossness
# with casts is unavoidable for now.


F = TypeVar("F", bound=Callable[..., Any])


def run_subprocess(func: Callable[..., Iterator[Sequence[str]]]) -> Callable[..., None]:
    @wraps(func)
    def impl(*args: Any, **kwargs: Any) -> None:
        for command in func(*args, **kwargs):
            try:
                subprocess.run(command, check=True)
            except SubprocessError as err:
                raise CliError(f"Cannot run {shlex.join(command)}") from err

    return impl


# See: https://click.palletsprojects.com/en/7.x/commands/#decorating-commands


def require_bins(*bins: str) -> Callable[[F], F]:
    def decorate(fn: F) -> F:
        @wraps(fn)
        def wrapped(*args, **kwargs):
            exec_path = get_exec_path()
            for binary in bins:
                finder = (
                    True
                    for directory in exec_path
                    if access(path.join(directory, binary), X_OK)
                )
                if not next(finder, False):
                    raise CliError(f"Unable to find {binary} in your path!")
            return fn(*args, **kwargs)

        return cast(F, wrapped)

    return decorate


def require_login(fn: F) -> F:
    @wraps(fn)
    def wrapped(*args, **kwargs):
        config = Config()
        if not config.get("org"):
            raise CliError("run sym login first")
        return fn(*args, **kwargs)

    return cast(F, wrapped)
