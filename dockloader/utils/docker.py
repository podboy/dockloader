# coding:utf-8

from typing import List
from typing import TypeAlias

import docker
import docker.models
import docker.models.images

Image: TypeAlias = docker.models.images.Image
ImageList: TypeAlias = List[Image]


class DockerClient:

    def __init__(self):
        self.__client: docker.DockerClient = docker.from_env()

    @property
    def client(self) -> docker.DockerClient:
        return self.__client

    def retag(self, name: str, new_name: str) -> bool:
        return self.client.images.get(name).tag(new_name)

    def pull(self, repository: str) -> Image:
        return self.client.images.pull(repository, all_tags=False)

    def pull_all_tags(self, repository: str) -> ImageList:
        return self.client.images.pull(repository, all_tags=True)

    def push(self, repository: str):
        self.client.images.push(repository)

    def transport(self, src: str, dst: str) -> bool:
        self.pull(src)
        if not self.retag(src, dst):
            return False
        self.push(dst)
        return True
