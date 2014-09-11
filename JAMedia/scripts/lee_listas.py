#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shelve

path = "/home/flavio/JAMediaDatos/Datos/JAMediaTV.JAMedia"
archivo = shelve.open(path)
#archivo.clear()
for key in sorted(archivo.keys()):
    print "%s,%s" % (key, archivo[key])
archivo.close()
