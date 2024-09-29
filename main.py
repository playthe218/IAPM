#!/usr/bin/env python3

import os
import random
import sys
import time
import re
import gettext
T = gettext.translation('iapm', '/usr/share/locale')
_ = T.gettext

def clean_exists(packages, select):
    exists = []

    # 提取databasedir目录下的所有<软件包名>.info文件
    for filename in os.listdir(databasedir):
        if filename.endswith('.info'):
            package_name = filename[:-5]  # 去掉.info后缀
            exists.append(package_name)

    # 使用集合来提高查找效率
    exists_set = set(exists)
    select_set = set(select)

    # 遍历packages
    for package in packages[:]:  # 使用切片以便安全移除元素
        if package in select_set:
            if package in exists_set:
                # 如果package在exists中且在select中
                print(_("\033[33mATTENTION:\033[0m The package \033[32m%s\033[0m will be \033[34m\033[1mreinstalled\033[0m." % package))
            else:
                continue
        if package in exists_set and not package in select_set:
            packages.remove(package)  # 移除package

    return packages

def list_packages(packages, selects, action):
    if action == "remove":
        color = "\033[31m"
    else:
        color = "\033[34m"
    normal = "\033[0m"
    for package in packages:
        if package in selects:
            print("\033[1m%s%s%s "%(color, package, normal), end="")
        else:
            print("%s%s%s "%(color, package, normal), end="")

def update_check():
    # 初始化一个包含所有软件包VERCOMPARE的字典
    vercompare_dict = {}

    # 遍历reposdir目录下的所有repo文件
    for repo_file_name in os.listdir(reposdir):
        if repo_file_name.endswith('.repo'):
            repo_file_path = os.path.join(reposdir, repo_file_name)
            with open(repo_file_path, 'r') as file:
                current_section = None
                for line in file:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        vercompare_dict[current_section] = {'vercompare': 0}
                    elif '=' in line:
                        key, value = line.split('=', 1)
                        value = value.replace("'", "").replace('{', '').replace('}', '')
                        if key == 'vercompare':
                            vercompare_dict[current_section]['vercompare'] = int(value)

    # 读取info文件内容并比较版本
    info_files = [f for f in os.listdir(databasedir) if f.endswith('.info')]
    for info_file in info_files:
        file_path = os.path.join(databasedir, info_file)
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('name='):
                    package_name = line[5:]
                elif line.startswith('ver='):
                    package_version = line[4:]
                elif line.startswith('vercompare='):
                    info_data = {'version': package_version, 'vercompare': int(line[11:])}
                    if package_name in vercompare_dict and vercompare_dict[package_name]['vercompare'] < info_data['vercompare']:
                        # If vercompare in info is greater than repo, it's an update
                        vercompare_dict[package_name]['update'] = 'update1'
                    elif package_name in vercompare_dict and vercompare_dict[package_name]['vercompare'] != info_data['vercompare']:
                        # If vercompare in info is different and greater than repo, it might be an update
                        vercompare_dict[package_name]['update'] = 'update_maybe'

    # 收集需要更新的软件包
    updates = [pkg for pkg, data in vercompare_dict.items() if 'update' in data and data['update'] in ['update1', 'update_maybe']]

    return updates

def clean():
    rm_cachedir = input(_("Clean up IAPM cache? [Y/n] "))
    if rm_cachedir == "y" or rm_cachedir == "Y":
        os.system("rm -rf /var/cache/iapm/*")
    else: pass
    
    print(_("Operation completed!"))
    
    return 0

def update(packages, selects, options):   
    confirmed = False
    # Search options:
    for option in options:
        if option == "-y" or option == "--yes":
            confirmed = True
    # End of Search options
    
    # List packages:
    if packages == []:
        print(_("\nNo packages will be operated."))
        return 1
    
    print(_("\nThese packages will be \033[34m\033[1mupdated\033[0m:"))
    list_packages(packages, selects, "update")
    
    print()
    # Ask            
    while not confirmed:
        print()
        ask = input(_("Allow IAPM to operate? [Y/n] "))
        if ask == "Y" or ask == "y" or ask == "":
            confirmed = True
        elif ask == "N" or ask == "n":
            print(_("Operation aborted."))
            exit()
        else:
            print(_("\033[33mWARNING:\033[0m Can not understand."))
    print()
    
    # Download
    print(_("Downloading packages:"))
    for package in packages:
        spacing = " " * (32 - len(package))
        bar = 16
        for i in range(bar + 1):
            finishbar = "|" * i
            emptybar = "-" * (bar - i)
            print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
            time.sleep(random.randint(1, 5) / 10)
        os.system("scp %s/%s.iap %s"%(dwfrom, package, tmpdir))
        print()

    # Install
    print(_("\nInstalling packages:"))
    for package in packages:
        spacing = " " * (32 - len(package))
        bar = 16
        for i in range(bar + 1):
            finishbar = "|" * i
            emptybar = "-" * (bar - i)
            print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
            time.sleep(random.randint(5, 50) / 1000)
        print()
        os.system("mkdir %s/%s"%(tmpdir, package))
        os.system("tar xf %s/%s.iap --directory=%s"%(tmpdir, package, tmpdir))
        os.system("%s/%s/do_pre/*" % (tmpdir, package))
        os.system("cp -r %s/%s/install/* %s/"%(tmpdir, package, rootdir))
        os.system("cp %s/%s/%s.info %s/%s.info"%(tmpdir, package, package, databasedir, package))
        os.system("%s/%s/do_post/*" % (tmpdir, package))
        os.system("rm -rf %s/%s"%(tmpdir, package))
        
    # Finished
    print(_("\nOperation completed!"))
    return 0

