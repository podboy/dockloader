# coding:utf-8

from typing import Any
from typing import Dict
from typing import Tuple

import requests

from .tags import Tag


class DockerHubTag:
    class ImageTag:
        def __init__(self, image: str, data: Dict[str, Any]):
            self.__image: str = image
            self.__data: Dict[str, Any] = data
            self.__architecture: str = data["architecture"]
            self.__os: str = data["os"]
            self.__digest: str = data.get("digest", "")
            self.__size: int = data.get("size", 0)

        @property
        def image(self) -> str:
            return self.__image

        @property
        def architecture(self) -> str:
            return self.__architecture

        @property
        def os(self) -> str:
            return self.__os

        @property
        def digest(self) -> str:
            return self.__digest

        @property
        def size(self) -> int:
            return self.__size

    def __init__(self, image: str, data: Dict[str, Any]):
        self.__image: str = image
        self.__data: Dict[str, Any] = data
        self.__name: str = data["name"]
        self.__digest: str = data.get("digest", "")
        self.__full_size: int = data.get("full_size", 0)
        self.__image_tags: Tuple[DockerHubTag.ImageTag, ...] = tuple(
            DockerHubTag.ImageTag(image=self.image_name, data=image_data)
            for image_data in data["images"])

    @property
    def name(self) -> str:
        return f"{self.image_name}:{self.tag_name}"

    @property
    def image_name(self) -> str:
        return self.__image

    @property
    def tag_name(self) -> str:
        return self.__name

    @property
    def digest(self) -> str:
        return self.__digest

    @property
    def full_size(self) -> int:
        return self.__full_size

    @property
    def images(self) -> Tuple["DockerHubTag.ImageTag", ...]:
        return self.__image_tags


class DockerHubTags(Dict[str, DockerHubTag]):

    def __init__(self, image: str):
        self.__tag: Tag = Tag.parse_long_name(image)
        self.__namespace: str = self.__tag.namespace
        self.__repository: str = self.__tag.repository
        self.__image: str = f"{self.namespace}/{self.repository}"
        self.__website: str = f"https://hub.docker.com/_/{self.repository}" \
            if self.namespace == "library" else \
            f"https://hub.docker.com/r/{self.namespace}/{self.repository}"
        super().__init__()

    @property
    def website(self) -> str:
        return self.__website

    @property
    def namespace(self) -> str:
        return self.__namespace

    @property
    def repository(self) -> str:
        return self.__repository

    @property
    def image(self) -> str:
        return self.__image

    @classmethod
    def fetch(cls, image: str) -> "DockerHubTags":
        """fetch all tags of an image
        """
        count: int = 0
        tags: DockerHubTags = DockerHubTags(image)
        headers: Dict[str, str] = {"Accept": "application/json"}
        url: str = f"https://hub.docker.com/v2/repositories/{tags.image}/tags/"

        while url:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise IOError(f"{url} {response.status_code} {response.reason}")  # noqa: E501

            data = response.json()
            for tag_data in data["results"]:
                tag = DockerHubTag(image=tags.image, data=tag_data)
                tags[tag.tag_name] = tag

            _count: int = data["count"]
            if count == 0:
                count = _count
            elif count != _count:
                raise ValueError(f"count {_count} != {count}")

            url = data["next"]

        if count != len(tags):
            raise ValueError(f"actual count {len(tags)} != {count}")

        return tags
