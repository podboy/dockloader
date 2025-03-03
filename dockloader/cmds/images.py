# coding:utf-8

from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from xkits import Namespace
from xkits import add_command
from xkits import argp
from xkits import commands
from xkits import run_command

from ..utils import DockerClient
from ..utils import Tag
from ..utils import TagConfigFile
from ..utils import filter_tags


def parse_tags(args: Namespace) -> Tuple[Tag, ...]:
    tags: List[Tag] = [Tag.parse_long_name(name) for name in args.images]
    if len(args.config_file) > 0:
        config_file: str = args.config_file[0]
        for tag in TagConfigFile(config_file):
            tags.append(tag)

    extra_tags: List[Tag] = []
    for tag in tags:
        extra_tags.extend(tag.extra_tags)

    return filter_tags(tags + extra_tags)


def add_opt_config_file(_arg: argp, help: str):
    _arg.add_argument("-f", "--config-file", dest="config_file", type=str,
                      help=help, nargs=1, default=[], metavar="FILE")


def add_pos_images(_arg: argp, help: str):
    _arg.add_argument(type=str, dest="images", help=help,
                      nargs="*", default=[], metavar="IMAGE")


@add_command("pull", description="pull image")
def add_cmd_pull(_arg: argp):
    _arg.add_opt_on("-a", "--all-tags", dest="all_tags",
                    help="pull all image tags")
    add_opt_config_file(_arg, "the configuration file for pulling")
    add_pos_images(_arg, "the name for pulling")


@run_command(add_cmd_pull)
def run_cmd_pull(cmds: commands) -> int:
    cmds.logger.info("Pulling images:")
    for tag in parse_tags(cmds.args):
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
                      help="transport to another registry, default is ghcr.io",
                      nargs=1, default=["ghcr.io"], metavar="REGISTRY")
    _arg.add_argument("-n", "--namespace", dest="namespace", type=str,
                      help="transport to new namespace, default to old value",
                      nargs=1, default=[None], metavar="NAMESPACE")
    _arg.add_argument("--repo", "--repository", dest="repositorys", type=str,
                      help="transport to new repository, default to old value",
                      nargs=1, default=[], action="extend", metavar="REPO")
    add_opt_config_file(_arg, "the configuration file for transporting")
    add_pos_images(_arg, "the name for transporting")


@run_command(add_cmd_transport)
def run_cmd_transport(cmds: commands) -> int:
    registry: str = cmds.args.registry[0]
    namespace: Optional[str] = cmds.args.namespace[0]
    repositorys: Dict[int, str] = {i: r for i, r in
                                   enumerate(cmds.args.repositorys)}
    target: str = f"{registry}/{namespace}" if namespace else registry

    cmds.logger.debug(f"Transporting repositorys: {repositorys}")
    cmds.logger.info(f"Transporting images to {target}:")

    def get_repository_name(index: int, default: str) -> str:
        if len(repositorys) > 0:
            return repositorys.get(index, repositorys[0])
        return default

    for idx, tag in enumerate(parse_tags(cmds.args)):
        new_tag = Tag(repository=get_repository_name(idx, tag.repository),
                      namespace=namespace if namespace else tag.namespace,
                      registry_host=registry, tag=tag.tag)
        cmds.logger.info(f"\t{tag.name} -> {new_tag.name}")
        DockerClient().transport(tag.name, new_tag.name)
    return 0
