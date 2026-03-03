# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM stages description file.

def downloads(packages_summary, repos_summary, rootdir, cachedir, dl_backend):
    # We are trying to use subprocess instead of os.system
    import subprocess
    print("Downloading packages.")

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
    
def scripts(package_summary, status, action, rootdir, cachedir):
    import subprocess
    import os
    print("Running %s %s scripts" % (status, action))
    
    for i in range(len(package_summary)):
        scripts_directory = "%s/%s/%s/%s_%s" % (rootdir, cachedir, package_summary[i]["which"], status, action)
        if not os.path.isdir(scripts_directory):
            print("No %s %s scripts to be done with %s-%s" % (status, action, package_summary[i]["name"], package_summary[i]["version"]))
            continue
        else:
            for script in sorted(os.listdir(scripts_directory)):
                target = os.path.join(scripts_directory, script)
                if os.path.isfile(target) and os.access(target, os.X_OK):
                    try:
                        subprocess.run([target], check=True)
                    except subprocess.CalledProcessError:
                        print("Failed to run scripts (%s-%s, %s %s)" % (package_summary[i]["name"], package_summary[i]["version"], status, action))
                        return 1
        
# update("install", rootdir, cachedir, dbdir)
# scripts("post", "install")
