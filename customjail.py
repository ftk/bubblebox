#!/usr/bin/env python3
from bubblebox import *
import os
import sys
from profiles import is_sensitive

args = sys.argv[1:]
change_dir = None
passthrough_dirs = []
argv = []
desktop = False
exclude_sensitive = True
network = False

# Parse command line arguments
i = 0
while i < len(args):
    arg = args[i]
    i += 1
    if arg == '-C' and i < len(args):
        change_dir = args[i]
        i += 1
    elif arg == '--desktop':
        desktop = True
    elif arg == '--network':
        network = True
    elif arg == '--allow-sensitive':
        exclude_sensitive = False
    elif arg == '--':
        argv = args[i:]
        break
    else:
        passthrough_dirs.append(arg)

if len(argv) == 0:
    print(f"USAGE: {sys.argv[0]} [-C <workdir>] [--allow-sensitive] [--desktop] [--network] <dir1> [<dir2>...] -- <program name> <program arguments>")
    sys.exit(2)

if exclude_sensitive:
    for dir in passthrough_dirs[:]:
        if is_sensitive(dir):
            print(f"{sys.argv[0]}: Directory {dir} removed because its considered sensitive")
            passthrough_dirs.remove(dir)

# Change working directory if specified
if change_dir:
    try:
        os.chdir(change_dir)
        print(f"{sys.argv[0]}: Changed working directory to: {change_dir}")
    except OSError as e:
        print(f"{sys.argv[0]}: Error changing directory: {e}", file=sys.stderr)
        sys.exit(1)



bubblebox(

  #bwrap_flags("--bind", HOME + "/sandbox/home", HOME),
  #bwrap_flags("--bind", HOME + "/sandbox/wine", HOME + "/.wine"),

  profiles.DESKTOP(argv[0]) if desktop else profiles.DEFAULT,

  host_access({x: Access.Device if x.startswith("/dev") else Access.Write for x in passthrough_dirs}),

  #bwrap_flags("--unshare-user-try", "--unshare-pid", "" if os.getenv("sbnet") is not None else "--unshare-net", "--unshare-uts", "--unshare-cgroup-try", "--new-session"),
  bwrap_flags("--unshare-net") if not network else None,

  argv = argv
)


