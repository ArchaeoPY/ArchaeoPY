# -*- coding: utf-8 -*-

import sys, string, os


# Local variables...

script = 'pyuic4 -o'
uiFile = ' mpl.ui'
pyFile = ' mpl.py'

script = script + pyFile + uiFile

print script

os.system(script)

