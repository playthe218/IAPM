**Language / 语言 :**  [English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

---
# 贡献指南 #
IAPM 至今 (2026-1-24) 由于只有 `playthe218` 一个人在维护而正在缓慢开发。 <br>
我们感谢有意为 IAPM 贡献的人，请看下文： <br>

## 项目结构 ##
```
IAPM/                       # 我们有时用 "SRC://" 代替它。
|-share/
| |-exampleRepo             # 示例仓库。
| | |-os.repo               # 示例: 操作系统的软件仓库。
| |-iapm.conf               # IAPM 主程序配置文件。
| |-repos.conf              # IAPM 仓库配置文件。
|-src/
| |-iapm/                   # IAPM 内建模块。
| | |-__init__.py
| | |-action.py             # 包含 IAPM 的所有 action 。
| | |-base.py               # IAPM 基础内部功能。
| | |-extra.py              # IAPM 高级内部功能。
| |-main.py                 # IAPM 主程序。
|-test/                     # 完成测试 IAPM 需要的内容。
| |-example/                # 未打包的 "example" 软件包，可用于测试 mkiap 功能。
| |-repos/                  # 软件仓库。存放示范性软件包，测试下载、更新等是否正常。
|-.gitignore                # 请使用此文件，屏蔽不需要的临时文件。
```

## .iap 软件包 ##
IAPM 使用的软件包格式为 **`.iap`** ，<del>本质是 tar 打包完之后改了下后缀名。</del> <br>
仓库内有一个示例用的 .iap 软件包，结构如下：
```
example.iap/
|-install/                  # 安装内容。
| |-usr/
|   |-bin/
|     |-helloiapm           # 一个可以直接执行的 Python 文件，它会输出 "Hello, world!"。
|-install_config/           # 安装的配置文件。
|-post_install/             # 安装后脚本。
| |-1_test.sh               # 先执行。
| |-2_test.sh               # 后执行。
|-post_install_imme/        # 安装后脚本，立即执行。
| |-...                     # 同上，之后省略。
|-post_remove/              # 移除后脚本。
|-post_remove_imme/         # 移除后脚本，立即执行。
|-post_update/              # 更新后脚本。
|-post_update_imme/         # 更新后脚本，立即执行。
|-pre_install/              # 安装前脚本。
|-pre_remove/               # 移除前脚本。
|-pre_update/               # 更新前脚本。
|-package.info              # 软件包元信息。
```
.iap 软件包的安装、移除、更新前后 (或它们的"立即执行") 脚本理论上**不限制语言**，前提是这些脚本可以以 ```./xxx``` 的方式直接运行。 <br>
出于兼容性保障，请在开头加入 ```#! /usr/bin/env xxx``` 声明解释器。建议使用 Shell、Python 来撰写这些脚本，其中 Shell 是几乎所有的**基本可用的 Linux 发行版**必然包含的软件包，而 Python 是 IAPM 的依赖项之一。

## 定义 & 术语 ##
接下来的内容可能会使用以下定义或术语，这些定义或术语通常不会在仓库内的其他部分进行翻译： <br>
* `SRC://` : IAPM 源代码仓库的根目录。
* `action` : IAPM 的目标操作，通常被识别第一个不以 `--` 或 `-` 开头的参数。也就是 `install` 、 `remove` 、 `update` 等。
* `stage` : IAPM 的操作阶段。
* `PR` : 老生常谈，这是 Pull Request 。
* `.iap` : IAPM 使用的软件包。
* `基本可用的 Linux 发行版` : 我们认定为一个至少可以通过 chroot 进入的 Linux 发行版，且至少包含 `coreutils`。我们不保证 `busybox` 的替代项能完美替代 IAPM 所需的功能。

## 准备开始 ##
1. Fork 这个仓库，然后 Clone 您的 Fork 。
2. 创建分支，千万、千万不要使用 `main` (主线)、 `test` (测试)、 `dev` (开发)、 `NUM.NUM` (固定):
```bash 
git checkout -b xxx
```
3. 瞎改一番。
4. 提交您的改动，为了减少查看时间，推荐写明改动目的: 
```bash
git commit
```
5. 推送到远程仓库:
```bash
git push origin xxx
```
6. 提交 PR 。
### PR 格式 ###
IAPM 正处于开发阶段，我们欢迎大家的贡献，但我们不一定总是有力查阅所有贡献。 <br>

为了避免 PR 被拒绝，您**必须写明修改**，示例:
```
feature: 添加 xxx 功能。
fix: 修复 xxx bug/漏洞。
performance: 提高参数处理性能
docs: 更新 README.md
```
如果此项未写明，您的 PR 的查阅预计会**被排到最后**，或**被直接拒绝**。

为了提高 PR 的查阅优先级，我们也建议您写明修改涉及的文件。

### 检查 ###
一般情况下，这/这些不一定是必需由您完成的，但自行完成检查并在 PR 内告知检查结果，或许可以**显著减少查阅所需的时间**:
* ```iapm --test --debug xxx```: ```--test``` 会**跳过 root 权限检查**，并**创建一个假的根目录 ```~/.iapm/fakeroot/```** 。```--debug``` 会**指示大多数信息的级别**，并**显示这些信息发出时的时间**。
* ```iapm --test --verbose xxx```: ```--test``` 同上。 ```--verbose``` 会将 ```--debug``` 显示的时间点由精确到**秒**改动为精确到**毫秒**，如果您的更改是性能优化，可以用这个指令产生并将原版的测试结果与您的测试结果放在一起，以凸显您的的实现<del>非常的牛逼</del>比原版更好。

### 哪些 PR 会被拒绝 ###
以下记录了通常会被拒绝的 PR ，请避免相同情况： <br>
1. "热心"的格式化: 只是把代码丢进 black 格式化一遍，并没有其他实际的功能、修复或优化性改动，然后交了 PR 。
2. 过度优化: 为了提高性能或精简代码大小(甚至只是为了省一个换行符)，严重忽视了可读性；最坏的情况下，这样的过度优化或许可读性很低，而其目的也未能达成:
    ```python
    for x in range(1, 10):
        for y in range(1, x+1):
            print(str(y)+"x"+str(x)+"="+str(x*y), end=" ")
        print()
    ```
    ```python
    for x in range(1, 10): print(" ".join([str(y)+"x"+str(x)+"="+str(x*y) for y in range(1, x+1)]))
    ```
3. 我导入了 100 个包：导入了大量的 Python 包，甚至包括了绝大部分 Linux 发行版的基础安装甚至最小安装不会安装的。
4. 大可不必的功能：明显不符合软件包管理器应有功能的，例如：调用 ChatGPT 或 DeepSeek 或这 AI 那 AI 的 API 。
5. 存在恶意代码的提交：活爹啊你可别塞点什么挖矿程序进来然后一个提交把我 GitHub 仓库的骨灰都扬了，你敢这么干让我逮住了我就叫 GitHub 把你的账号的骨灰扬了。

如果我们在将来遇到更多典型问题或常见的错误模式，本节内容将会随时更新。

## 许可证 ##
IAPM 从 3.0 开始在 **GPL-3.0-or-later (GPL-3.0 或更新版本)** 许可证下发布，故您为 IAPM 贡献的代码将会随之以 **GPL-3.0-or-later** 一同发布，提交即表示同意。