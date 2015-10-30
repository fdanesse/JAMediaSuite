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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GLib

from Globales import get_separador
from Globales import get_pixels
from Globales import get_boton
from Globales import get_color
from Globales import get_colors

BASE_PATH = os.path.dirname(__file__)


class Toolbar(Gtk.Toolbar):
    """
    Toolbar principal.
    """

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(BASE_PATH,
            "Iconos", "JAMediaVideo.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            icono, -1, 35)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Salir.")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.show_all()

    def __salir(self, widget):
        """
        Cuando se hace click en el boton salir
        de la toolbar principal.
        """

        self.emit('salir')


class Visor(Gtk.DrawingArea):
    """
    Visor generico para utilizar como area de
    reproduccion de videos o dibujar.
    """

    __gsignals__ = {
    "ocultar_controles": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}

    def __init__(self):

        Gtk.DrawingArea.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

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

        #self.connect("touch-event", self.__touch)

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


class JAMediaButton(Gtk.EventBox):
    """
    Un Boton a medida.
    """

    __gsignals__ = {
    "clicked": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
    "click_derecho": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

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
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.ENTER_NOTIFY_MASK |
            Gdk.EventMask.LEAVE_NOTIFY_MASK)

        self.connect("button_press_event", self.button_press)
        self.connect("button_release_event", self.__button_release)
        self.connect("enter-notify-event", self.__enter_notify_event)
        self.connect("leave-notify-event", self.__leave_notify_event)

        self.imagen = Gtk.Image()
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

        label = Gtk.Label(texto)
        label.show()
        self.add(label)

    def set_imagen(self, archivo):

        self.imagen.set_from_file(archivo)

    def set_tamanio(self, w, h):

        self.set_size_request(w, h)


class ToolbarSalir(Gtk.Toolbar):
    """
    Toolbar para confirmar salir de la aplicación.
    """

    __gsignals__ = {
    "salir": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def run(self, nombre_aplicacion):
        """
        La toolbar se muestra y espera confirmación
        del usuario.
        """

        self.label.set_text("¿Salir de %s?" % (nombre_aplicacion))
        self.show()

    def __emit_salir(self, widget):
        """
        Confirma Salir de la aplicación.
        """

        self.cancelar()
        self.emit('salir')

    def cancelar(self, widget=None):
        """
        Cancela salir de la aplicación.
        """

        self.label.set_text("")
        self.hide()


class ToolbarPrincipal(Gtk.Toolbar):
    """
    Toolbar principal.
    """

    __gsignals__ = {
    'menu': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "camara.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Filmar")
        boton.connect("clicked", self.__emit_senial, "Filmar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "foto.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Fotografiar")
        boton.connect("clicked", self.__emit_senial, "Fotografiar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "microfono.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Grabar")
        boton.connect("clicked", self.__emit_senial, "Grabar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Reproducir")
        boton.connect("clicked", self.__emit_senial, "Reproducir")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "monitor.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Ver")
        boton.connect("clicked", self.__emit_senial, "Ver")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def __emit_senial(self, widget, text):
        """
        Cuando se hace click en algún boton.
        """

        self.emit('menu', text)


class ToolbarVideo(Gtk.Toolbar):
    """
    Toolbar de filmación.
    """

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'accion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'rotar': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.color = get_color("BLANCO")

        self.actualizador = False

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        item.set_expand(False)
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "camara.svg")
        self.filmar = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        self.filmar.set_tooltip_text("Filmar")
        self.filmar.connect("clicked", self.__emit_senial, "filmar")
        self.insert(self.filmar, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "configurar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_rotar, 'Izquierda')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_rotar, 'Derecha')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Reset")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Salir.")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.show_all()

    def set_estado(self, estado):
        """
        Cuando está grabando cambiará los colores
        intermitentemente en el botón correspondiente.
        """

        self.estado = estado

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if estado == "grabando":
            self.actualizador = GLib.timeout_add(400, self.__handle)
            self.label.set_text("Grabando . . .")

        elif estado == "detenido":
            self.label.set_text("")
            self.color = get_color("BLANCO")

    def __handle(self):
        """
        Cambia el color para advertir al usuario
        de que está grabando desde la webcam.
        """

        # FIXME: El color de fondo de la toolbar
        # no se puede cambiar, por eso agregué el label.
        if self.color == get_color("BLANCO"):
            self.color = get_color("NARANJA")

        elif self.color == get_color("NARANJA"):
            self.color = get_color("BLANCO")

        self.label.modify_fg(0, self.color)

        return True

    def __emit_rotar(self, widget, valor):
        """
        Emite la señal rotar con su valor Izquierda o Derecha.
        """

        self.emit('rotar', valor)

    def __emit_senial(self, widget, senial):
        """
        Emite filmar o configurar.
        """

        self.emit('accion', senial)

    def __salir(self, widget):
        """
        Para Salir al menú principal.
        """

        self.emit('salir')


class ToolbarFotografia(Gtk.Toolbar):
    """
    Toolbar Fotografias.
    """

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'accion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'rotar': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.color = get_color("BLANCO")

        self.actualizador = False

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        item.set_expand(False)
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "foto.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Fotografiar")
        boton.connect("clicked", self.__emit_senial, "fotografiar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "configurar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_rotar, 'Izquierda')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_rotar, 'Derecha')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Reset")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.show_all()

    def set_estado(self, estado):
        """
        Cuando está grabando cambiará los colores
        intermitentemente en el botón correspondiente.
        """

        self.estado = estado

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if estado == "grabando":
            self.actualizador = GLib.timeout_add(400, self.__handle)
            self.label.set_text("Fotografiando . . .")

        elif estado == "detenido":
            self.color = get_color("BLANCO")
            self.label.set_text("")

    def __handle(self):
        """
        Cambia el color para advertir al usuario
        de que está grabando desde la webcam.
        """

        # FIXME: El color de fondo de la toolbar
        # no se puede cambiar, por eso agregué el label.
        if self.color == get_color("BLANCO"):
            self.color = get_color("NARANJA")

        elif self.color == get_color("NARANJA"):
            self.color = get_color("BLANCO")

        self.label.modify_fg(0, self.color)

        return True

    def __emit_rotar(self, widget, valor):
        """
        Emite la señal rotar con su valor Izquierda o Derecha.
        """

        self.emit('rotar', valor)

    def __emit_senial(self, widget, senial):
        """
        Emite grabar o configurar.
        """

        self.emit('accion', senial)

    def __salir(self, widget):
        """
        Para Salir al menú principal.
        """

        self.emit('salir')


