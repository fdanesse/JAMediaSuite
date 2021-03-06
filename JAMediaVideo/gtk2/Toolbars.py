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
import gobject

from Globales import get_separador
from Globales import get_boton
from Globales import get_colors

from Widgets import Help
from Widgets import Credits

BASE_PATH = os.path.dirname(__file__)


def ocultar(objeto):
    if objeto.get_visible():
        objeto.hide()


def activar(objeto):
    objeto.set_sensitive(True)


def desactivar(objeto):
    objeto.set_sensitive(False)


class Toolbar(gtk.EventBox):
    """
    Toolbar principal.
    """

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "config-show": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "accion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING)),
    "mode-change": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.toolbars = []

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "JAMediaVideo.svg")
        boton = get_boton(archivo, flip=False, pixels=35)
        boton.set_tooltip_text("Autor")
        boton.connect("clicked", self.__show_credits)
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "JAMedia-help.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Ayuda")
        boton.connect("clicked", self.__show_help)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        self.toolbars_container = gtk.HBox()
        item = gtk.ToolItem()
        item.set_expand(True)
        item.add(self.toolbars_container)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        self.toolbar_principal = ToolbarPrincipal()
        self.toolbars_container.pack_start(
            self.toolbar_principal, True, True, 0)
        self.toolbars.append(self.toolbar_principal)

        self.toolbar_video = ToolbarVideo()
        self.toolbars_container.pack_start(self.toolbar_video, True, True, 0)
        self.toolbars.append(self.toolbar_video)

        self.toolbar_fotografia = ToolbarFotografia()
        self.toolbars_container.pack_start(
            self.toolbar_fotografia, True, True, 0)
        self.toolbars.append(self.toolbar_fotografia)

        #self.toolbar_audio = ToolbarGrabarAudio()
        #self.toolbars_container.pack_start(
        #    self.toolbar_audio, True, True, 0)
        #self.toolbars.append(self.toolbar_audio)

        self.toolbar_jamedia = ToolbarJAMedia()
        self.toolbars_container.pack_start(self.toolbar_jamedia, True, True, 0)
        self.toolbars.append(self.toolbar_jamedia)

        self.toolbar_jamediaimagenes = ToolbarJAMediaImagenes()
        self.toolbars_container.pack_start(
            self.toolbar_jamediaimagenes, True, True, 0)
        self.toolbars.append(self.toolbar_jamediaimagenes)

        self.toolbar_converter = ToolbarConverter()
        self.toolbars_container.pack_start(
            self.toolbar_converter, True, True, 0)
        self.toolbars.append(self.toolbar_converter)

        self.add(toolbar)
        self.show_all()

        self.toolbar_principal.connect("menu", self.__get_menu)
        self.toolbar_video.connect("accion", self.__set_video_accion)
        self.toolbar_fotografia.connect("accion", self.__set_foto_accion)
        self.toolbar_jamedia.connect("accion", self.__set_jamedia_accion)
        #self.toolbar_audio.connect("accion", self.__set_audio_accion)
        self.toolbar_jamediaimagenes.connect("accion",
            self.__set_jamediaimagenes_accion)
        self.toolbar_converter.connect("accion", self.__set_converter_accion)

    def __set_converter_accion(self, toolbar, accion):
        self.emit("accion", "jamediaconverter", accion)

    def __set_jamediaimagenes_accion(self, toolbar, accion):
        if accion == "Salir":
            self.emit("accion", "jamediaimagenes", accion)

        elif accion == "Configurar":
            self.emit("config-show", "jamediaimagenes")

        else:
            self.emit("accion", "jamediaimagenes", accion)

    def __set_jamedia_accion(self, toolbar, accion):
        if accion == "Salir":
            self.emit("accion", "jamedia", accion)

        elif accion == "Configurar":
            self.emit("config-show", "jamedia")

        else:
            self.emit("accion", "jamedia", accion)

    def __set_foto_accion(self, toolbar, accion):
        if accion == "Salir":
            self.emit("accion", "foto", accion)
            self.toolbar_fotografia.set_estado(False)

        elif accion == "Configurar":
            self.emit("config-show", "foto")

        elif accion == "Stop":
            self.emit("accion", "foto", accion)
            self.toolbar_fotografia.set_estado("Stop")
            self.emit("config-show", "foto")

        elif accion == "Fotografiar":
            self.emit("accion", "foto", accion)
            self.toolbar_fotografia.set_estado("Playing")
            self.emit("config-show", "")

        elif accion == "Izquierda" or accion == "Derecha":
            self.emit("accion", "foto", accion)

    def __set_video_accion(self, toolbar, accion):
        if accion == "Salir":
            self.emit("accion", "video", accion)
            self.toolbar_video.set_estado(False)

        elif accion == "Configurar":
            self.emit("config-show", "camara")

        elif accion == "Stop":
            self.emit("accion", "video", accion)
            self.toolbar_video.set_estado("Stop")
            self.emit("config-show", "camara")

        elif accion == "Filmar":
            self.emit("accion", "video", accion)
            self.toolbar_video.set_estado("Playing")
            self.emit("config-show", "")

        elif accion == "Izquierda" or accion == "Derecha":
            self.emit("accion", "video", accion)

    def __show_credits(self, widget):
        dialog = Credits(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __show_help(self, widget):
        dialog = Help(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __get_menu(self, widget, menu):
        self.switch(menu)

    def __salir(self, widget):
        self.emit('salir')

    def switch(self, modo):
        """
        Muestra la toolbar correspondiente a:
            Filmar
            Grabar Audio
            Fotografiar
            Reproducir Audio y Video
            Ver Imágenes
            Convertir audio o video y/o extraer audio, video o imágenes
        """

        map(ocultar, self.toolbars)

        if modo == "Filmar":
            self.toolbar_video.show()
            self.toolbar_video.set_estado("Stop")
            self.emit("config-show", "camara")
            self.emit("mode-change", "video")

        elif modo == "menu":
            self.toolbar_principal.show()
            self.emit("config-show", "")
            self.emit("mode-change", "menu")

        elif modo == "Fotografiar":
            self.toolbar_fotografia.show()
            self.toolbar_fotografia.set_estado("Stop")
            self.emit("config-show", "foto")
            self.emit("mode-change", "foto")

        elif modo == "Reproducir":
            self.toolbar_jamedia.show()
            self.emit("config-show", "jamedia")
            self.emit("mode-change", "jamedia")

        elif modo == "Ver":
            self.toolbar_jamediaimagenes.show()
            self.emit("config-show", "jamediaimagenes")
            self.emit("mode-change", "jamediaimagenes")

        elif modo == "Convert":
            self.toolbar_converter.show()
            #self.emit("config-show", "converter")
            self.emit("mode-change", "converter")

        else:
            print "switch:", modo

    def permitir_filmar(self, valor):
        self.toolbar_video.permitir_filmar(valor)

    def activate_conversor(self, valor):
        self.toolbar_converter.activate_conversor(valor)


class ToolbarPrincipal(gtk.EventBox):
    """
    Toolbar principal.
    """

    __gsignals__ = {
    'menu': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "camara.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Filmar")
        boton.connect("clicked", self.__emit_senial, "Filmar")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "foto.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Fotografiar")
        boton.connect("clicked", self.__emit_senial, "Fotografiar")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "microfono.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Grabar Audio")
        boton.set_sensitive(False)
        boton.connect("clicked", self.__emit_senial, "Grabar")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "convert.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("JAMediaConverter")
        boton.connect("clicked", self.__emit_senial, "Convert")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Reproducir Audio y Video")
        boton.connect("clicked", self.__emit_senial, "Reproducir")
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "monitor.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Ver Imágenes")
        boton.connect("clicked", self.__emit_senial, "Ver")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def __emit_senial(self, widget, text):
        """
        Cuando se hace click en algún boton.
        """
        self.emit('menu', text)


