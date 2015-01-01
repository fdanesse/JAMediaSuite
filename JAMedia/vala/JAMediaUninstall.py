#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands
import platform

print "Desinstalando JAMedia de:", platform.platform()
print commands.getoutput('rm -r /usr/local/share/JAMedia')
print commands.getoutput('rm /usr/share/applications/JAMedia.desktop')
print commands.getoutput('rm /usr/local/bin/jamedia_run.sh')
print commands.getoutput('rm /usr/local/bin/jamedia_uninstall.sh')
print "JAMedia se ha Desinstalado Correctamente del Sistema"
