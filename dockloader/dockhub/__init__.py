# coding:utf-8

from typing import Optional
from typing import Sequence

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from ..attribute import __url_home__
from ..attribute import __version__
from .tags import add_cmd_tags


@add_command("dockhub")
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_tags)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description="docker hub toolkit",
        epilog=f"For more, please visit {__url_home__}.")
