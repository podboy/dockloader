# coding:utf-8

import os

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from .parser import TagConfigFile

DEFAULT_CONFIG_FILE = os.path.join("cfgs", "docker.io")


@add_command("config", description="list configuration file")
def add_cmd_config(_arg: argp):
    _arg.add_argument("-f", "--config-file", dest="config_file", type=str,
                      help="the configuration file", nargs=1,
                      default=[DEFAULT_CONFIG_FILE], metavar="FILE")


@run_command(add_cmd_config)
def run_cmd_config(cmds: commands) -> int:
    config_file: str = cmds.args.config_file[0]
    for tag in TagConfigFile(config_file):
        cmds.stdout(tag.name)
    return 0
