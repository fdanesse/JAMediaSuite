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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GLib

BASE_PATH = os.path.dirname(__file__)

#import JAMediaObjects
#from JAMediaObjects.JAMediaWidgets import JAMediaButton

from Globales import get_color
from Globales import get_separador
from Globales import get_boton


class PlayerControl(Gtk.Box):
    """
    Controles de reproduccion: play/pausa, stop, siguiente, atras.
    """

    __gsignals__ = {
    "activar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.botonatras = JAMediaToolButton(pixels=24)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "siguiente.svg")

        self.botonatras.set_imagen(
            archivo=archivo,
            flip=True,
            rotacion=False)

        self.botonatras.set_tooltip_text("Anterior")
        self.botonatras.connect("clicked", self.__clickenatras)
        self.pack_start(self.botonatras, False, True, 0)

        self.botonplay = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")

        self.botonplay.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

        self.botonplay.set_tooltip_text("Reproducir")
        self.botonplay.connect("clicked", self.__clickenplay_pausa)
        self.pack_start(self.botonplay, False, True, 0)

        self.botonsiguiente = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "siguiente.svg")

        self.botonsiguiente.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

        self.botonsiguiente.set_tooltip_text("Siguiente")
        self.botonsiguiente.connect("clicked", self.__clickensiguiente)
        self.pack_start(self.botonsiguiente, False, True, 0)

        self.botonstop = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")

        self.botonstop.set_imagen(
            archivo=archivo,
            flip=False,
            rotacion=False)

        self.botonstop.set_tooltip_text("Detener Reproducción")
        self.botonstop.connect("clicked", self.__clickenstop)
        self.pack_start(self.botonstop, False, True, 0)

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


class JAMediaToolButton(Gtk.ToolButton):
    """
    Toolbutton con drawingarea donde se
    dibuja una imagen con cairo.
    """

    def __init__(self, pixels=24):

        Gtk.ToolButton.__init__(self)

        self.imagen = Imagen_Button()
        self.set_icon_widget(self.imagen)
        self.imagen.show()

        self.set_size_request(pixels, pixels)
        self.imagen.set_size_request(pixels, pixels)

        self.show_all()

    def set_imagen(self, archivo=None, flip=False, rotacion=False):

        if archivo == None:
            pixbuf = None

        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(archivo))

            if flip:
                pixbuf = pixbuf.flip(True)

            if rotacion:
                pixbuf = pixbuf.rotate_simple(rotacion)

        self.imagen.set_imagen(pixbuf)


class Imagen_Button(Gtk.DrawingArea):
    """
    DrawingArea de JAMediaToolButton.
    """

    def __init__(self):

        Gtk.DrawingArea.__init__(self)

        self.pixbuf = None

        self.show_all()

    def do_draw(self, context):

        if self.pixbuf != None:
            rect = self.get_allocation()
            x, y, w, h = (rect.x, rect.y, rect.width, rect.height)
            ww, hh = self.pixbuf.get_width(), self.pixbuf.get_height()

            scaledPixbuf = self.pixbuf.scale_simple(
                w, h, GdkPixbuf.InterpType.BILINEAR)

            import cairo

            surface = cairo.ImageSurface(
                cairo.FORMAT_ARGB32,
                scaledPixbuf.get_width(),
                scaledPixbuf.get_height())

            tmpcontext = cairo.Context(surface)
            Gdk.cairo_set_source_pixbuf(tmpcontext, scaledPixbuf, 0, 0)
            tmpcontext.paint()
            context.set_source_surface(surface)
            context.paint()

    def set_imagen(self, pixbuf):

        self.pixbuf = pixbuf
        self.queue_draw()