def remove(packages, selects, options):
    confirmed = False
    
    for option in options:
        if option == "-y" or option == "--yes":
            confirmed = True
    
    print(_("\nThese packages will be \033[34m\033[1mremoved\033[0m:"))
    list_packages(packages, selects, "remove")
    
    if "iapm" in packages:
        iapm_dangerous = True
    
    try:
        if iapm_dangerous:
            try:
                with open('/etc/iapm.conf', 'r') as conf:
                    content = conf.read()
                    if option == "--force" and "IKnowWhatImDoing" in content:
                        iapm_dangerous = False
            except: pass
    except: pass
    
    print()                     
    try:
        if iapm_dangerous:
            print(_('\n\033[33mWARNING:\033[0m The operation is VERY DANGER\nIAPM rufused to remove the package "iapm". If IAPM is the only package manager on your system, this will make it difficult to manage the packages\nIf you STILL want to continue, please add "IKnowWhatImDoing" to /etc/iapm.conf and continue with option "--force"'))
            print(_("Operation aborted."))
            return 0
    except: pass
    
    if confirmed:
        print(_("\nPress Ctrl + C to stop removing."))
        print(_("\nRemoving in:", end=""))
        count_max = 5
        for i in range(1,count_max + 1):
            print(" %d" %(count_max + 1 - i), end="", flush=True)
            time.sleep(1)
    while not confirmed:
        print()
        ask = input(_("Allow IAPM to operate? [y/N] "))
        if ask == "Y" or ask == "y":
            confirmed = True
        elif ask == "N" or ask == "n" or ask == "":
            print("O")
            exit()
        else:
            print(_("\033[33mWARNING:\033[0m Can not understand."))
    print(_("\nRemoving packages:"))
    for package in packages:
        spacing = " " * (32 - len(package))
        bar = 16
        for i in range(bar + 1):
            finishbar = "|" * i
            emptybar = "-" * (bar - i)
            print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
            time.sleep(random.randint(5, 50) / 1000)
        print()
        
        with open("%s/%s.info"%(databasedir, package), 'r') as info:
            info_contents = info.readlines()
        
        info_contents.append('\n')
        remove = []
        for line in info_contents:
            line = line.strip()
            if "installation_file" in line:
                files = line.split("installation_file=")[1].strip()
                remove.append(files)
            if "pre_remove" in line:
                pre_remove = line.split("pre_remove=")[1].strip('"')
                try:
                    os.system(pre_remove)
                except: pass
            if "post_remove" in line:
                post_remove = line.split("post_remove=")[1].strip('"')
        for file in remove:
            os.system("rm -rf %s/%s"%(rootdir, file))
        try:
            os.system(post_remove)
        except: pass
        os.system("rm -rf %s/%s.info"%(databasedir, package))
    print(_("\nOperation completed!"))
    return 0


def install(packages, selects, options):
    confirmed = False
    # Search options:
    for option in options:
        if option == "-y" or option == "--yes":
            confirmed = True
        if option == "--no-depends":
            print(_("\033[33mWARNING:\033[0m Skipping dependency handling is not recommended."))
            packages = selects
    # End of Search options
    
    # List packages:
    if packages == []:
        print(_("\nNo packages will be operated."))
        return 1
    
    print(_("\nThese packages will be \033[34m\033[1minstalled\033[0m:"))
    list_packages(packages, selects, "install")
    
    print()
    # Ask            
    while not confirmed:
        print()
        ask = input(_("Allow IAPM to operate? [Y/n] "))
        if ask == "Y" or ask == "y" or ask == "":
            confirmed = True
        elif ask == "N" or ask == "n":
            print(_("Operation aborted."))
            exit()
        else:
            print(_("\033[33mWARNING:\033[0m Can not understand."))
    print()
    
    # Download
    print(_("Downloading packages:"))
    for package in packages:
        if not os.path.exists("%s/%s.iap" % (tmpdir, package)):
            spacing = " " * (32 - len(package))
            bar = 16
            for i in range(bar + 1):
                finishbar = "|" * i
                emptybar = "-" * (bar - i)
                print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
                time.sleep(random.randint(1, 5) / 10)
            os.system("scp %s/%s.iap %s"%(dwfrom, package, tmpdir))
            print()

    # Install
    print(_("\nInstalling packages:"))
    for package in packages:
        spacing = " " * (32 - len(package))
        bar = 16
        for i in range(bar + 1):
            finishbar = "|" * i
            emptybar = "-" * (bar - i)
            print("\r{}{}[{}{}]".format(package, spacing, finishbar, emptybar), end="")
            time.sleep(random.randint(5, 50) / 1000)
        print()
        os.system("mkdir %s/%s"%(tmpdir, package))
        os.system("tar xf %s/%s.iap --directory=%s"%(tmpdir, package, tmpdir))
        os.system("%s/%s/do_pre/*" % (tmpdir, package))
        os.system("cp -r %s/%s/install/* %s/"%(tmpdir, package, rootdir))
        os.system("cp %s/%s/%s.info %s/%s.info"%(tmpdir, package, package, databasedir, package))
        os.system("%s/%s/do_post/*" % (tmpdir, package))
        os.system("rm -rf %s/%s"%(tmpdir, package))
        
    # Finished
    print(_("\nOperation completed!"))
    return 0


