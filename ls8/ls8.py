"""#!/usr/bin/env python3"""

"""Main."""

import sys
from cpu import *
#sys.argv[0] = "ls8.py"
#sys.argv[1] = "print8.ls8"

cpu = CPU()

cpu.load()
cpu.run()
print("ls8 executed")