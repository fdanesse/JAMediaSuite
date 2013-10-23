#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Make_doc.py por:
#       Flavio Danesse <fdanesse@gmail.com>, <fdanesse@activitycentral.com>
#       CeibalJAM - Uruguay - Activity Central

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
import pydoc

BASEPATH = os.path.dirname(__file__)
os.chdir(BASEPATH)

def get_modulo(name, attrib):
    
    modulo = False
    
    if len(name.split(".")) == 2:
        try:
            mod = __import__(name)
            modulo = mod.__getattribute__(name.replace("%s." % name.split(".")[0], ''))
        except:
            pass
    
    elif len(name.split(".")) == 1:
        try:
            modulo = __import__(name)
        except:
            pass
        
    else:
        pass
    
    if modulo:
        try:
            clase = getattr(modulo, attrib)

            archivo = os.path.join(BASEPATH, '%s.html' % attrib)
            ar = open(archivo, "w")
            ar.write("")
            ar.close()
            
            pydoc.writedoc(clase)
            
        except:
            sys.exit(0)
        
    else:
        sys.exit(0)
        
print get_modulo(sys.argv[1], sys.argv[2])
