def main(targets, repofile):
    import configparser

    packages = targets
    FoundNewDepends = False
    for i in range(len(packages)):
        target = packages[i]
        repos = configparser.ConfigParser()
        repos.read(repofile)

        
