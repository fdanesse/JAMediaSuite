#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWeb.py por:
#   Flavio Danesse <fdanesse@activitycentral.com>
#   CeibalJAM - Uruguay - Activity Central

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

import gi
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import WebKit

import JAMediaObjects
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class JAMediaWeb(Gtk.Plug):
    
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """JAMediaWeb: Gtk.Plug para embeber en otra aplicacion."""
        
        Gtk.Plug.__init__(self, 0L)
        
        self.navegador = None
        
        self.show_all()
        
        self.connect("embedded", self.embed_event)
        
    def setup_init(self):
        """Se crea la interfaz grafica,
        se setea y se empaqueta todo."""
        
        self.navegador = WebKit.WebView()
        
        base_panel = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        
        # Izquierda
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        #scroll.add_with_viewport (self.lista_de_reproduccion)
        
        base_panel.pack1(scroll, resize = True, shrink = True)
        
        # Derecha
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport (self.navegador)
        
        base_panel.pack2(scroll, resize = True, shrink = True)
        
        self.add(base_panel)
        self.show_all()
        self.navegador.open('https://www.google.com/')
        
    def embed_event(self, widget):
        """No hace nada por ahora."""
        
        print "JAMediaWeb => OK"
        
    def emit_salir(self, widget):
        """Emite salir para que cuando esta embebida, la
        aplicacion decida que hacer, si salir, o cerrar solo
        JAMediaWeb."""
                
        self.emit('salir')
        