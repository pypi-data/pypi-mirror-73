import click

from typing import Tuple

from .version import __version__
from .helpers.aws_okta import AwsOkta
from .helpers.config import Config
from .helpers.params import get_profiles, PARAMS
from .decorators import require_bins, require_login
from .errors import CliError


@click.group()
def sym() -> None:
    """Access resources managed by Sym workflows.

    Use these tools to work with your resources once you've gotten approval in
    Slack.
    """
    pass


@sym.command(short_help="print the version")
def version() -> None:
    click.echo(__version__)


@sym.command(short_help="login to your sym account")
@click.option("--org", help="org slug", prompt=True)
def login(org: str) -> None:
    """Link your Sym account"""
    if org not in PARAMS:
        raise CliError(f"Invalid org: {org}")
    config = Config()
    config["org"] = org


@sym.command(short_help="list available resource groups")
@require_login
def resources() -> None:
    """List resource groups available for use"""
    for (slug, profile) in get_profiles().items():
        click.echo(f"{slug} ({profile.display_name})")


@sym.command(short_help="ssh to an ec2 instance")
@click.argument("resource")
@click.option(
    "--target", help="target instance id", metavar="<instance-id>", required=True
)
@require_bins("session-manager-plugin")
@require_login
def ssh(resource: str, target: str) -> None:
    """Use approved creds for RESOURCE to ssh to an ec2 instance"""
    AwsOkta(resource).exec("aws", "ssm", "start-session", target=target)


@sym.command("exec", short_help="execute a command")
@click.argument("resource")
@click.argument("command", nargs=-1)
@require_login
def sym_exec(resource: str, command: Tuple[str, ...]) -> None:
    """Use approved creds for RESOURCE to execute COMMAND"""
    AwsOkta(resource).exec(*command)
