# coding:utf-8

from argparse import FileType
from io import TextIOWrapper
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from .attribute import __description__
from .attribute import __project__
from .attribute import __url_home__
from .attribute import __version__
from .client import DockerClient
from .config import add_cmd_config
from .parser import Tag
from .parser import TagConfig


def filter_tags(tags: Sequence[Tag]) -> Tuple[Tag, ...]:
    names: List[str] = []
    for tag in tags:
        if tag.name not in names:
            names.append(tag.name)
    return tuple(tag.parse(name) for name in names)


@add_command("pull", description="pull image")
def add_cmd_pull(_arg: argp):
    _arg.add_opt_on("-a", "--all-tags", dest="all_tags",
                    help="pull all image tags")
    _arg.add_argument("-f", "--config-file", dest="config_file", type=str,
                      help="the configuration file for pulling images",
                      nargs=1, default=[], metavar="FILE")
    _arg.add_argument(type=str, dest="images", help="the name for pulling",
                      nargs="*", default=[], metavar="IMAGE")


@run_command(add_cmd_pull)
def run_cmd_pull(cmds: commands) -> int:
    images_tag: List[Tag] = [Tag.parse(image) for image in cmds.args.images]
    if len(cmds.args.config_file) > 0:
        config_file: str = cmds.args.config_file[0]
        for tag in TagConfig(config_file):
            images_tag.append(tag)

    cmds.logger.info("Pulling images:")
    for tag in filter_tags(images_tag):
        if cmds.args.all_tags:
            cmds.logger.info(f"\t{tag.name_without_tag} all tags")
            DockerClient().pull_all_tags(tag.name_without_tag)
        else:
            cmds.logger.info(f"\t{tag.name}")
            DockerClient().pull(tag.name)
    return 0


@add_command("transport", description="transport image")
def add_cmd_transport(_arg: argp):
    _arg.add_argument("-r", "--registry", dest="registry", type=str,
                      help="the new registry for transporting images",
                      nargs=1, default=["ghcr.io"], metavar="REGISTRY")
    _arg.add_argument("-n", "--namespace", dest="namespace", type=str,
                      help="the new namespace for transporting images",
                      nargs=1, default=["podboy"], metavar="NAMESPACE")
    _arg.add_argument("-f", "--file", dest="images_file",
                      type=FileType("r", encoding="UTF-8"),
                      help="the file for transporting images",
                      nargs=1, metavar="FILE")
    _arg.add_argument(type=str, dest="images",
                      help="the name for transporting",
                      nargs="*", default=[], metavar="IMAGE")


@run_command(add_cmd_transport)
def run_cmd_transport(cmds: commands) -> int:
    images: List[str] = cmds.args.images
    if cmds.args.images_file is not None:
        images_file: TextIOWrapper = cmds.args.images_file[0]
        for line in images_file:
            images.append(line.strip())
    images_tag: List[Tag] = [Tag.parse(image) for image in images]
    registry: List[str] = cmds.args.registry[0]
    namespace: List[str] = cmds.args.namespace[0]
    cmds.logger.info(f"Transporting images to {registry}/{namespace}:")
    for tag in filter_tags(images_tag):
        new_tag = Tag(repository=tag.repository,
                      registry_host="ghcr.io",
                      namespace="podboy",
                      tag=tag.tag)
        cmds.logger.info(f"\t{tag.name} -> {new_tag.name}")
        DockerClient().transport(tag.name, new_tag.name)
    return 0


@add_command(__project__)
def add_cmd(_arg: argp):
    pass


@run_command(add_cmd, add_cmd_config, add_cmd_pull, add_cmd_transport)
def run_cmd(cmds: commands) -> int:
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description=__description__,
        epilog=f"For more, please visit {__url_home__}.")
