#!/bin/python3
from bubblebox import *
import os

bubblebox(
  profiles.DESKTOP("gamejail"),
  dbus_proxy_flags("--own=com.steampowered.*"),

  host_access({

    "/dev/input": Access.Device, # gamepads
    "/dev/winesync": Access.Device,
    "/dev/ntsync": Access.Device,

  }),

  home_access({
    ".steam": Access.Write,
    ".local/share/Steam": Access.Write,
  }),

   #bwrap_flags("--setenv", "PROTON_USE_WINESYNC", "1"),

)