class ToolbarVideo(gtk.EventBox):
    """
    Toolbar de filmación.
    """

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.widget_playing = []  # activos en playing
        self.widget_stop = []  # activos en stop

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        item = gtk.ToolItem()
        item.set_expand(False)
        self.label = gtk.Label("")
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "camara.svg")
        self.boton_filmar = get_boton(archivo, flip=False, pixels=24)
        self.boton_filmar.set_tooltip_text("Filmar")
        self.boton_filmar.connect("clicked", self.__emit_senial, "Filmar")
        toolbar.insert(self.boton_filmar, -1)
        self.widget_stop = [self.boton_filmar]

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "Configurar")
        toolbar.insert(boton, -1)
        self.widget_stop.append(boton)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_senial, 'Izquierda')
        toolbar.insert(boton, -1)
        self.widget_stop.append(boton)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True, pixels=24)
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_senial, 'Derecha')
        toolbar.insert(boton, -1)
        self.widget_stop.append(boton)

        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Stop")
        toolbar.insert(boton, -1)

        self.widget_playing = [boton]

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Volver al Menú")
        boton.connect("clicked", self.__emit_senial, "Salir")
        toolbar.insert(boton, -1)

        self.add(toolbar)
        self.show_all()

    def __emit_senial(self, widget, senial):
        """
        Emite filmar o configurar.
        """
        self.emit('accion', senial)

    def set_estado(self, estado):
        if not estado or estado == "Stop":
            map(activar, self.widget_stop)
            map(desactivar, self.widget_playing)

        elif estado == "Playing":
            map(activar, self.widget_playing)
            map(desactivar, self.widget_stop)

    def permitir_filmar(self, valor):
        self.boton_filmar.set_sensitive(valor)


