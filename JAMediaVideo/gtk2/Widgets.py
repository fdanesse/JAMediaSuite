#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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

import os

import gtk
from gtk import gdk
import gobject

from Globales import get_separador
from Globales import get_boton
from Globales import get_color
from Globales import get_colors

BASE_PATH = os.path.dirname(__file__)


class Visor(gtk.DrawingArea):
    """
    Visor generico para utilizar como area de
    reproduccion de videos o dibujar.
    """

    __gsignals__ = {
    "ocultar_controles": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.add_events(
            gdk.KEY_PRESS_MASK |
            gdk.KEY_RELEASE_MASK |
            gdk.POINTER_MOTION_MASK |
            gdk.POINTER_MOTION_HINT_MASK |
            gdk.BUTTON_MOTION_MASK |
            gdk.BUTTON_PRESS_MASK |
            gdk.BUTTON_RELEASE_MASK
        )

        self.show_all()

    def do_motion_notify_event(self, event):
        """
        Cuando se mueve el mouse sobre el visor.
        """

        x, y = (int(event.x), int(event.y))
        rect = self.get_allocation()
        xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)

        if x in range(ww - 60, ww) or y in range(yy, yy + 60) \
            or y in range(hh - 60, hh):

            self.emit("ocultar_controles", False)
            return

        else:
            self.emit("ocultar_controles", True)
            return

'''
class JAMediaButton(gtk.EventBox):
    """
    Un Boton a medida.
    """

    __gsignals__ = {
    "clicked": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    "click_derecho": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.cn = get_color("BLANCO")
        self.cs = get_color("AMARILLO")
        self.cc = get_color("NARANJA")
        self.text_color = get_color("NEGRO")
        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.set_visible_window(True)
        self.modify_bg(0, self.colornormal)
        self.modify_fg(0, self.text_color)
        self.set_border_width(1)

        self.estado_select = False

        self.add_events(
            gdk.BUTTON_PRESS_MASK |
            gdk.BUTTON_RELEASE_MASK |
            gdk.POINTER_MOTION_MASK |
            gdk.ENTER_NOTIFY_MASK |
            gdk.LEAVE_NOTIFY_MASK)

        self.connect("button_press_event", self.button_press)
        self.connect("button_release_event", self.__button_release)
        self.connect("enter-notify-event", self.__enter_notify_event)
        self.connect("leave-notify-event", self.__leave_notify_event)

        self.imagen = gtk.Image()
        self.add(self.imagen)

        self.show_all()

    def set_colores(self, colornormal=False,
        colorselect=False, colorclicked=False):

        if colornormal:
            self.cn = colornormal

        if colorselect:
            self.cs = colorselect

        if colorclicked:
            self.cc = colorclicked

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        if self.estado_select:
            self.seleccionar()

        else:
            self.des_seleccionar()

    def seleccionar(self):
        """
        Marca como seleccionado
        """

        self.estado_select = True
        self.colornormal = self.cc
        self.colorselect = self.cc
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def des_seleccionar(self):
        """
        Desmarca como seleccionado
        """

        self.estado_select = False

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def __button_release(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def __leave_notify_event(self, widget, event):

        self.modify_bg(0, self.colornormal)

    def __enter_notify_event(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def button_press(self, widget, event):

        self.seleccionar()

        if event.button == 1:
            self.emit("clicked", event)

        elif event.button == 3:
            self.emit("click_derecho", event)

    def set_tooltip(self, texto):

        self.set_tooltip_text(texto)

    def set_label(self, texto):

        for child in self.get_children():
            child.destroy()

        label = gtk.Label(texto)
        label.show()
        self.add(label)

    def set_imagen(self, archivo):

        self.imagen.set_from_file(archivo)

    def set_tamanio(self, w, h):

        self.set_size_request(w, h)


class WidgetEfecto_en_Pipe(JAMediaButton):
    """
    Representa un efecto agregado al pipe de JAMediaVideo.
    Es simplemente un objeto gráfico que se agrega debajo del
    visor de video, para que el usuario tenga una referencia de
    los efectos que ha agregado y en que orden se encuentran.
    """

    def __init__(self):

        JAMediaButton.__init__(self)

        self.show_all()

        self.set_colores(
            colornormal=get_color("NEGRO"),
            colorselect=get_color("NEGRO"),
            colorclicked=get_color("NEGRO"))

        self.modify_bg(0, self.colornormal)

    def seleccionar(self):
        pass

    def des_seleccionar(self):
        pass
'''
