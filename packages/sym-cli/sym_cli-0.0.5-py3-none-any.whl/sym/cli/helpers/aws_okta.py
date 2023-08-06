from typing import Final, Iterator, Tuple

from ..decorators import require_bins, run_subprocess
from ..errors import CliError
from .params import get_profile


class AwsOkta:
    __slots__ = ["resource"]

    resource: Final[str]

    def __init__(self, resource: str) -> None:
        self.resource = resource

    @run_subprocess
    @require_bins("aws-okta")
    def exec(self, *args: str, **kwargs: str) -> Iterator[Tuple[str, ...]]:
        try:
            profile = get_profile(self.resource)
        except KeyError:
            raise CliError(f"Invalid resource: {self.resource}")
        options = [
            arg
            for (key, value) in kwargs.items()
            for arg in ("--" + key.replace("_", "-"), value)
        ]
        yield "aws-okta", "exec", "-r", profile.arn, "--", *args, *options