class ToolbarFotografia(gtk.EventBox):
    """
    Toolbar Fotografias.
    """

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        self.widget_playing = []  # activos en playing
        self.widget_stop = []  # activos en stop

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.actualizador = False

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "foto.svg")
        self.boton_fotografiar = get_boton(archivo, flip=False, pixels=24)
        self.boton_fotografiar.set_tooltip_text("Fotografiar")
        self.boton_fotografiar.connect("clicked",
            self.__emit_senial, "Fotografiar")
        self.widget_stop = [self.boton_fotografiar]
        toolbar.insert(self.boton_fotografiar, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "Configurar")
        self.widget_stop.append(boton)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_senial, 'Izquierda')
        self.widget_stop.append(boton)
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True, pixels=24)
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_senial, 'Derecha')
        self.widget_stop.append(boton)
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_sensitive(False)
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Stop")
        self.widget_playing.append(boton)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Volver al Menú")
        boton.connect("clicked", self.__emit_senial, "Salir")
        toolbar.insert(boton, -1)

        self.add(toolbar)
        self.show_all()

    def __emit_senial(self, widget, senial):
        self.emit('accion', senial)

    def set_estado(self, estado):
        if not estado or estado == "Stop":
            map(activar, self.widget_stop)
            map(desactivar, self.widget_playing)

        elif estado == "Playing":
            map(activar, self.widget_playing)
            map(desactivar, self.widget_stop)


'''
class ToolbarGrabarAudio(gtk.EventBox):
    """
    Toolbar Fotografias.
    """

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'rotar': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        self.actualizador = False

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = gtk.ToolItem()
        item.set_expand(False)
        self.label = gtk.Label("")
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "microfono.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Grabar")
        boton.connect("clicked", self.__emit_senial, "grabar")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Configurar")
        boton.connect("clicked", self.__emit_senial, "configurar")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        #archivo = os.path.join(BASE_PATH,
        #    "Iconos", "rotar.svg")
        #boton = get_boton(archivo, flip=False,
        #    pixels=24)
        #boton.set_tooltip_text("Izquierda")
        #boton.connect("clicked", self.__emit_rotar, 'Izquierda')
        #toolbar.insert(boton, -1)

        #archivo = os.path.join(BASE_PATH,
        #    "Iconos", "rotar.svg")
        #boton = get_boton(archivo, flip=True,
        #    pixels=24)
        #boton.set_tooltip_text("Derecha")
        #boton.connect("clicked", self.__emit_rotar, 'Derecha')
        #toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(
            archivo, flip=False, pixels=24)
        boton.set_sensitive(False)
        boton.set_tooltip_text("Detener")
        boton.connect("clicked", self.__emit_senial, "Reset")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Volver al Menú")
        boton.connect("clicked", self.__salir)
        toolbar.insert(boton, -1)

        self.add(toolbar)
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
'''


