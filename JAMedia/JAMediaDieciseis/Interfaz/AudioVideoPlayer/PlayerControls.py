#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
from ..Globales import get_colors
from ..Globales import get_boton
from ..Globales import get_SeparatorToolItem
from ..Globales import get_ToggleToolButton

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONS = os.path.join(os.path.dirname(BASE_PATH), "Iconos")


class PlayerControls(gtk.Toolbar):
    """
    Controles de reproduccion: play/pausa, stop, siguiente, atras.
    """

    __gsignals__ = {
    "accion-controls": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.pix_play = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONS, "play.svg"), 24, 24)
        self.pix_paused = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(ICONS, "pausa.svg"), 24, 24)

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(ICONS, "siguiente.svg")
        self.atras = get_boton(archivo, flip=True,
            pixels=24, tooltip_text="Anterior")
        self.atras.connect("clicked", self.__emit_accion, "atras")
        self.insert(self.atras, -1)

        archivo = os.path.join(ICONS, "play.svg")
        self.play = JAMediaToolButton(archivo, pixels=24,
            tooltip_text="Reproducir")
        self.play.connect("clicked", self.__emit_accion, "pausa-play")
        self.insert(self.play, -1)

        archivo = os.path.join(ICONS, "siguiente.svg")
        self.siguiente = get_boton(archivo, flip=False,
            pixels=24, tooltip_text="Siguiente")
        self.siguiente.connect("clicked", self.__emit_accion, "siguiente")
        self.insert(self.siguiente, -1)

        archivo = os.path.join(ICONS, "stop.svg")
        self.stop = get_boton(archivo, flip=False,
            pixels=24, tooltip_text="Detener")
        self.stop.connect("clicked", self.__emit_accion, "stop")
        self.insert(self.stop, -1)

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=10, expand=False), -1)

        archivo = os.path.join(ICONS, "rotar.svg")
        self.izquierda = get_boton(archivo, flip=False,
            pixels=24, tooltip_text="Rotar a la Izquierda")
        self.izquierda.connect("clicked", self.__emit_accion, "Izquierda")
        self.insert(self.izquierda, -1)

        archivo = os.path.join(ICONS, "rotar.svg")
        self.derecha = get_boton(archivo, flip=True,
            pixels=24, tooltip_text="Rotar a la Derecha")
        self.derecha.connect("clicked", self.__emit_accion, "Derecha")
        self.insert(self.derecha, -1)

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=10, expand=False), -1)

        item = gtk.ToolItem()
        self.volumen = ControlVolumen()
        item.add(self.volumen)
        self.insert(item, -1)

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=10, expand=False), -1)

        archivo = os.path.join(ICONS, "lista.svg")
        self.lista = get_ToggleToolButton(archivo, flip=False,
            pixels=24, tooltip_text="Lista Siempre Visible")
        self.lista.connect("toggled", self.__emit_accion, "showlist")
        self.insert(self.lista, -1)

        archivo = os.path.join(ICONS, "controls.svg")
        self.controls = get_ToggleToolButton(archivo, flip=False,
            pixels=24, tooltip_text="Controles Siempre Visibles")
        self.controls.connect("toggled", self.__emit_accion, "showcontrols")
        self.insert(self.controls, -1)

        archivo = os.path.join(ICONS, "fullscreen.png")
        self.full = get_ToggleToolButton(archivo, flip=False,
            pixels=24, tooltip_text="Pantalla Completa")
        self.full.connect("toggled", self.__fullscreen)
        self.insert(self.full, -1)
        self.full.set_active(False)

        self.insert(get_SeparatorToolItem(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

        self.set_sensitive(False)
        self.set_paused()
        self.lista.set_active(True)
        self.controls.set_active(True)

    def __fullscreen(self, widget):
        if widget.get_active():
            self.get_toplevel().fullscreen()
        else:
            self.get_toplevel().unfullscreen()

    def __emit_accion(self, widget, accion):
        if widget == self.controls:
            self.lista.set_active(self.controls.get_active())
        elif widget == self.lista:
            if self.lista.get_active():
                self.controls.set_active(self.lista.get_active())
        self.emit("accion-controls", accion)

    def set_video(self, widget, valor):
        self.izquierda.set_sensitive(valor)
        self.derecha.set_sensitive(valor)

    def set_paused(self):
        self.play.set_paused(self.pix_play)

    def set_playing(self):
        self.play.set_playing(self.pix_paused)


class JAMediaToolButton(gtk.ToolButton):

    def __init__(self, archivo, pixels=24, tooltip_text=""):

        gtk.ToolButton.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.estado = False
        self.imagen = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(archivo), pixels, pixels)
        self.imagen.set_from_pixbuf(pixbuf)
        self.set_icon_widget(self.imagen)
        self.imagen.show()
        self.set_tooltip_text(tooltip_text)
        self.imagen.set_size_request(pixels, pixels)
        self.show_all()

    def set_playing(self, pixbuf):
        if self.estado:
            return
        self.estado = True
        self.imagen.set_from_pixbuf(pixbuf)
        self.set_tooltip_text("Pausar")

    def set_paused(self, pixbuf):
        if not self.estado:
            return
        self.estado = False
        self.imagen.set_from_pixbuf(pixbuf)
        self.set_tooltip_text("Reproducir")


class ControlVolumen(gtk.VolumeButton):

    __gsignals__ = {
    "volumen": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.VolumeButton.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        archivo = os.path.join(ICONS, "Media-Controls-Volume-Up-icon.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(archivo), 24, 24)
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        self.get_child().destroy()
        self.add(image)

        self.connect("value-changed", self.__value_changed)
        self.show_all()

        self.set_value(0.1)

    def __value_changed(self, widget, valor):
        valor = int(valor * 10)
        self.emit('volumen', valor)
