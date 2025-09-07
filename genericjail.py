#!/usr/bin/env python3
from bubblebox import *
import os

import evdev
from evdev import InputDevice, categorize, ecodes

import glob

def list_gamepads():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    gamepads = []

    for device in devices:
        capabilities = device.capabilities()
        if ecodes.EV_KEY in capabilities:
            if ecodes.BTN_GAMEPAD in capabilities[ecodes.EV_KEY]:
                gamepads.append(device.path)

    return gamepads

sensitive = [HOME, "/tmp", XDG_RUNTIME_DIR, HOME + "/.ssh", HOME + "/.mozilla"]

cwd = os.getcwd()
dirname = cwd.split(os.path.sep)[-1].lower()

# for windows games
while dirname.startswith("bin") or dirname.startswith("engine")  or dirname.endswith("64") or dirname.endswith("86") or dirname.endswith("32"):
  cwd = os.path.dirname(cwd)
  dirname = cwd.split(os.path.sep)[-1].lower()


if any(s.startswith(cwd) for s in sensitive):
  raise Exception("Dont run it from sensitive dirs!")



bubblebox(

  bwrap_flags("--bind", HOME + "/sandbox/home", HOME),
  bwrap_flags("--dev-bind", HOME + "/sandbox/wine", HOME + "/.wine"),

  profiles.DESKTOP("genericjail"),

  host_access({
    cwd: Access.Write, # current dir

    #"/dev/input": Access.Device, # gamepads

    # wine ntsync
    "/dev/ntsync": Access.Device,

    "/opt": Access.Read, # some software

    "/dev/kfd": Access.Device, # AMD GPU compute
  }),

  # gamepads
  host_access({x: Access.Device for x in list_gamepads()}),
  host_access({x: Access.Device for x in glob.glob("/dev/hidraw*")}),


  #bwrap_flags("--unshare-user-try", "--unshare-pid", "" if os.getenv("sbnet") is not None else "--unshare-net", "--unshare-uts", "--unshare-cgroup-try", "--new-session"),
  bwrap_flags("--unshare-net") if not os.getenv("sbnet") else None,

  bwrap_flags("--setenv", "WINEDEBUG", "-all"),

  # gamemoded
  #dbus_proxy_flags("--talk=com.feralinteractive.GameMode",)

)