class ToolbarJAMedia(gtk.EventBox):

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Listar Archivos")
        boton.connect("clicked", self.__emit_senial, "Configurar")
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_senial, 'Izquierda')
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True, pixels=24)
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_senial, 'Derecha')
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Volver al Menú")
        boton.connect("clicked", self.__emit_senial, "Salir")
        toolbar.insert(boton, -1)

        self.add(toolbar)
        self.show_all()

    def __emit_senial(self, widget, senial):
        self.emit('accion', senial)


class ToolbarJAMediaImagenes(gtk.EventBox):

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Listar Archivos")
        boton.connect("clicked", self.__emit_senial, "Configurar")
        toolbar.insert(boton, -1)

        #toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        #archivo = os.path.join(BASE_PATH, "Iconos", "zoom-fit-best.svg")
        #boton = get_boton(archivo, flip=False, pixels=24)
        #boton.set_tooltip_text("Centrar")
        #boton.connect("clicked", self.__emit_senial, 'Centrar')
        #toolbar.insert(boton, -1)

        #archivo = os.path.join(BASE_PATH, "Iconos", "zoom-in.svg")
        #boton = get_boton(archivo, flip=False, pixels=24)
        #boton.set_tooltip_text("Acercar")
        #boton.connect("clicked", self.__emit_senial, 'Acercar')
        #toolbar.insert(boton, -1)

        #archivo = os.path.join(BASE_PATH, "Iconos", "zoom-out.svg")
        #boton = get_boton(archivo, flip=False, pixels=24)
        #boton.set_tooltip_text("Alejar")
        #boton.connect("clicked", self.__emit_senial, 'Alejar')
        #toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Izquierda")
        boton.connect("clicked", self.__emit_senial, 'Izquierda')
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "rotar.svg")
        boton = get_boton(archivo, flip=True, pixels=24)
        boton.set_tooltip_text("Derecha")
        boton.connect("clicked", self.__emit_senial, 'Derecha')
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Volver al Menú")
        boton.connect("clicked", self.__emit_senial, "Salir")
        toolbar.insert(boton, -1)

        self.add(toolbar)
        self.show_all()

    def __emit_senial(self, widget, senial):
        self.emit('accion', senial)


class ToolbarConverter(gtk.EventBox):

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")
        self.boton_stop = get_boton(archivo, flip=False, pixels=24)
        self.boton_stop.set_sensitive(False)
        self.boton_stop.set_tooltip_text("Detener")
        self.boton_stop.connect("clicked", self.__emit_senial, "Stop")
        toolbar.insert(self.boton_stop, -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        self.info = gtk.Label("")
        self.info.set_alignment(0.0, 0.5)
        self.info.modify_fg(0, get_colors("drawingplayer"))
        self.info.show()
        item.add(self.info)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        self.boton_menu = get_boton(archivo, flip=False, pixels=24)
        self.boton_menu.set_tooltip_text("Volver al Menú")
        self.boton_menu.connect("clicked", self.__emit_senial, "Salir")
        toolbar.insert(self.boton_menu, -1)

        self.add(toolbar)
        self.show_all()

    def __emit_senial(self, widget, senial):
        self.boton_menu.set_sensitive(False)
        self.boton_stop.set_sensitive(False)
        self.emit('accion', senial)

    def set_info(self, info):
        self.info.set_text(info)

    def activate_conversor(self, valor):
        self.boton_menu.set_sensitive(not valor)
        self.boton_stop.set_sensitive(valor)
