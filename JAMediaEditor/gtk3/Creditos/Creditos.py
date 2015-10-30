#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Creditos.py por:
#    Flavio Danesse <fdanesse@gmail.com>

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
import cairo
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import GLib
from Player import Player

screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()

BASEPATH = os.path.dirname(__file__)


class Creditos(Gtk.Window):

    __gtype_name__ = 'JAMediaEditorCredits'

    def __init__(self, parent_window):

        Gtk.Window.__init__(self)

        self.set_title("Creditos")
        self.set_transient_for(parent_window)
        self.set_border_width(10)

        self.resize(820, h - 40)
        self.move(w / 2 - 410, 40)
        self.maximize()
        self.set_resizable(False)

        self.visor = Visor()
        self.player = Player()
        self.player.connect("endfile", self.__replay)

        self.add(self.visor)
        self.show_all()

        self.connect("key-press-event", self.__key_press_even)
        self.connect("delete-event", self.stop)

    def __key_press_even(self, widget, event):
        if Gdk.keyval_name(event.keyval) == "Escape":
            self.stop()
            self.destroy()
        return False

    def __replay(self, player):
        uri = os.path.join(BASEPATH, "Sonidos", "yarina.ogg")
        self.player.load(uri)

    def stop(self, widget=False, event=False):
        self.player.stop()
        self.visor.new_handle(False)
        self.hide()

    def run(self):
        self.show()
        self.visor.new_handle(True)
        uri = os.path.join(BASEPATH, "Sonidos", "yarina.ogg")
        self.player.load(uri)


class Visor(Gtk.DrawingArea):

    def __init__(self):

        Gtk.DrawingArea.__init__(self)

        self.posy = 200
        self.update = False
        self.imagen = False
        self.show_all()

    def __handle(self):
        try:
            cr = self.get_property("window").cairo_create()
            if not self.imagen:
                self.imagen = cairo.ImageSurface.create_from_png(
                    os.path.join(BASEPATH, "Imagenes", "creditos.png"))
            self.rect = self.get_allocation()
            cr.rectangle(self.rect.x, self.rect.y,
                self.rect.width, self.rect.height)
            ww = self.imagen.get_width()
            hh = self.imagen.get_height()
            x = self.rect.width / 2 - ww / 2
            cr.set_source_surface(self.imagen, x, self.posy)
            cr.fill()
            self.posy -= 1
            if self.posy < -hh:
                self.posy = h - 100
        except:
            pass
        return True

    def new_handle(self, reset):
        if self.update:
            GLib.source_remove(self.update)
            self.update = False
        if reset:
            self.posy = 300
            self.update = GLib.timeout_add(100, self.__handle)
