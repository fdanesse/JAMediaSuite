#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PlayerNull.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
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

import cairo
import gobject


def paint_text(contexto, texto, rect):
    contexto.set_source_rgba(0, 0, 0, 1)
    x, y, w, h = (rect)
    posx, posy = (-10, 0)

    for linea in texto:
        (nx, ny, width, height, dx, dy) = contexto.text_extents(linea)
        posy += height + height
        contexto.move_to(posx, posy)
        contexto.show_text(linea)


def resize_font(font_size, contexto, texto):

    contexto.set_font_size(font_size)
    ancho, alto = (0, 0)

    for linea in texto:
        nx, ny, width, height, dx, dy = contexto.text_extents(linea)

        if width > ancho:
            ancho = width

        if height > alto:
            alto = height

    alto = alto * len(texto) + (alto * len(texto))
    ancho += 30

    return (ancho, alto)


def get_text_path(contexto, texto, rect):

    font_size = 50
    x, y, w, h = (rect)
    lineas = texto.split("\n")
    ancho, alto = resize_font(font_size, contexto, lineas)

    while ancho > w or alto > h:
        font_size -= 1
        ancho, alto = resize_font(font_size, contexto, lineas)

    paint_text(contexto, lineas, rect)


class Player(gobject.GObject):

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_STRING,)),
    "newposicion": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_INT,)),
    "volumen": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_FLOAT,)),
    "video": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,
        (gobject.TYPE_BOOLEAN,))}

    def __init__(self, ventana):

        gobject.GObject.__init__(self)

        self.name = "PlayerNull"
        self.ventana = ventana

        # FIXME: Corregir o eliminar
        #self.ventana.connect('draw', self.paint)

        self.config = {
            'saturacion': 1.0,
            'contraste': 1.0,
            'brillo': 0.0,
            'hue': 0.0,
            'gamma': 1.0
            }

        self.efectos = []
        self.config_efectos = {}

    def pintar_fondo(self, widget, contexto):

        rect = widget.get_allocation()
        w, h = (rect.width, rect.height)
        contexto.set_operator(cairo.OPERATOR_SOURCE)
        contexto.rectangle(0, 0, w, h)
        contexto.set_source_rgba(1, 1, 1, 1)
        contexto.fill()

    def paint(self, widget, contexto):
        texto = '''
        No tienes instalado un Reproductor que JAMedia pueda utilizar.

        Para que JAMedia funcione, debes instalar lo siguiente:

            mplayer
            gir1.2-gstreamer-1.0
            gir1.2-gst-plugins-base-1.0,
            gstreamer1.0-plugins-good,
            gstreamer1.0-plugins-ugly,
            gstreamer1.0-plugins-bad,
            gstreamer1.0-libav'''

        self.pintar_fondo(widget, contexto)
        rect = widget.get_allocation()
        x, y, w, h = (rect.x, rect.y, rect.width, rect.height)
        rect = (x, y, w, h)
        get_text_path(contexto, texto, rect)

    def set_pipeline(self):
        pass

    def sync_message(self, bus, mensaje):
        pass

    def on_mensaje(self, bus, mensaje):
        pass

    def load(self, uri):
        pass

    def play(self):
        pass

    def stop(self):
        pass

    def pause(self):
        pass

    def pause_play(self):
        pass

    def new_handle(self, reset):
        pass

    def handle(self):
        pass

    def set_position(self, posicion):
        pass

    def get_volumen(self):
        pass

    def set_volumen(self, valor):
        pass

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        pass

    def get_balance(self):

        return {
        'saturacion': 50.0,
        'contraste': 50.0,
        'brillo': 50.0,
        'hue': 50.0,
        'gamma': 10.0
        }

    def agregar_efecto(self, nombre_efecto):

        pass

    def quitar_efecto(self, indice_efecto):

        pass

    def configurar_efecto(self, nombre_efecto, propiedad, valor):

        pass

    def rotar(self, valor):
        pass


class Grabador(gobject.GObject):

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "endfile": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gobject.GObject.__init__(self)

        self.emit('update', "No Tienes un Grabador Instalado Actualmente.")

    def stop(self):
        pass


class JAMediaReproductor(Player):

    def __init__(self, ventana):

        Player.__init__(self, ventana)


class MplayerReproductor(Player):

    def __init__(self, ventana):

        Player.__init__(self, ventana)


class MplayerGrabador(Grabador):

    def __init__(self, uri, archivo):

        Grabador.__init__(self)


class JAMediaGrabador(Grabador):

    def __init__(self, uri, archivo):

        Grabador.__init__(self)
