#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ProgressPlayer.py por:
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
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

from Globales import get_colors

BASE_PATH = os.path.dirname(__file__)


class ProgressPlayer(Gtk.EventBox):

    __gsignals__ = {
    "seek": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, )),
    "volumen": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("toolbars"))

        self.barraprogreso = BarraProgreso()
        self.volumen = ControlVolumen()

        hbox = Gtk.HBox()
        hbox.pack_start(self.barraprogreso, True, True, 0)
        hbox.pack_start(self.volumen, False, False, 0)

        self.add(hbox)

        self.barraprogreso.connect("user-set-value", self.__user_set_value)
        self.volumen.connect("volumen", self.__set_volumen)

        self.show_all()

    def __user_set_value(self, widget=None, valor=None):
        self.emit("seek", valor)

    def __set_volumen(self, widget, valor):
        self.emit('volumen', valor)

    def set_progress(self, valor):
        self.barraprogreso.set_progress(valor)


class BarraProgreso(Gtk.EventBox):
    """
    Barra de progreso para mostrar estado de reproduccion.
    """

    __gsignals__ = {
    "user-set-value": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("toolbars"))

        self.escala = ProgressBar(
            Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0

        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)
        self.set_size_request(-1, 24)

    def __emit_valor(self, widget, valor):
        if self.valor != valor:
            self.valor = valor
            self.emit("user-set-value", self.valor)

    def set_progress(self, valor=0.0):
        if self.escala.presed:
            return

        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()


class ProgressBar(Gtk.Scale):
    """
    Escala de SlicerBalance.
    """

    __gsignals__ = {
    "user-set-value": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        Gtk.Scale.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("toolbars"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        # FIXME: Verificar
        self.presed = False
        self.ancho, self.borde = (10, 10)

        icono = os.path.join(BASE_PATH, "Iconos", "controlslicer.svg")
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, 24, 24)

        self.connect("button-press-event", self.__button_press_event)
        self.connect("button-release-event", self.__button_release_event)
        self.connect("motion-notify-event", self.__motion_notify_event)

        self.show_all()

    def __button_press_event(self, widget, event):
        self.presed = True

    def __button_release_event(self, widget, event):
        self.presed = False

    def __motion_notify_event(self, widget, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """

        if event.state == Gdk.ModifierType.MOD2_MASK | \
            Gdk.ModifierType.BUTTON1_MASK:
            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)

            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

    def do_draw(self, contexto):
        """
        Dibuja el estado de la barra de progreso.
        """

        rect = self.get_allocation()
        w, h = (rect.width, rect.height)

        # Relleno de la barra
        ww = w - self.borde * 2
        hh = 10  #h - self.borde * 2
        Gdk.cairo_set_source_color(contexto, get_colors("drawingplayer"))
        rect = Gdk.Rectangle()
        rect.x, rect.y, rect.width, rect.height = (
            self.borde, self.borde, ww, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()

        # Relleno de la barra segun progreso
        Gdk.cairo_set_source_color(contexto, get_colors("naranaja"))
        rect = Gdk.Rectangle()
        ximage = int(self.get_adjustment().get_value() * ww / 100)
        rect.x, rect.y, rect.width, rect.height = (self.borde, self.borde,
            ximage, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()

        # borde del progreso
        Gdk.cairo_set_source_color(contexto, get_colors("window"))
        rect = Gdk.Rectangle()
        rect.x, rect.y, rect.width, rect.height = (
            self.borde, self.borde, ww, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.stroke()

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        imgx = ximage
        imgy = float(self.borde + hh / 2 - imgh / 2)
        Gdk.cairo_set_source_pixbuf(contexto, self.pixbuf, imgx, imgy)
        contexto.paint()

        return True


class ControlVolumen(Gtk.VolumeButton):

    __gsignals__ = {
    "volumen": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}

    def __init__(self):

        Gtk.VolumeButton.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("toolbars"))

        self.connect("value-changed", self.__value_changed)
        self.show_all()

        self.set_value(0.1)

    def __value_changed(self, widget, valor):
        """
        Cuando el usuario desplaza la escala.
        """

        valor = int(valor * 10)
        self.emit('volumen', valor)
