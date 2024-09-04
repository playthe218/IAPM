import os
import random
import sys
import time
import re


def remove(packages, selects, options):
    print("\n以下的包将会被\033[34m\033[1m卸载\033[0m:")
    for package in packages:
        if package in selects:
            print("\033[1m\033[31m%s\033[0m" % package, end=" ")
        else:
            print("\033[31m%s\033[0m" % package, end=" ")
        if package == "iapm":
            iapm_dangerous = True
    confirmed = False
    
    for option in options:
        if option == "-y" or option == "--yes":
            confirmed = True
            print("\n按下 Ctrl + C 来阻止卸载")
            print("\n即将在倒计时结束后卸载:", end="")
            count_max = 5
            for i in range(1,count_max + 1):
                print(" %d" %(count_max + 1 - i), end="", flush=True)
                time.sleep(1)
        if iapm_dangerous:
            try:
                with open('/etc/iapm.conf', 'r') as conf:
                    content = conf.read()
                    if option == "--force" and "IKnowWhatImDoing" in content:
                        iapm_dangerous = False
            except: pass
        
        print()
    try:
        if iapm_dangerous:
            print('\n\033[33m警告:\033[0m 极端危险的操作\nIAPM 拒绝卸载软件包 "iapm"，如果这是您系统唯一的软件包管理器，则该操作将导致您很难处理软件包\nIAPM 仍然尊重您的操作，如果您仍要不计后果，请在 /etc/iapm.conf 添加 "IKnowWhatAmDoing" 并使用 --force 选项继续')
            return 0
    except: pass
    
    while not confirmed:
        print()
        ask = input("允许 IAPM 操作吗? [y/N] ")
        if ask == "Y" or ask == "y":
            confirmed = True
        elif ask == "N" or ask == "n" or ask == "":
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


def install(packages, selects, options):
    # List packages:
    print("\n以下的包将会被\033[34m\033[1m安装\033[0m:")
    for package in packages:
        if package in selects:
            print("\033[1m\033[34m%s\033[0m" % package, end=" ")
        else:
            print("\033[34m%s\033[0m" % package, end=" ")
    confirmed = False
    
    # Search options:
    for option in options:
        if option == "-y" or option == "--yes":
            confirmed = True
        
        print()
    # End of Search options
    
    # Ask            
    while not confirmed:
        print()
        ask = input("允许 IAPM 操作吗? [Y/n] ")
        if ask == "Y" or ask == "y" or ask == "":
            confirmed = True
        elif ask == "N" or ask == "n":
            print("操作终止")
            exit()
        else:
            print("\033[33m警告:\033[0m 无法理解")
    print()
    
    # Download
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

    # Install
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

    # Finished
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
    print("\n发行版: ", end="")
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
        except:
            select = None
        if not select:
            select = None
    except:
        print("没有指定操作")
        print("IAPM 0.1 - the \033[34mI\033[0mnstallation/\033[34mI\033[0mnstaller of \033[34mA\033[0mpps, managed by \033[34mP\033[0mLAY OS's \033[34mM\033[0manager")
        print("实现方式简单的软件包管理器")
        print("用法: iapm <help,install,update,remove,clean> <package> --<option>")
        # exit(0)
        base_action = "install"
        select = ['@all']
    if base_action == "help":
        print("用法: iapm <help,install,update,remove,clean> <package> --<option>")
        finished = 0
    elif base_action == "install" or base_action == "update" or base_action == "reinstall" or base_action == "remove":
        distro = identify_distro()
        if select is None:
            print("\033[31m错误:\033[0m 没有软件包被选定")
            exit()
        print("IAPM 正在准备 \033[1m\033[34m%s\033[0m 软件包..." % base_action, end="")
        packages = get_depends(select)
        print("完成!")
        if not base_action == "update" and select == ['@all']:
            print("\n\033[33m警告:\033[0m IAPM 只推荐在更新操作下使用 @all")
        if base_action == "install":
            finished = install(packages, select, option)
        if base_action == "remove":
            finished = remove(packages, select, option)
    else:
        print("\033[31m错误:\033[0m 操作不正确")
        print("可用操作: help, install, update, remove, clean")
        finished = 0

    try:
        exit(finished)
    except:
        exit(1)


databasedir = "/home/play/workspace/IAPM/database_test/"
reposdir = "/home/play/workspace/IAPM/repos_test/"
bindir = "~/Desktop/bin/"  # TEST INSTALL ONLY

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[31m错误:\033[0m 中止信号")
