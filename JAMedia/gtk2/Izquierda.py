#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Izquierda.py por:
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

import gtk
import gobject

from IzquierdaWidgets import ToolbarGrabar
from IzquierdaWidgets import VideoVisor
#from IzquierdaWidgets import Efectos_en_Pipe
from IzquierdaWidgets import BufferInfo
from IzquierdaWidgets import ToolbarInfo
from ProgressPlayer import ProgressPlayer
from Globales import get_colors


def ocultar(objeto):
    if objeto.get_visible():
        objeto.hide()


def mostrar(objeto):
    if not objeto.get_visible():
        objeto.show()


class Izquierda(gtk.EventBox):

    __gsignals__ = {
    "show-controls": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    'rotar': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'actualizar_streamings': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    'stop-record': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "seek": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, )),
    "volumen": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        vbox = gtk.VBox()

        self.toolbar_record = ToolbarGrabar()
        self.video_visor = VideoVisor()
        #self.efectos_aplicados = Efectos_en_Pipe()
        self.buffer_info = BufferInfo()
        self.toolbar_info = ToolbarInfo()
        self.progress = ProgressPlayer()

        vbox.pack_start(self.toolbar_record, False, False, 0)
        vbox.pack_start(self.video_visor, True, True, 0)
        #vbox.pack_start(self.efectos_aplicados, False, False, 0)
        vbox.pack_start(self.buffer_info, False, False, 0)
        vbox.pack_start(self.toolbar_info, False, False, 0)
        vbox.pack_start(self.progress, False, False, 0)

        self.add(vbox)
        self.show_all()

        self.toolbar_record.connect("stop", self.__emit_stop_record)

        self.video_visor.connect("ocultar_controles",
            self.__emit_show_controls)
        self.video_visor.connect("button_press_event", self.__set_fullscreen)

        self.toolbar_info.connect("rotar", self.__emit_rotar)
        self.toolbar_info.connect("actualizar_streamings",
            self.__emit_actualizar_streamings)

        self.progress.connect("seek", self.__emit_seek)
        self.progress.connect("volumen", self.__emit_volumen)

    def __emit_volumen(self, widget, valor):
        self.emit('volumen', valor)

    def __emit_seek(self, widget, valor):
        self.emit("seek", valor)

    def __emit_stop_record(self, widget):
        self.emit("stop-record")

    def __emit_actualizar_streamings(self, widget):
        self.emit('actualizar_streamings')

    def __emit_rotar(self, widget, sentido):
        self.emit('rotar', sentido)

    def __set_fullscreen(self, widget, event):
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            win = self.get_toplevel()
            widget.set_sensitive(False)
            screen = win.get_screen()
            w, h = win.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            if ww == w and hh == h:
                win.set_border_width(2)
                gobject.idle_add(self.__set_full, win, False)
            else:
                win.set_border_width(0)
                gobject.idle_add(self.__set_full, win, True)
            widget.set_sensitive(True)

    def __set_full(self, win, valor):
        if valor:
            win.fullscreen()
        else:
            win.unfullscreen()

    def __emit_show_controls(self, widget, valor):
        zona, ocultar = (valor, self.toolbar_info.ocultar_controles)
        self.emit("show-controls", (zona, ocultar))

    def setup_init(self):
        map(ocultar, [self.toolbar_record, self.buffer_info])
        #, self.efectos_aplicados])
        self.toolbar_info.set_video(False)
        self.progress.set_sensitive(False)

    def set_ip(self, valor):
        self.toolbar_info.set_ip(valor)
