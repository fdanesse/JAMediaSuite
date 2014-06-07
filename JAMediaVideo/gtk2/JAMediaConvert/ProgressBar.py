#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ProgressBar.py por:
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


class ProgressBar(gtk.EventBox):

    #__gsignals__ = {
    #"user-set-value": (gobject.SIGNAL_RUN_CLEANUP,
    #    gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.escala = BalanceBar(gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))

        self.add(self.escala)
        self.show_all()

        #self.escala.connect('user-set-value', self.__emit_valor)

    def set_progress(self, valor=0.0):
        """
        El reproductor modifica la escala.
        """

        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()

    #def __emit_valor(self, widget, valor):
    #    """
    #    El usuario modifica la escala.
    #    Y se emite la señal con el valor (% float).
    #    """

    #    self.emit("user-set-value", valor)


class BalanceBar(gtk.HScale):
    """
    Escala de SlicerBalance.
    """

    #__gsignals__ = {
    #"user-set-value": (gobject.SIGNAL_RUN_CLEANUP,
    #    gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (7, 10)

        #icono = os.path.join(BASE_PATH,
        #    "Iconos", "controlslicer.svg")
        #self.pixbuf = gdk.pixbuf_new_from_file_at_size(icono,
        #    16, 16)

        self.connect("expose_event", self.__expose)

        self.show_all()

    #def do_motion_notify_event(self, event):
    #    """
    #    Cuando el usuario se desplaza por la barra de progreso.
    #    Se emite el valor en % (float).
    #    """

    #    if event.state == gdk.MOD2_MASK | \
    #        gdk.BUTTON1_MASK:

    #        rect = self.get_allocation()
    #        valor = float(event.x * 100 / rect.width)
    #        if valor >= 0.0 and valor <= 100.0:
    #            self.ajuste.set_value(valor)
    #            self.queue_draw()
    #            self.emit("user-set-value", valor)

    def __expose(self, widget, event):
        """
        Dibuja el estado de la barra de progreso.
        """

        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        gc.set_rgb_fg_color(gdk.color_parse("#ffffff"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        gc.set_rgb_fg_color(gdk.Color(0, 0, 0))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(gdk.Color(65000, 26000, 0))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # La Imagen
        #imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        #yimage = yy + hh / 2 - imgh / 2

        #self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
        #    imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True
