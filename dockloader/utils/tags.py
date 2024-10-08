# coding:utf-8

import os
import re
from typing import Dict
from typing import Iterable
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union
from urllib.parse import urlparse


def is_valid_transport(transport: str) -> bool:
    def is_domain_name(transport: str) -> bool:
        domain_regex = r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"  # noqa: E501
        return bool(re.match(domain_regex, transport))

    def is_domain_name_with_port(transport: str) -> bool:
        domain_with_port_regex = r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]:[0-9]+$"  # noqa: E501
        return bool(re.match(domain_with_port_regex, transport))

    def is_transport(transport: str) -> bool:
        try:
            return bool(urlparse(transport).scheme)
        except ValueError:
            return False

    return is_domain_name(transport) or is_domain_name_with_port(transport) or is_transport(transport)  # noqa: E501


def is_valid_repository_name(repository: str) -> bool:
    return bool(re.match(r"^[a-z0-9_-]+$", repository))


class Tag:
    """Docker Tag Format:

    [registry_host[:port]/][namespace/]repository[:<tag>|@sha256:<digest>]
    """

    def __init__(self, repository: str,
                 registry_host: Optional[str] = None,
                 namespace: Optional[str] = None,
                 tag: Optional[str] = None,
                 extra_tags: List[str] = [],
                 digest: Optional[str] = None):
        if tag is None:
            if len(extra_tags) > 0:
                raise ValueError("tag must be set when extra_tags is set")
        elif digest is not None:
            raise ValueError("tag and digest cannot be set at the same time")

        self.__registry_host: Optional[str] = registry_host
        self.__namespace: Optional[str] = namespace
        self.__repository: str = repository
        self.__tag: Optional[str] = tag
        self.__digest: Optional[str] = digest
        # self.__extra_tags: Dict[str, Tag] = {}
        # for extra_tag in extra_tags:
        #     etag: Tag = Tag(repository=repository,
        #                     registry_host=registry_host,
        #                     namespace=namespace,
        #                     tag=extra_tag)
        #     self.__extra_tags[etag.name] = etag
        self.__extra_tags: Tags = Tags()
        for extra_tag in extra_tags:
            etag: Tag = Tag(repository=repository,
                            registry_host=registry_host,
                            namespace=namespace,
                            tag=extra_tag)
            self.__extra_tags.append(etag)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}) "\
            f"registry: {self.registry_host}, "\
            f"namespace: {self.namespace}, "\
            f"repository: {self.repository}, "\
            f"tag: {self.tag}, digest: {self.digest}"

    def __str__(self):
        return self.name

    def __eq__(self, other: Union[str, "Tag"]) -> bool:
        if not isinstance(other, (str, Tag)):
            return False
        tag = other if isinstance(other, Tag) else Tag.parse_long_name(other)
        return tag.name == self.name

    @property
    def registry_host(self) -> str:
        return self.__registry_host or "docker.io"

    @property
    def namespace(self) -> str:
        return self.__namespace or "library"

    @property
    def repository(self) -> str:
        return self.__repository

    @property
    def tag(self) -> str:
        return self.__tag or "latest"

    @property
    def extra_tags(self) -> "Tags":
        return self.__extra_tags

    @property
    def digest(self) -> Optional[str]:
        return self.__digest

    @property
    def image(self) -> str:
        """name and tag or digest
        """
        if self.__tag is not None:
            return f"{self.repository}:{self.__tag}"
        if self.__digest is not None:
            return f"{self.repository}@{self.__digest}"
        return f"{self.repository}:latest"

    @property
    def name_without_tag(self) -> str:
        return f"{self.registry_host}/{self.namespace}/{self.repository}"

    @property
    def name_latest_tag(self) -> str:
        return f"{self.name_without_tag}:latest"

    @property
    def name_stable_tag(self) -> str:
        return f"{self.name_without_tag}:stable"

    @property
    def name(self) -> str:
        return f"{self.registry_host}/{self.namespace}/{self.image}"

    def is_extra_tag(self, other: Union[str, "Tag"]) -> bool:
        return other in self.extra_tags

    @classmethod
    def parse_short_name(cls, name_with_tag_or_digest: str)\
            -> Tuple[str, Optional[str], Optional[str], List[str]]:
        """Parse a short Docker tag name string.

        short name format: repository[:<tag|tags>|@sha256:<digest>]
        multiple tags format: <tag1>[,<tag2>[,<tag3>[,...]]]
        """
        tag: Optional[str] = None
        digest: Optional[str] = None

        # Split by ":tag" or "@sha256:digest" to get tag or digest
        repository_with_digest = name_with_tag_or_digest.split("@")
        if len(repository_with_digest) == 2:
            repository, digest = repository_with_digest
            # Check the digest format (@sha256:<digest>)
            if len(digest) != 71 or not digest.startswith("sha256:"):
                raise ValueError(f"Invalid digest: '{digest}'")
        else:
            repository_with_tag = name_with_tag_or_digest.split(":")
            if len(repository_with_tag) == 2:
                repository, tag = repository_with_tag
            else:
                repository = name_with_tag_or_digest

        if tag is not None:
            # Handle the tag format ([:<tag>[,<tag>[,...]]])
            tags = [_tag.strip() for _tag in tag.split(",")]
            return repository, tags[0], digest, tags[1:]

        return repository, tag, digest, []

    @classmethod
    def parse_long_name(cls, name: str) -> "Tag":
        """Parse a long Docker tag name string.

        [registry_host[:port]/][namespace/]repository[:<tag>|@sha256:<digest>]
        """
        # # Remove protocol prefix if present (like https:// or http://)
        # parsed_url = urlparse(name)
        # # ignore netloc and leading slash
        # name = parsed_url.path[1:] if parsed_url.scheme else name

        # Split by "/" to separate registry, namespace, and repository
        parts = name.rsplit(sep="/", maxsplit=2)
        if len(parts) == 1:
            # Case: just the repository
            registry_host = "docker.io"
            namespace = "library"
            repo_with_tag_or_digest = parts[0]
        elif len(parts) == 2:
            # Case: registry/repository or namespace/repository
            registry_host_or_namespace, repo_with_tag_or_digest = parts
            if is_valid_transport(registry_host_or_namespace):
                # Case: registry/repository
                registry_host = registry_host_or_namespace
                namespace = "library"
                repo_with_tag_or_digest = parts[1]
            else:
                # Case: namespace/repository
                registry_host = "docker.io"
                namespace = registry_host_or_namespace
        elif len(parts) == 3:
            # Case: full path including registry, namespace, and repository
            registry_host, namespace, repo_with_tag_or_digest = parts
        else:
            raise ValueError(f"Invalid tag: '{name}'")

        repository, tag, digest, extra_tags = cls.parse_short_name(
            repo_with_tag_or_digest)

        if not is_valid_repository_name(repository):
            raise ValueError(f"Invalid repository name: '{repository}'")

        return cls(repository=repository, registry_host=registry_host,
                   namespace=namespace, tag=tag, extra_tags=extra_tags,
                   digest=digest)


