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

from Navegador import Navegador

import JAMediaObjects
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]


class JAMediaWeb(Gtk.Plug):

    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):
        """
        JAMediaWeb: Gtk.Plug para embeber en otra aplicacion.
        """

        Gtk.Plug.__init__(self, 0L)

        self.navegador = None
        self.show_all()
        self.connect("embedded", self.embed_event)

    def setup_init(self):
        self.navegador = Navegador()
        base_panel = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.navegador)
        base_panel.pack2(scroll, resize = True, shrink = True)

        self.add(base_panel)

        self.show_all()

        #self.navegador.connect("title-changed", self.set_titulo)
        #self.navegador.connect("load-finished", self.listo)
        #self.navegador.connect("load-started", self.cargando)
        #self.navegador.connect("load-progress-changed", self.set_progreso)
        #self.navegador.connect("load-error", self.error)
        #self.navegador.connect("download-requested", self.descargar_archivo, gtk.Window())
        #self.navegador.connect("create-web-view", self.ventana_con_webview)
        #self.navegador.connect("populate-popup", self.menu_webview)
        #self.navegador.connect("status-bar-text-changed", self.set_text_status)
        #self.navegador.connect("icon-loaded", self.favicon)

        #self.navegador.open('https://www.google.com/')
        #self.navegador.set_zoom_level(1.0)
        #print self.navegador.get_view_mode()
        #self.navegador.set_view_mode(WebKit.WebViewViewMode.FLOATING)

    def load(self, url):
        self.navegador.load(url)

    def anterior(self, widget):
        self.navegador.go_back()

    def siguiente(self, widget):
        self.navegador.go_forward()

    def recargar(self, widget):
        self.navegador.reload()

    def detener(self, widget):
        self.navegador.stop_loading()

    def acercar(self, widget):
        pass

    def alejar(self, widget):
        pass

    def embed_event(self, widget):
        print "JAMediaWeb => OK"

    def emit_salir(self, widget):
        self.emit('salir')
