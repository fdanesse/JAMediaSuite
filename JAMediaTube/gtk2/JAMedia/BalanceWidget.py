#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BalanceWidget.py por:
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

"""
Descripción:

Contiene Widgets para controlar:
    brillo
    contraste
    hue
    saturación
    gamma

    Utilice:
        set_balance(self, brillo=None, contraste=None,
            saturacion=None, hue=None, gamma=None)

            para setear los valores en los widgets.

    Conéctese a la señal:
        'balance-valor': gobject.TYPE_FLOAT, gobject.TYPE_STRING

            para obtener los valores del widgets de cada propiedad según
            cambios del usuario sobre el widget.
"""

import os
import gtk
import gobject

from Globales import get_colors

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class BalanceWidget(gtk.EventBox):

    __gsignals__ = {
    'balance-valor': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
        (gobject.TYPE_FLOAT, gobject.TYPE_STRING))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        tabla = gtk.Table(rows=5, columns=1, homogeneous=True)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        tabla.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.brillo = ToolbarcontrolValores("Brillo")
        self.contraste = ToolbarcontrolValores("Contraste")
        self.saturacion = ToolbarcontrolValores("Saturación")
        self.hue = ToolbarcontrolValores("Matíz")
        self.gamma = ToolbarcontrolValores("Gamma")

        tabla.attach(self.brillo, 0, 1, 0, 1)
        tabla.attach(self.contraste, 0, 1, 1, 2)
        tabla.attach(self.saturacion, 0, 1, 2, 3)
        tabla.attach(self.hue, 0, 1, 3, 4)
        tabla.attach(self.gamma, 0, 1, 4, 5)

        self.add(tabla)
        self.show_all()

        self.set_size_request(150, -1)

        self.brillo.connect('valor', self.__emit_senial, 'brillo')
        self.contraste.connect('valor', self.__emit_senial, 'contraste')
        self.saturacion.connect('valor', self.__emit_senial, 'saturacion')
        self.hue.connect('valor', self.__emit_senial, 'hue')
        self.gamma.connect('valor', self.__emit_senial, 'gamma')

    def __emit_senial(self, widget, valor, tipo):
        self.emit('balance-valor', valor, tipo)

    def set_balance(self, brillo=50.0, contraste=50.0,
        saturacion=50.0, hue=50.0, gamma=10.0):
        if saturacion != None:
            self.saturacion.set_progress(saturacion)
        if contraste != None:
            self.contraste.set_progress(contraste)
        if brillo != None:
            self.brillo.set_progress(brillo)
        if hue != None:
            self.hue.set_progress(hue)
        if gamma != None:
            self.gamma.set_progress(gamma)


class ToolbarcontrolValores(gtk.Toolbar):

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self, label):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.titulo = label

        self.escala = SlicerBalance()

        item = gtk.ToolItem()
        item.set_expand(True)

        self.frame = gtk.Frame()
        self.frame.set_border_width(4)
        self.frame.set_label(self.titulo)
        self.frame.get_property("label-widget").modify_fg(
            0, get_colors("drawingplayer"))
        self.frame.set_label_align(0.5, 1.0)
        event = gtk.EventBox()
        event.set_border_width(4)
        event.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        event.add(self.escala)
        self.frame.add(event)
        self.frame.show_all()
        item.add(self.frame)
        self.insert(item, -1)

        self.show_all()

        self.escala.connect("user-set-value", self.__user_set_value)

    def __user_set_value(self, widget=None, valor=None):
        if valor > 99.4:
            valor = 100.0
        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def set_progress(self, valor):
        self.escala.set_progress(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))


class SlicerBalance(gtk.EventBox):

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.escala = BalanceBar(gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))

        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)

    def __emit_valor(self, widget, valor):
        self.emit("user-set-value", valor)

    def set_progress(self, valor=0.0):
        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()


class BalanceBar(gtk.HScale):

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (7, 10)

        icono = os.path.join(BASE_PATH, "Iconos", "controlslicer.svg")
        self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 16, 16)

        self.connect("expose_event", self.__expose)

        self.show_all()

    def __expose(self, widget, event):
        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        gc.set_rgb_fg_color(get_colors("window"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        gc.set_rgb_fg_color(get_colors("drawingplayer"))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(get_colors("naranaja"))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """
        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:
            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)
            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)