class ToolbarGrabarAudio(Gtk.Toolbar):
    """
    Toolbar Fotografias.
    """

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'accion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'rotar': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.color = get_color("BLANCO")

        self.actualizador = False

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        item.set_expand(False)
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "microfono.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Grabar")
        boton.connect("clicked", self.__emit_senial, "grabar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "configurar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_rotar, 'Izquierda')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_rotar, 'Derecha')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Reset")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.show_all()

    def set_estado(self, estado):
        """
        Cuando está grabando cambiará los colores
        intermitentemente en el botón correspondiente.
        """

        self.estado = estado

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if estado == "grabando":
            self.actualizador = GLib.timeout_add(400, self.__handle)
            self.label.set_text("Grabando . . .")

        elif estado == "detenido":
            self.label.set_text("")
            self.color = get_color("BLANCO")

    def __handle(self):
        """
        Cambia el color para advertir al usuario
        de que está grabando desde la webcam.
        """

        # FIXME: El color de fondo de la toolbar
        # no se puede cambiar, por eso agregué el label.
        if self.color == get_color("BLANCO"):
            self.color = get_color("NARANJA")

        elif self.color == get_color("NARANJA"):
            self.color = get_color("BLANCO")

        self.label.modify_fg(0, self.color)

        return True

    def __emit_rotar(self, widget, valor):
        """
        Emite la señal rotar con su valor Izquierda o Derecha.
        """

        self.emit('rotar', valor)

    def __emit_senial(self, widget, senial):
        """
        Emite grabar o configurar.
        """

        self.emit('accion', senial)

    def __salir(self, widget):
        """
        Para Salir al menú principal.
        """

        self.emit('salir')


class ToolbarRafagas(Gtk.Toolbar):
    """
    Pequeña toolbar con controles para
    configurar rafagas fotográficas.
    """

    __gsignals__ = {
    "run_rafaga": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        # > toolbar interna
        toolbar = Gtk.Toolbar()

        archivo = os.path.join(BASE_PATH,
            "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Disminuir")
        boton.connect("clicked", self.__restar)
        toolbar.insert(boton, -1)

        item = Gtk.ToolItem()
        self.time_label = Gtk.Label("1.0")
        self.time_label.show()
        item.add(self.time_label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "acercar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Aumentar")
        boton.connect("clicked", self.__sumar)
        toolbar.insert(boton, -1)

        item = Gtk.ToolItem()
        label = Gtk.Label("Seg.")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Comenzar")
        boton.connect("clicked", self.__run)
        toolbar.insert(boton, -1)

        toolbar.show_all()
        # < toolbar interna

        item = Gtk.ToolItem()
        item.set_expand(True)

        frame = Gtk.Frame()
        frame.set_label("Ráfaga:")
        frame.set_label_align(0.5, 0.5)
        frame.show()

        frame.add(toolbar)

        item.add(frame)
        self.insert(item, -1)

        self.show_all()

    def __run(self, widget):
        """
        Cuando el usuario da play en fotografiar en ráfagas.
        """

        self.emit('run_rafaga', float(self.time_label.get_text()))

    def __restar(self, widget):
        """
        Aumenta la frecuencia fotográfica en las ráfagas.
        """

        tiempo = float(self.time_label.get_text())

        if tiempo > 1.0:
            tiempo -= 0.1

        self.time_label.set_text(str(tiempo))

    def __sumar(self, widget):
        """
        Disminuye la frecuencia fotográfica en las ráfagas.
        """

        tiempo = float(self.time_label.get_text())
        tiempo += 0.1
        self.time_label.set_text(str(tiempo))


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
