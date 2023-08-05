import subprocess

from .errors import CliError


def aws_okta_exec(profile, subcommand):
    check_aws_okta()
    # TODO using subprocess.popen and communicate would let you stream to
    # stdout/err
    result = subprocess.run(
        ["aws-okta", "exec", profile, "--"] + subcommand, text=True, capture_output=True
    )
    if result.returncode != 0:
        raise CliError(result.stderr)
    return result.stdout


def check_aws_okta():
    result = subprocess.run(["which", "aws-okta"], capture_output=True)
    if result.returncode != 0:
        raise CliError("Unable to find aws-okta in your path!")
