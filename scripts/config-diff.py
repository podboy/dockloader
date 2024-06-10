# coding:utf-8

import sys

from dockloader import Tag
from dockloader import TagConfigBase
from dockloader import TagConfigFile

old_config_file = sys.argv[1]
new_config_file = sys.argv[2]

old_config = TagConfigFile(old_config_file)
new_config = TagConfigFile(new_config_file)

add_tags: TagConfigBase = TagConfigBase()
for tag in new_config:
    if tag not in old_config:
        latest_tag: str = tag.name_latest_tag
        if latest_tag in old_config:
            # Automatically add the latest tag again
            add_tags.append(Tag.parse_long_name(latest_tag))
        add_tags.extend(tag.extra_tags)
        add_tags.append(tag)


if len(add_tags) > 0:
    print(" ".join([tag.name for tag in add_tags]))
