# coding:utf-8

import os
from typing import List

from xarg import add_command
from xarg import argp
from xarg import commands
from xarg import run_command

from .parser import Tag
from .parser import Tags
from .parser import TagConfigFile

DEFAULT_CONFIG_FILE = os.path.join("cfgs", "docker.io")


@add_command("diff", description="list all different tags")
def add_cmd_config_diff(_arg: argp):
    _arg.add_argument(type=str, dest="config_file_diff",
                      help="another configuration file",
                      nargs=1, metavar="FILE")


@run_command(add_cmd_config_diff)
def run_cmd_config_diff(cmds: commands) -> int:
    another_config_file: str = cmds.args.config_file_diff[0]
    current_config_file: str = cmds.args.config_file[0]
    another_config = TagConfigFile(another_config_file)
    current_config = TagConfigFile(current_config_file)

    diff_tags: Tags = Tags()
    for tag in current_config:
        extra_tags: List[Tag] = [etag for etag in tag.extra_tags]
        batch_tags: List[Tag] = list(reversed(extra_tags))
        batch_tags.append(tag)

        if any(_tag not in another_config for _tag in batch_tags):
            latest_tag: str = tag.name_latest_tag
            stable_tag: str = tag.name_stable_tag
            if latest_tag in another_config:
                # Automatically add the latest tag again
                diff_tags.append(Tag.parse_long_name(latest_tag))
            if stable_tag in another_config:
                # Automatically add the stable tag again
                diff_tags.append(Tag.parse_long_name(stable_tag))
            diff_tags.extend(batch_tags)

    if len(diff_tags) > 0:
        cmds.stdout(" ".join(reversed([tag.name for tag in diff_tags])))
    return 0


@add_command("config", description="list configuration file")
def add_cmd_config(_arg: argp):
    _arg.add_opt_on("--extra-tags", dest="extra_tags",
                    help="list all extra tags")
    _arg.add_argument("-f", "--config-file", dest="config_file", type=str,
                      help="the configuration file", nargs=1,
                      default=[DEFAULT_CONFIG_FILE], metavar="FILE")


@run_command(add_cmd_config, add_cmd_config_diff)
def run_cmd_config(cmds: commands) -> int:
    if not cmds.has_sub(add_cmd_config):
        tags: Tags = Tags()
        config_file: str = cmds.args.config_file[0]
        extra_tags: bool = cmds.args.extra_tags

        for tag in TagConfigFile(config_file):
            if extra_tags:  # list all extra tags
                tags.extend(tag.extra_tags)
            tags.append(tag)

        for tag in tags:  # stdout all tags
            cmds.stdout(tag.name)
    return 0
