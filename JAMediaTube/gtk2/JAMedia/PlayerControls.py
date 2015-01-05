#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PlayerControls.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import gtk
import gobject

from Globales import get_colors


def sensibilizar(objeto):
    if not objeto.get_sensitive():
        objeto.set_sensitive(True)


def insensibilizar(objeto):
    if objeto.get_sensitive():
        objeto.set_sensitive(False)


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class PlayerControls(gtk.EventBox):
    """
    Controles de reproduccion: play/pausa, stop, siguiente, atras.
    """

    __gsignals__ = {
    "accion-controls": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        vbox = gtk.HBox()

        self.pix_play = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(BASE_PATH, "Iconos", "play.svg"), 24, 24)
        self.pix_paused = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(BASE_PATH, "Iconos", "pausa.svg"), 24, 24)

        self.atras = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "siguiente.svg")
        self.atras.set_imagen(archivo=archivo, flip=True, rotacion=False)
        self.atras.set_tooltip_text("Anterior")
        self.atras.connect("clicked", self.__emit_accion, "atras")
        vbox.pack_start(self.atras, False, True, 0)

        self.play = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")
        self.play.set_imagen(archivo=archivo, flip=False, rotacion=False)
        self.play.set_tooltip_text("Reproducir")
        self.play.connect("clicked", self.__emit_accion, "pausa-play")
        vbox.pack_start(self.play, False, True, 0)

        self.siguiente = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "siguiente.svg")
        self.siguiente.set_imagen(archivo=archivo, flip=False, rotacion=False)
        self.siguiente.set_tooltip_text("Siguiente")
        self.siguiente.connect("clicked", self.__emit_accion, "siguiente")
        vbox.pack_start(self.siguiente, False, True, 0)

        self.stop = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")
        self.stop.set_imagen(archivo=archivo, flip=False, rotacion=False)
        self.stop.set_tooltip_text("Detener Reproducción")
        self.stop.connect("clicked", self.__emit_accion, "stop")
        vbox.pack_start(self.stop, False, True, 0)

        self.add(vbox)
        self.show_all()

    def __emit_accion(self, widget, accion):
        self.emit("accion-controls", accion)

    def set_paused(self):
        self.play.set_paused(self.pix_play)

    def set_playing(self):
        self.play.set_playing(self.pix_paused)

    def activar(self, valor):
        if valor == 0:
            map(insensibilizar, [self.atras, self.play,
                self.siguiente, self.stop])
        elif valor == 1:
            map(insensibilizar, [self.atras, self.siguiente])
            map(sensibilizar, [self.play, self.stop])
        else:
            map(sensibilizar, [self.atras, self.play,
                self.siguiente, self.stop])


class JAMediaToolButton(gtk.ToolButton):

    def __init__(self, pixels=34):

        gtk.ToolButton.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.estado = False
        self.pixels = pixels
        self.imagen = gtk.Image()
        self.set_icon_widget(self.imagen)
        self.imagen.show()

        self.imagen.set_size_request(self.pixels, self.pixels)
        self.show_all()

    def set_imagen(self, archivo=None, flip=False, rotacion=False):
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(archivo), self.pixels, self.pixels)
        if flip:
            pixbuf = pixbuf.flip(True)
        if rotacion:
            pixbuf = pixbuf.rotate_simple(rotacion)
        self.imagen.set_from_pixbuf(pixbuf)

    def set_playing(self, pixbuf):
        if self.estado:
            return
        self.estado = True
        self.imagen.set_from_pixbuf(pixbuf)

    def set_paused(self, pixbuf):
        if not self.estado:
            return
        self.estado = False
        self.imagen.set_from_pixbuf(pixbuf)
