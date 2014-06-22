#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PlayerControls.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

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

import gtk
from gtk import gdk
import gobject

from Globales import get_colors

BASE_PATH = os.path.dirname(__file__)
BASE_PATH = os.path.dirname(BASE_PATH)


class PlayerControl(gtk.EventBox):
    """
    Controles de reproduccion: play/pausa, stop, siguiente, atras.
    """

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("toolbars"))

        vbox = gtk.HBox()
        self.botonatras = JAMediaToolButton(pixels=24)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "siguiente.svg")

        self.botonatras.set_imagen(
            archivo=archivo,
            flip=True,
            rotacion=False)

        self.botonatras.set_tooltip_text("Anterior")
        self.botonatras.connect("clicked", self.__clickenatras)
        vbox.pack_start(self.botonatras, False, True, 0)

        self.botonplay = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")

        self.botonplay.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

        self.botonplay.set_tooltip_text("Reproducir")
        self.botonplay.connect("clicked", self.__clickenplay_pausa)
        vbox.pack_start(self.botonplay, False, True, 0)

        self.botonsiguiente = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "siguiente.svg")

        self.botonsiguiente.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

        self.botonsiguiente.set_tooltip_text("Siguiente")
        self.botonsiguiente.connect("clicked", self.__clickensiguiente)
        vbox.pack_start(self.botonsiguiente, False, True, 0)

        self.botonstop = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")

        self.botonstop.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

        self.botonstop.set_tooltip_text("Detener Reproducción")
        self.botonstop.connect("clicked", self.__clickenstop)
        vbox.pack_start(self.botonstop, False, True, 0)

        self.add(vbox)
        self.show_all()

    def set_paused(self):

        archivo = os.path.join(
            BASE_PATH, "Iconos", "play.svg")

        self.botonplay.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

    def set_playing(self):

        archivo = os.path.join(
            BASE_PATH, "Iconos", "pausa.svg")

        self.botonplay.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

    def __clickenstop(self, widget=None, event=None):
        self.emit("activar", "stop")

    def __clickenplay_pausa(self, widget=None, event=None):
        self.emit("activar", "pausa-play")

    def __clickenatras(self, widget=None, event=None):
        self.emit("activar", "atras")

    def __clickensiguiente(self, widget=None, event=None):
        self.emit("activar", "siguiente")


class JAMediaToolButton(gtk.ToolButton):
    """
    Toolbutton con drawingarea donde se
    dibuja una imagen con cairo.
    """

    def __init__(self, pixels=34):

        gtk.ToolButton.__init__(self)

        self.modify_bg(0, get_colors("toolbars"))

        self.imagen = Imagen_Button()
        self.set_icon_widget(self.imagen)
        self.imagen.show()

        self.imagen.set_size_request(pixels, pixels)

        self.show_all()

    def set_imagen(self, archivo=None, flip=False, rotacion=False):

        if archivo == None:
            pixbuf = None

        else:
            pixbuf = gdk.pixbuf_new_from_file(os.path.join(archivo))

            if flip:
                pixbuf = pixbuf.flip(True)

            if rotacion:
                pixbuf = pixbuf.rotate_simple(rotacion)

        self.imagen.set_imagen(pixbuf)


class Imagen_Button(gtk.DrawingArea):
    """
    DrawingArea de JAMediaToolButton.
    """

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(0, get_colors("toolbars"))

        self.pixbuf = None

        self.connect("expose-event", self.__expose_event)

        self.show_all()

    def __expose_event(self, widget, event):

        if not self.pixbuf:
            return True

        rect = self.get_allocation()
        x, y, w, h = (rect.x, rect.y, rect.width, rect.height)

        scaledPixbuf = self.pixbuf.scale_simple(
            w, h, gtk.gdk.INTERP_BILINEAR)

        gc = gtk.gdk.Drawable.new_gc(self.window)
        self.window.draw_pixbuf(gc, scaledPixbuf, 0, 0, 0, 0)

        return True

    def set_imagen(self, pixbuf):

        self.pixbuf = pixbuf
        self.queue_draw()
