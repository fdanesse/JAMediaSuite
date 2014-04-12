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


class Toolbar(gtk.EventBox):
    """
    Toolbar principal.
    """

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        toolbar = gtk.Toolbar()

        self.modify_bg(0, get_colors("toolbars"))
        toolbar.modify_bg(0, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(BASE_PATH,
            "Iconos", "JAMediaVideo.svg")
        pixbuf = gdk.pixbuf_new_from_file_at_size(
            icono, -1, 35)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.toolbars_container = gtk.HBox()
        item = gtk.ToolItem()
        item.set_expand(True)
        item.add(self.toolbars_container)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.toolbars_container.pack_start(
            ToolbarPrincipal(), True, True, 0)

        self.add(toolbar)
        self.show_all()

    def __salir(self, widget):
        """
        Cuando se hace click en el boton salir
        de la toolbar principal.
        """

        self.emit('salir')


class ToolbarSalir(gtk.EventBox):
    """
    Toolbar para confirmar salir de la aplicación.
    """

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        toolbar = gtk.Toolbar()

        self.modify_bg(0, get_colors("window"))
        toolbar.modify_bg(0, get_colors("window"))

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("")
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_salir)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.add(toolbar)
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


class ToolbarPrincipal(gtk.EventBox):
    """
    Toolbar principal.
    """

    __gsignals__ = {
    'menu': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(0, get_colors("toolbars"))
        toolbar.modify_bg(0, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "camara.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Filmar")
        boton.connect("clicked", self.__emit_senial, "Filmar")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "foto.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Fotografiar")
        boton.connect("clicked", self.__emit_senial, "Fotografiar")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "microfono.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Grabar")
        boton.connect("clicked", self.__emit_senial, "Grabar")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Reproducir")
        boton.connect("clicked", self.__emit_senial, "Reproducir")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "monitor.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Ver")
        boton.connect("clicked", self.__emit_senial, "Ver")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def __emit_senial(self, widget, text):
        """
        Cuando se hace click en algún boton.
        """

        self.emit('menu', text)

'''
class ToolbarVideo(gtk.Toolbar):
    """
    Toolbar de filmación.
    """

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'accion': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'rotar': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.color = get_color("BLANCO")

        self.actualizador = False

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = gtk.ToolItem()
        item.set_expand(False)
        self.label = gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "camara.svg")
        self.filmar = get_boton(archivo, flip=False,
            pixels=24)
        self.filmar.set_tooltip_text("Filmar")
        self.filmar.connect("clicked", self.__emit_senial, "filmar")
        self.insert(self.filmar, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "configurar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_rotar, 'Izquierda')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True,
            pixels=24)
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_rotar, 'Derecha')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Reset")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
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
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if estado == "grabando":
            self.actualizador = gobject.timeout_add(400, self.__handle)
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


class ToolbarFotografia(gtk.Toolbar):
    """
    Toolbar Fotografias.
    """

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'accion': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'rotar': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.color = get_color("BLANCO")

        self.actualizador = False

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = gtk.ToolItem()
        item.set_expand(False)
        self.label = gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "foto.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Fotografiar")
        boton.connect("clicked", self.__emit_senial, "fotografiar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "configurar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_rotar, 'Izquierda')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True,
            pixels=24)
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_rotar, 'Derecha')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Reset")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
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
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if estado == "grabando":
            self.actualizador = gobject.timeout_add(400, self.__handle)
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


class ToolbarGrabarAudio(gtk.Toolbar):
    """
    Toolbar Fotografias.
    """

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'accion': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'rotar': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.color = get_color("BLANCO")

        self.actualizador = False

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = gtk.ToolItem()
        item.set_expand(False)
        self.label = gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "microfono.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Grabar")
        boton.connect("clicked", self.__emit_senial, "grabar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "configurar")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_rotar, 'Izquierda')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True,
            pixels=24)
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_rotar, 'Derecha')
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Reset")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
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
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if estado == "grabando":
            self.actualizador = gobject.timeout_add(400, self.__handle)
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


class ToolbarRafagas(gtk.Toolbar):
    """
    Pequeña toolbar con controles para
    configurar rafagas fotográficas.
    """

    __gsignals__ = {
    "run_rafaga": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        # > toolbar interna
        toolbar = gtk.Toolbar()

        archivo = os.path.join(BASE_PATH,
            "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Disminuir")
        boton.connect("clicked", self.__restar)
        toolbar.insert(boton, -1)

        item = gtk.ToolItem()
        self.time_label = gtk.Label("1.0")
        self.time_label.show()
        item.add(self.time_label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "acercar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Aumentar")
        boton.connect("clicked", self.__sumar)
        toolbar.insert(boton, -1)

        item = gtk.ToolItem()
        label = gtk.Label("Seg.")
        label.show()
        item.add(label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Comenzar")
        boton.connect("clicked", self.__run)
        toolbar.insert(boton, -1)

        toolbar.show_all()
        # < toolbar interna

        item = gtk.ToolItem()
        item.set_expand(True)

        frame = gtk.Frame()
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
'''
