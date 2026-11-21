def main(os_summary):
    import subprocess
    rootdir = os_summary[rootdir]
    cachedir = os_summary[cachedir]

    target = "%s/%s/" % (rootdir, cachedir)
    print("By continuing, this directory will be cleaned:")
    print()
    print("     %s" % target)
    print()

    confirmed = False
    while not confirmed:
        print("Would you like to continue?", end=" ")
        confirm = input("[Y/n]")
        if confirm in ["Y", "y", "yes", ""]:
            confirmed = True
        elif confirm in ["N", "n", "no"]:
            print("Operation aborted.")
            return 0
        else:
            print("Sorry, can't understand \"%s\"" % confirm)
    
    # clean up
    how_to = ["rm", "-rf" "%s/*" % target]

    try:
        subprocess.run(how_to, check=True)
    except subprocess.CalledProcessError:
        print("Failed to clean cache directory.")
        return 1
    
    # Finished without error.
    print("Completed!")
    return 0