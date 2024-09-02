import os
import random
import sys
import time
import re


def remove(packages, selects):
    print("\n以下的包将会被\033[34m\033[1m卸载\033[0m:")
    for package in packages:
        if package in selects:
            print("\033[1m\033[34m%s\033[0m" % package, end=" ")
        else:
            print("\033[34m%s\033[0m" % package, end=" ")
    confirmed = False
    print()
    while not confirmed:
        ask = input("允许 IAPM 操作吗? [Y/n] ")
        if ask == "Y" or ask == "y" or ask == "":
            confirmed = True
        elif ask == "N" or ask == "n":
            print("操作终止")
            exit()
        else:
            print("\033[33m警告:\033[0m 无法理解")
    print("\n卸载软件包:")
    for package in packages:
        spacing = " " * (32 - len(package))
        bar = 16
        for i in range(bar + 1):
            finishbar = "|" * i
            emptybar = "-" * (bar - i)
            print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
            time.sleep(random.randint(5, 50) / 1000)
        print()
    print("\n操作完成!")
    return 1


def install(packages, selects):
    print("\n以下的包将会被\033[34m\033[1m安装\033[0m:")
    for package in packages:
        if package in selects:
            print("\033[1m\033[34m%s\033[0m" % package, end=" ")
        else:
            print("\033[34m%s\033[0m" % package, end=" ")
    confirmed = False
    print()
    while not confirmed:
        ask = input("允许 IAPM 操作吗? [Y/n] ")
        if ask == "Y" or ask == "y" or ask == "":
            confirmed = True
        elif ask == "N" or ask == "n":
            print("操作终止")
            exit()
        else:
            print("\033[33m警告:\033[0m 无法理解")
    print()
    for package in packages:
        spacing = " " * (32 - len(package))
        bar = 16
        for i in range(bar + 1):
            finishbar = "|" * i
            emptybar = "-" * (bar - i)
            print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
            time.sleep(random.randint(1, 5) / 10)
        print()
    print()

    print("\n安装软件包:")
    for package in packages:
        spacing = " " * (32 - len(package))
        bar = 16
        for i in range(bar + 1):
            finishbar = "|" * i
            emptybar = "-" * (bar - i)
            print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
            time.sleep(random.randint(5, 50) / 1000)
        print()
    print()

    print("\n操作完成!")
    return 1


def parse_repo_file(repo_file):
    """
    解析一个 .repo 文件，返回一个字典，表示每个包及其依赖关系
    """
    dependencies = {}
    with open(repo_file, 'r') as f:
        current_package = None
        for line in f:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                # 读取包名
                current_package = line[1:-1].strip()
                dependencies[current_package] = set()
            elif line.startswith('depends='):
                # 提取依赖关系
                match = re.search(r'depends=\{(.*?)\}', line)
                if match:
                    deps = match.group(1).replace("'", "").replace('"', "").split(',')
                    dependencies[current_package].update(dep.strip() for dep in deps if dep.strip())
    return dependencies

def get_depends(packages):
    """
    获取给定包的所有依赖包
    """
    # 存储所有依赖关系
    all_dependencies = {}
    
    # 读取所有 .repo 文件
    for file in os.listdir(reposdir):
        if file.endswith('.repo'):
            repo_file_path = os.path.join(reposdir, file)
            dependencies = parse_repo_file(repo_file_path)
            all_dependencies.update(dependencies)

    # 存储最终结果
    result = set()

    def resolve(package):
        if package in all_dependencies:
            result.add(package)
            for dep in all_dependencies[package]:
                resolve(dep)

    for package in packages:
        resolve(package)

    return list(result)


def identify_distro():
    print("发行版: ", end="")
    # distro = platform.linux_distribution()
    distro = os.popen("lsb_release -i").read().strip()
    distro = distro.split(" ")[1][4:]
    print(distro + "\n")
    return distro


def main():
    # 获取基本行为和选定软件包与选项
    try:
        base_action = sys.argv[1]
        select = []
        option = []
        try:
            for i in range(2, len(sys.argv)):
                if sys.argv[i].startswith("-") or sys.argv[i].startswith("--"):
                    option.append(sys.argv[i])
                else:
                    select.append(sys.argv[i])
            if option:
                print(option)
        except:
            select = None
        if not select:
            select = None
    except:
        print("没有指定操作")
        print("IAPM 0.1 - the \033[34mI\033[0mnstallation/\033[34mI\033[0mnstaller of \033[34mA\033[0mpps, managed by \033[34mP\033[0mLAY OS's \033[34mM\033[0manager")
        print("实现方式简单的软件包管理器")
        print("用法: iapm <help,install,update,reinstall,remove,clean> <package> --<option>")
        exit(0)
        # base_action = "debug" # use on debug
    if base_action == "help":
        print("用法: iapm <help,install,update,reinstall,remove,clean> <package> --<option>")
        finished = 0
    elif base_action == "install" or base_action == "update" or base_action == "reinstall" or base_action == "remove":
        distro = identify_distro()
        if select is None:
            print("\033[31m错误:\033[0m 没有软件包被选定")
            exit()
        print("IAPM 正在准备 \033[1m\033[34m%s\033[0m 软件包..." % base_action, end="")
        packages = get_depends(select)
        print("完成!")
        if base_action == "install":
            finished = install(packages, select)
        if base_action == "remove":
            finished = remove(packages, select)
    else:
        print("\033[31m错误:\033[0m 操作不正确")
        print("可用操作: help, install, update, reinstall, remove, clean")
        finished = 0

    try:
        exit(finished)
    except:
        exit(1)


reposdir = "/home/play/Desktop/IAPMProject/repos/"
bindir = "~/Desktop/bin/"  # DEBUGING ONLY

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[31m错误:\033[0m 中止信号")
