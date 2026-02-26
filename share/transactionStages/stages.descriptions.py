def downloads(packages_summary, repos_summary, rootdir, cachedir, dl_backend):
    # We are trying to use subprocess instead of os.system
    import subprocess
    import os
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
            subprocess.run(how_to, check=True)
        except subprocess.CalledProcessError:
            print("Downloading failed")
            return 1
    
verify(packages_summary, rootdir, cachedir, gpgdir)
scripts("pre", "install")
update("install", rootdir, cachedir, dbdir)
scripts("post", "install")