class Tags:
    """A set of Tags
    """

    def __init__(self):
        self.__tags: Dict[str, Tag] = {}

    def __iter__(self) -> Iterator[Tag]:
        return iter(self.__tags.values())

    def __contains__(self, other: Union[str, Tag]) -> bool:
        t = other if isinstance(other, Tag) else Tag.parse_long_name(other)
        return t.name in self.__tags or any(t in _t.extra_tags for _t in self)

    def __len__(self) -> int:
        return len(self.__tags)

    def append(self, tag: Union[str, Tag]):
        if isinstance(tag, str):
            tag = Tag.parse_long_name(tag)

        tag_name: str = tag.name
        if tag_name not in self.__tags:
            self.__tags[tag_name] = tag

    def extend(self, tags: Iterable[Union[str, Tag]]):
        for tag in tags:
            self.append(tag)

    @staticmethod
    def filter(tags: Sequence[Tag]) -> Tuple[Tag, ...]:
        names: List[str] = []
        for tag in tags:
            if tag.name not in names:
                names.append(tag.name)
        return tuple(tag.parse_long_name(name) for name in names)


filter_tags = Tags.filter


class TagConfigFile(Tags):
    """Parser tag configuration file
    """

    def __init__(self, filename: str):
        super().__init__()
        filename = os.path.abspath(filename)
        self.__dirname: str = os.path.dirname(filename)
        self.__basename: str = os.path.basename(filename)

        if not os.path.isfile(self.filename):
            raise FileNotFoundError(f"Config file not found: '{filename}'")

        with open(self.filename, "r", encoding="utf-8") as rhdl:
            for line in rhdl:
                line = line.strip()

                if line == "" or line.startswith("#"):
                    continue

                if "#" in line:
                    line = line[:line.index("#")].strip()

                if line.startswith("import"):
                    for text in line.split()[1:]:
                        path: str = os.path.join(self.dirname, text)
                        if os.path.isdir(path):
                            for file in os.listdir(path):
                                sub_path: str = os.path.join(path, file)
                                self.extend(TagConfigFile(sub_path))
                        elif os.path.isfile(path):
                            self.extend(TagConfigFile(path))
                        else:
                            raise ValueError(f"Invalid import: '{path}'")
                    continue

                self.append(Tag.parse_long_name(line))

    @property
    def dirname(self) -> str:
        return self.__dirname

    @property
    def basename(self) -> str:
        return self.__basename

    @property
    def filename(self) -> str:
        return os.path.join(self.dirname, self.basename)
