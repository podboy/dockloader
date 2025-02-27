# coding:utf-8

from xkits import add_command
from xkits import argp
from xkits import cmds
from xkits import commands
from xkits import run_command

from ..utils import DockerHubTags


def list_tags(generate: bool):
    for image in cmds.args.images:
        tags = DockerHubTags.fetch(image)
        if generate:
            cmds.stdout(f"# {tags.website}")
        for tag in tags.values():
            cmds.stdout(tag.name if generate else tag.tag_name)


def add_pos_images(_arg: argp, help: str):
    _arg.add_argument(type=str, dest="images", help=help,
                      nargs="*", default=[], metavar="IMAGE")


@add_command("list", help="list docker hub image all tags")
def add_cmd_list(_arg: argp):
    add_pos_images(_arg, "image name")


@run_command(add_cmd_list)
def run_cmd_list(cmds: commands) -> int:
    list_tags(generate=False)
    return 0


@add_command("generate", help="generate docker hub image all tags")
def add_cmd_generate(_arg: argp):
    add_pos_images(_arg, "image name")


@run_command(add_cmd_generate)
def run_cmd_generate(cmds: commands) -> int:
    list_tags(generate=True)
    return 0


@add_command("tags", help="docker hub image additional name")
def add_cmd_tags(_arg: argp):
    pass


@run_command(add_cmd_tags, add_cmd_list, add_cmd_generate)
def run_cmd_tags(cmds: commands) -> int:
    return 0
