# coding:utf-8

import sys
from typing import List

from dockloader import Tag
from dockloader import TagConfig

old_config_file = sys.argv[1]
new_config_file = sys.argv[2]

old_config = TagConfig(old_config_file)
new_config = TagConfig(new_config_file)

new_tags: List[Tag] = []
for tag in new_config:
    if tag not in old_config:
        new_tags.append(tag)


if len(new_tags) > 0:
    print(" ".join([tag.name for tag in new_tags]))
