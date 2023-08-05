import click

from subprocess import CalledProcessError

from .version import __version__
from .aws_okta import aws_okta_exec
from .errors import CliError


@click.group()
def sym():
    """Access resources managed by Sym workflows.

    Use these tools to work with your resources once you've gotten approval in
    Slack.
    """
    pass


@sym.command(short_help="print the version")
def version():
    click.echo(__version__)


@sym.command(short_help="ssh to an ec2 instance")
@click.argument("resource")
@click.option("--target", help="target instance id", metavar="<instance-id>")
def ssh(target, resource):
    """Use approved creds for RESOURCE to ssh to an ec2 instance"""
    # TODO boto ssm start-session
    click.echo(f"SSH: {resource}")


@sym.command("exec", short_help="execute a command")
@click.argument("resource")
@click.argument("command", nargs=-1)
def sym_exec(resource, command):
    """Use approved creds for RESOURCE to execute COMMAND"""
    try:
        out = aws_okta_exec(resource, list(command))
        click.echo(out)
    except CliError as err:
        click.echo(err)
