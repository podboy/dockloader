# coding:utf-8

from typing import Optional
from typing import Sequence

from xkits import add_command
from xkits import argp
from xkits import commands
from xkits import run_command

from ..attribute import __description__
from ..attribute import __project__
from ..attribute import __urlhome__
from ..attribute import __version__
from .config import add_cmd_config
from .images import add_cmd_pull
from .images import add_cmd_transport


@add_command(__project__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_config, add_cmd_pull, add_cmd_transport)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(root=add_cmd, argv=argv, description=__description__,
                    epilog=f"For more, please visit {__urlhome__}.")
