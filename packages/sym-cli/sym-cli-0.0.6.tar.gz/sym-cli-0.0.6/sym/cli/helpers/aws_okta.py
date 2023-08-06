from typing import Final, Iterator, Tuple

import subprocess

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

        base_profile = self.get_base_okta_profile()

        yield "aws-okta", "exec", base_profile, "-r", profile.arn, "--", *args, *options

    def get_base_okta_profile(self) -> str:
        result = subprocess.run("aws-okta list | sed -n 2p | awk '{print $1}'",
                capture_output=True, shell=True, text=True)
        output = result.stdout.rstrip()
        if result.returncode != 0 or not output:
            raise CliError("Please run aws-okta login to configure your Okta credentials!")
        return output
