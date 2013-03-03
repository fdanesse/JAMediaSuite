#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
#   Flavio Danesse <fdanesse@activitycentral.com>
#   CeibalJAM - Uruguay - Activity Central
#
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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from Widgets import ToolbarTry
from Widgets import Navegador

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir

JAMediaObjectsPath = JAMediaObjects.__path__[0]
    
GObject.threads_init()
Gdk.threads_init()

class JAMediaPygiHack(Gtk.Plug):
    
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Plug.__init__(self, 0L)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbartry = ToolbarTry()
        self.navegador = Navegador()
        
        vbox.pack_start(self.navegador, True, True, 0)
        vbox.pack_start(self.toolbartry, False, False, 3)
        
        self.add(vbox)
        self.show_all()
        
        self.navegador.connect('info', self.get_info)
        self.connect("embedded", self.embed_event)
        
    def embed_event(self, widget):
        """No hace nada por ahora."""
        
        print "JAMediaPygiHack => OK"
    
    def get_info(self, widget, objeto):
        
        self.toolbartry.label.set_text( str(objeto) )
