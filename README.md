# dockloader

由于 `Docker Hub` 及其镜像仓库在中国大陆地区被限制，您已无法在中国大陆地区通过 `docker pull` 来拉取映像。

虚拟化和容器技术已成为现代软件开发、开源和云计算的基石，我们完全无法想象在没有容器镜像的情况下，应用程序的构建、测试、发布和运行会如何进行。

对于普通个人用户，无论自己构建映像亦或是搭建 [Harbor](https://github.com/goharbor/harbor) 都会是一项耗时、耗力的投入与维护，也不是每个人都能轻松翻墙来拉取映像。

`dockloader` 项目的初衷寻找一种可简单替代 `docker pull` 从 docker.io 拉取映像的方案。它使用 [GitHub Actions](https://github.com/features/actions) 来从 `Docker Hub` 拉取映像并上传到 [GitHub Packages](https://github.com/features/packages) 之上，这样就可以通过 ghcr.io 来拉取映像。

这项工作并不复杂，当 `workflows` 被创建之后，仅需要提交一个 `PR` 即可触发，然后等待 `actions` 执行完毕即可。

同时，基于 `Python(>=3.8)` 开发的 [dockloader](https://pypi.org/project/dockloader/) 命令行工具可以方便的在多个镜像仓库之间迁移映像。

## 贡献指南

由于 `Docker Hub` 的映像极其庞大，我们欢迎你能贡献你的 `PR` 以帮助所有人获取到更多、更新的映像。

如果你对 [dockloader](https://pypi.org/project/dockloader/) 命令行工具感兴趣，请向 [dockloader branch](https://github.com/podboy/dockloader/tree/dockloader) 提交 `PR`。

非常感谢您对本项目的支持和贡献！
