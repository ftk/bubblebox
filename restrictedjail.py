#!/usr/bin/env python3
from bubblebox import *
import os



bubblebox(
  bwrap_flags("--bind", HOME + "/sandbox/home", HOME),

  profiles.DEFAULT,
  WORKDIR(),

  host_access({
    os.getcwd(): Access.Write, # current dir

    "/opt": Access.Read, # some software

    "/dev/kfd": Access.Device, # GPU compute
  }),
  bwrap_flags("--unshare-net") if os.getenv("sbnet") is  None else None,

)

