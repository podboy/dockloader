# dockloader

由于 [Docker Hub](https://hub.docker.com/) 及其镜像仓库在中国大陆地区被限制，您已无法在中国大陆地区通过 `docker pull` 来拉取映像。

虚拟化和容器技术已成为现代软件开发、开源和云计算的基石，我们完全无法想象在没有容器镜像的情况下，应用程序的构建、测试、发布和运行会如何进行。

对于普通个人用户，无论自己构建映像亦或是搭建 [Harbor](https://github.com/goharbor/harbor) 都会是一项耗时、耗力的投入与维护，也不是每个人都能轻松翻墙来拉取映像。

`dockloader` 项目的初衷是寻找一种无需任何部署即可简单替代 `docker pull` 从 docker.io 拉取映像的方案。它使用 [GitHub Actions](https://github.com/features/actions) 来从 `Docker Hub` 拉取映像并上传到 [GitHub Packages](https://github.com/features/packages) 之上，这样就可以通过 ghcr.io 来拉取映像。

这项工作并不复杂，当 `workflows` 被创建之后，仅需要提交一个 `PR` 即可触发，然后等待 `actions` 执行完毕即可通过 `docker pull ghcr.io/podboy/<image>[:tag]` 拉取对应的映像。

同时，基于 `Python(>=3.10)` 开发的 [dockloader](https://pypi.org/project/dockloader/) 命令行工具为迁移映像提供支撑。

## 拉取映像

请首先在 [Packages](https://github.com/orgs/podboy/packages) 中查找您需要的映像是否已经存在！

如果没有您需要的仓库或者特定版本，则可以提交[变更请求](#贡献指南)以更新映像。

## 贡献指南

由于 `Docker Hub` 的映像数量极其庞大，欢迎任何人贡献 `PR` 以帮助其他人获取到更多、更新、更好的映像。

提交 `PR` 之前，请先了解[贡献原则](#贡献原则)和[配置文件格式](#config-文件)，并仔细阅读此贡献指南！

### 贡献原则

- 任何已添加的仓库新增 `tag` 只做格式审查
- 无条件的接受[官方映像](https://hub.docker.com/search?image_filter=official)，只对 [library](cfgs/library) 中的新增内容做格式审查，无需提供任何额外的信息
- 增加非官方官方映像仓库，请首先考虑开源项目自己维护的官方仓库，如果没有官方仓库也请优先考虑有良好维护（定期更新并且有版本标签，而非仅有 `latest` 标签）并被广泛使用的仓库（有一定的拉取统计量），并请在配置文件的顶部增加项目链接，以供决策是否接受该仓库：
  - `Docker Hub`链接
  - 仓库（`Github`或者其他源码仓库）链接
  - 主页链接（如果存在）
  - 文档链接（如果存在）
  - 其他（如：演示、预览页面）链接

### tag 格式

映像的 tag 的格式如下：

```text
[registry_host[:port]/][namespace/]repository[:<tag>|@sha256:<digest>]
```

`Docker Hub`的`registry`为固定的`docker.io`，`namespace`为`username`（官方映像为`library`）。

### config 文件

配置文件的总入口为 [docker.io](cfgs/docker.io) 文件，每个 `username` 均需要在 [cfgs](cfgs) 文件夹中新增一个同名的文件夹，并且在 [docker.io](cfgs/docker.io) 中增加一行 `import <username>` 以导入文件夹中的所有配置文件。

每个 `repository` 均需要新增一个同名的配置文件，并放置在对应的 `username` 文件夹（官方映像为 `library` 文件夹）下。

配置文件的格式为：

- 所有 "#" 之后的内容为注释内容
- 每行一个映像，并且将所有关联的 `tag` 合并在一起（示例：`mysql:8.0.0,8.0,8,latest`）
- 请按从上至下由新到旧的顺序，并且 `latest` 在第一行

### dockloader 命令行工具

如果你对 [dockloader](https://pypi.org/project/dockloader/) 命令行工具感兴趣，请向 [dockloader branch](https://github.com/podboy/dockloader/tree/dockloader) 提交 `PR`。

非常感谢您对本项目的支持和贡献！
