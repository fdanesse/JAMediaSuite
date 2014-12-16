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
import gtk
import gobject

from Globales import get_colors
from Globales import get_separador
from Globales import get_boton


def sensibilizar(objeto):
    if not objeto.get_sensitive():
        objeto.set_sensitive(True)


def insensibilizar(objeto):
    if objeto.get_sensitive():
        objeto.set_sensitive(False)


BASE_PATH = os.path.dirname(os.path.realpath(__file__))


class ToolbarGrabar(gtk.EventBox):
    """
    Informa al usuario cuando se está grabando desde un streaming.
    """

    __gsignals__ = {
    "stop": (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.colors = [get_colors("window"), get_colors("naranaja")]
        self.color = self.colors[0]

        self.toolbar = gtk.Toolbar()
        self.toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Detener")
        self.toolbar.insert(boton, -1)

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("Grabador Detenido.")
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

        self.label.modify_fg(0, self.color)

        if not self.get_visible():
            self.show()

    def stop(self):
        self.color = self.colors[0]
        self.label.modify_fg(0, self.color)
        self.label.set_text("Grabador Detenido.")
        self.hide()

    def set_info(self, datos):
        self.label.set_text(datos)
        self.__update()


class VideoVisor(gtk.DrawingArea):

    __gsignals__ = {
    "ocultar_controles": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.add_events(
            gtk.gdk.KEY_PRESS_MASK |
            gtk.gdk.KEY_RELEASE_MASK |
            gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_MOTION_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK
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
            return True
        else:
            self.emit("ocultar_controles", True)
            return True


class ToolbarInfo(gtk.EventBox):

    __gsignals__ = {
    'rotar': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'actualizar_streamings': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

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

        item = gtk.ToolItem()
        label = gtk.Label("Ocultar Controles:")
        label.modify_fg(0, get_colors("drawingplayer"))
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        switch = gtk.CheckButton()
        item = gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "iconplay.svg")
        self.descarga = get_boton(archivo, flip=False,
            rotacion=gtk.gdk.PIXBUF_ROTATE_CLOCKWISE, pixels=24)
        self.descarga.set_tooltip_text("Actualizar Streamings")
        self.descarga.set_sensitive(False)
        self.descarga.connect("clicked", self.__emit_actualizar_streamings)
        toolbar.insert(self.descarga, -1)

        self.add(toolbar)
        self.show_all()

        switch.connect('button-press-event', self.__set_controles_view)

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

    def set_ip(self, valor):
        self.descarga.set_sensitive(valor)


# FIXME: No lo estoy utilizando
class Efectos_en_Pipe(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.box = gtk.HBox()

        self.add(self.box)
        self.show_all()
        #self.set_size_request(-1, 15)

    def clear(self):
        for child in self.box.get_children():
            self.box.remove(child)
            child.destroy()
        self.hide()

    def add_efecto(self, efecto):
        button = gtk.Button(efecto)
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


class BufferInfo(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("windows"))
        self.set_border_width(4)

        self.escala = ProgressBar(
            gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0

        box = gtk.EventBox()
        box.modify_bg(gtk.STATE_NORMAL, get_colors("windows"))
        box.set_border_width(4)
        box.add(self.escala)

        frame = gtk.Frame()
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


class ProgressBar(gtk.HScale):

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (10, 10)

        #icono = os.path.join(BASE_PATH, "Iconos", "controlslicer.svg")
        #self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 24, 24)

        self.connect("expose_event", self.__expose)

        self.show_all()
        self.set_sensitive(False)

    def __expose(self, widget, event):
        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        # todo el widget
        gc.set_rgb_fg_color(get_colors("toolbars"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        # vacio
        gc.set_rgb_fg_color(get_colors("drawingplayer"))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        # progreso
        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(get_colors("naranaja"))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # borde de progreso
        gc.set_rgb_fg_color(get_colors("window"))
        self.window.draw_rectangle(gc, False, xx, yy, ww, hh)

        # La Imagen
        #imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        #yimage = yy + hh / 2 - imgh / 2

        #self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
        #    imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True
