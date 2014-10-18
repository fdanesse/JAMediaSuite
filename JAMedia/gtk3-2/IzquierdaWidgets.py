#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   IzquierdaWidgets.py por:
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
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import GLib

from Globales import get_colors
from Globales import get_separador
from Globales import get_boton
from Globales import get_ip


def sensibilizar(objeto):
    if not objeto.get_sensitive():
        objeto.set_sensitive(True)


def insensibilizar(objeto):
    if objeto.get_sensitive():
        objeto.set_sensitive(False)


BASE_PATH = os.path.dirname(__file__)


class ToolbarGrabar(Gtk.EventBox):
    """
    Informa al usuario cuando se está grabando desde un streaming.
    """

    __gsignals__ = {
    "stop": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("drawingplayer"))

        self.colors = [get_colors("window"), get_colors("naranaja")]
        self.color = self.colors[0]

        self.toolbar = Gtk.Toolbar()
        self.toolbar.modify_bg(Gtk.StateType.NORMAL,
            get_colors("drawingplayer"))

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Detener")
        self.toolbar.insert(boton, -1)

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label("Grabador Detenido.")
        self.label.modify_fg(0, self.colors[0])
        self.label.show()
        item.add(self.label)
        self.toolbar.insert(item, -1)

        self.add(self.toolbar)

        self.show_all()

        boton.connect("clicked", self.__emit_stop)

    def __emit_stop(self, widget=None, event=None):
        self.stop()
        self.emit("stop")

    def __update(self):
        if self.color == self.colors[0]:
            self.color = self.colors[1]

        elif self.color == self.colors[1]:
            self.color = self.colors[0]

        self.label.modify_fg(Gtk.StateType.NORMAL, self.color)

        if not self.get_visible():
            self.show()

    def stop(self):
        self.color = self.colors[0]
        self.label.modify_fg(Gtk.StateType.NORMAL, self.color)
        self.label.set_text("Grabador Detenido.")
        self.hide()

    def set_info(self, datos):
        self.label.set_text(datos)
        self.__update()


class VideoVisor(Gtk.DrawingArea):

    __gsignals__ = {
    "ocultar_controles": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}

    def __init__(self):

        Gtk.DrawingArea.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("drawingplayer"))

        self.add_events(
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.KEY_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
            Gdk.EventMask.BUTTON_MOTION_MASK |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK
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


class ToolbarInfo(Gtk.EventBox):

    __gsignals__ = {
    'rotar': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'actualizar_streamings': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        toolbar = Gtk.Toolbar()

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(Gtk.StateType.NORMAL, get_colors("toolbars"))

        self.ocultar_controles = False

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        self.boton_izquierda = get_boton(archivo, flip=False, pixels=24)
        self.boton_izquierda.set_tooltip_text("Izquierda")
        self.boton_izquierda.connect("clicked", self.__emit_rotar)
        toolbar.insert(self.boton_izquierda, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        self.boton_derecha = get_boton(archivo, flip=True, pixels=24)
        self.boton_derecha.set_tooltip_text("Derecha")
        self.boton_derecha.connect("clicked", self.__emit_rotar)
        toolbar.insert(self.boton_derecha, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        label = Gtk.Label("Ocultar Controles:")
        label.modify_fg(0, get_colors("drawingplayer"))
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        switch = Gtk.CheckButton()
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "iconplay.svg")
        self.descarga = get_boton(archivo, flip=False,
            rotacion=GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE, pixels=24)
        self.descarga.set_tooltip_text("Actualizar Streamings")
        self.descarga.set_sensitive(False)
        self.descarga.connect("clicked", self.__emit_actualizar_streamings)
        toolbar.insert(self.descarga, -1)

        self.add(toolbar)
        self.show_all()

        switch.connect('button-press-event', self.__set_controles_view)
        GLib.timeout_add(2000, self.__check_ip)

    def __check_ip(self):
        if get_ip():
            self.descarga.set_sensitive(True)
        else:
            self.descarga.set_sensitive(False)
        return True

    def __emit_actualizar_streamings(self, widget):
        self.emit('actualizar_streamings')

    def __emit_rotar(self, widget):
        if widget == self.boton_derecha:
            self.emit('rotar', "Derecha")
        elif widget == self.boton_izquierda:
            self.emit('rotar', "Izquierda")

    def __set_controles_view(self, widget, senial):
        self.ocultar_controles = not widget.get_active()

    def set_video(self, valor):
        if valor:
            map(sensibilizar, [self.boton_izquierda, self.boton_derecha])
        else:
            map(insensibilizar, [self.boton_izquierda, self.boton_derecha])


# FIXME: No lo estoy utilizando
class Efectos_en_Pipe(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("drawingplayer"))

        self.box = Gtk.HBox()

        self.add(self.box)
        self.show_all()

        #self.set_size_request(-1, 15)

    def clear(self):
        for child in self.box.get_children():
            self.box.remove(child)
            child.destroy()

        self.hide()

    def add_efecto(self, efecto):
        button = Gtk.Button(efecto)
        button.set_tooltip_text(efecto)
        self.box.pack_start(button, False, False, 0)
        self.show_all()

    def remover_efecto(self, efecto):
        for button in self.box.get_children():
            if button.get_tooltip_text() == efecto:
                self.box.remove(button)
                button.destroy()
                break

        if not self.box.get_children():
            self.hide()

    def get_efectos(self):
        efectos = []
        for button in self.box.get_children():
            efectos.append(button.get_label())

        return efectos


class BufferInfo(Gtk.EventBox):

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("windows"))
        self.set_border_width(4)

        self.escala = ProgressBar(
            Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0

        box = Gtk.EventBox()
        box.modify_bg(Gtk.StateType.NORMAL, get_colors("windows"))
        box.set_border_width(4)
        box.add(self.escala)

        frame = Gtk.Frame()
        frame.set_border_width(4)
        frame.set_label(" Cargando Buffer ... ")
        frame.set_label_align(0.0, 0.5)

        frame.add(box)
        self.add(frame)
        self.show_all()

    def set_progress(self, valor=0.0):
        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()

        if self.valor == 100.0:
            self.hide()

        else:
            self.show()


class ProgressBar(Gtk.Scale):

    def __init__(self, ajuste):

        Gtk.Scale.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.modify_bg(Gtk.StateType.NORMAL, get_colors("toolbars"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (10, 10)

        self.show_all()

    def do_draw(self, contexto):
        rect = self.get_allocation()
        w, h = (rect.width, rect.height)

        # Relleno de la barra
        ww = w - self.borde * 2
        hh = 10 #h - self.borde * 2
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
        #imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        #imgx = ximage
        #imgy = float(self.borde + hh / 2 - imgh / 2)
        #Gdk.cairo_set_source_pixbuf(contexto, self.pixbuf, imgx, imgy)
        contexto.paint()

        return True
