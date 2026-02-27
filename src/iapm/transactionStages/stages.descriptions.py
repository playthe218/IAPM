def downloads(packages_summary, repos_summary, rootdir, cachedir, dl_backend):
    # We are trying to use subprocess instead of os.system
    import subprocess
    print("Downloading packages.")
    
    # things are all messed, mess mess mess mess
    for i in range(len(packages_summary)):
        url = "%s/%s/%s/%s/%s" % (
                 repos_summary["dl"], 
                 packages_summary[i]["arch"], 
                 packages_summary[i]["category"],
                 packages_summary[i]["name"],
                 packages_summary[i]["which"]
                )
        if dl_backend == "curl":
            how_to = [
            'curl',
            '-o',
            '%s/%s/%s' % (rootdir, cachedir, packages_summary[i]["which"]),
            url
            ]
        try:
            #pass
            subprocess.run(how_to, check=True)
        except subprocess.CalledProcessError:
            print("Failed to download package %s-%s." % (packages_summary[i]["name"], packages_summary[i]["version"]))
            return 1
    
# verify(packages_summary, rootdir, cachedir, gpgdir)
def unpack(packages_summary, rootdir, cachedir):
    import subprocess
    print("Unpacking packages")
    
    for i in range(len(packages_summary)):
        how_to = [
            "tar",
            "-xf" ,
            "%s/%s/%s" % (rootdir, cachedir, packages_summary[i]["which"]),
            "-C",
            "%s/%s" % (rootdir, cachedir)
            ]
        try:
            subprocess.run(how_to, check=True)
        except subprocess.CalledProcessError:
            print("Failed to unpack package %s-%s." % (packages_summary[i]["name"], packages_summary[i]["version"]))
            return 1

# scripts("pre", "install")
# update("install", rootdir, cachedir, dbdir)
# scripts("post", "install")