def parse_repo_file(repo_file, get):
    """
    解析一个 .repo 文件，返回一个字典，表示每个包及其依赖关系
    """
    dependencies = {}
    with open(repo_file, 'r') as repo:
        current_package = None
        for line in repo:
            line = line.strip()
            if get == "depends":    
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
            dependencies = parse_repo_file(repo_file_path, "depends")
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
    print(_("\nDistro: "), end="")
    # distro = platform.linux_distribution()
    distro = os.popen("lsb_release -i").read().strip()
    distro = distro.split(" ")[1][4:]
    print(distro + "\n")
    return distro

def main(root):
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
            option = []
        if not select:
            select = None
        if not option:
            option = []
    except:
        print(_('No action. (Get help with action "help")'))
        exit(0)     # 需要debug时注释掉，然后改下面的变量决定要调试的功能
        base_action = "install"
        select = ['fastfetch']
        option = []
        print("The IAPM is debugging.")
    
    if base_action == "help":
        print("\033[1miapm \033[34mhelp")
        print("     \033[34mversion")
        print("     \033[34minstall \033[32m<packages> \033[33m<options>")
        print("     \033[34mupdate \033[32m<@all/pkg> \033[33m<options>")
        print("     \033[34mremove \033[32m<packages> \033[33m<options>")
        print("     \033[34mclean")
        finished = 0
    
    elif base_action == "version":
        print("  ______")
        print(" /|    |\\   IAPM 1.0")
        print(_("/ |____| \\  A simple package manager"))
        finished = 0

    elif base_action == "clean":
        if root:
            finished = clean()
        else: 
            print(_("\033[31mERROR:\033[0m Must run as root."))
            finished = 0
    
    elif base_action == "install" or base_action == "update" or base_action == "cleans" or base_action == "remove":
        if root:
            distro = identify_distro()
            if select is None:
                print(_("\033[31mERROR:\033[0m No package is selected."))
                exit()
            
            print(_("Preparing to \033[1m\033[34m%s\033[0m...") % base_action, end="")
            if base_action != "update":
                packages = get_depends(select)
            if base_action == "update" and select == ['@all']:
                packages = update_check()
            print(_("OK!"))
            
            if not base_action == "update" and select == ['@all']:
                print(_('\n\033[33mERROR:\033[0m @all only can be used with action "update".'))
                exit(0)
            if base_action == "install":
                packages = clean_exists(packages, select)
                finished = install(packages, select, option)
            if base_action == "remove":
                finished = remove(select, select, option)
            if base_action == "update":
                finished = update(packages, packages, option)
        else: 
            print(_("\033[31mERROR:\033[0m Must run as root."))
            finished = 0 
        
    else:
        print(_("\033[31mERROR:\033[0m The action does not exist."))
        print(_("Available actions: help, version, install, update, remove, clean"))
        finished = 0

    exit(finished)

config = {}
with open("/etc/iapm.conf", 'r') as conf:
    for line in conf:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.replace('_', '')
                config[key] = value.strip()

rootdir = config.get('rootdir', '/')
dwfrom = config.get('downloadfrom', '')
reposdir = config.get('reposdir', '/var/db/iapm/repos')
tmpdir = config.get('cachedir', '/var/cache/iapm/')
databasedir = config.get('databasedir', '/var/db/iapm/database')
# print(rootdir, dwfrom, reposdir, tmpdir, databasedir) # 在确认是否正确时取消注释

if __name__ == "__main__":
    try:
        if os.getuid() == 0:
            main(True)
        else:
            main(False)
    except KeyboardInterrupt:
        print(_("\n\033[31mERROR:\033[0m Ctrl + C is pressed."))
