import click
import subprocess

from awscli.completer import Completer as AwsCompleter
from ec2 import EC2


# Need invoke_without_commands=True because need to call --all-commands
# without any command.
@click.group(invoke_without_command=True)
@click.option(
    "--all-commands", is_flag=True, help="List all known commands.",
)
def cli(all_commands):
    if all_commands:
        for cmd in AwsCompleter().complete("aws", 3):
            click.echo(cmd)


@cli.command()
@click.option(
    "--attrib",
    default=["PrivateIpAddress"],
    show_default=True,
    multiple=True,
    help="One or multiple attributes to show",
)
@click.option(
    "--limit",
    default=0,
    show_default=True,
    help="Limit the number of results that get shown. 0 means no limit.",
)
@click.option(
    "--output",
    type=click.Choice(["json", "table", "text"], case_sensitive=False),
    default="text",
    show_default=True,
    help="The formatting style for command output.",
)
@click.option("--tag-key", default="Name", show_default=True)
@click.option("--tag-value")
def ec2(*args, **kwargs):
    # print(args)
    # print(kwargs)
    EC2(*args, **kwargs).run()


if __name__ == "__main__":
    cli()
