#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetConvert.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay
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

from PlayerList import PlayerList
from ProgressBar import ProgressBar

from Globales import get_colors
from Globales import describe_archivo

gobject.threads_init()
gtk.gdk.threads_init()


class WidgetConvert(gtk.HPaned):

    __gsignals__ = {
    #'copy_tarea': (gobject.SIGNAL_RUN_LAST,
    #    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}
    "accion-list": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.set_border_width(2)
        self.modify_bg(0, get_colors("window"))

        self.playerlist = PlayerList()
        self.playerlist.set_mime_types(["audio/*", "video/*"])
        self.scrolltareas = ScrollTareas()

        self.pack1(self.playerlist, resize=False, shrink=True)
        self.pack2(self.scrolltareas, resize=True, shrink=True)

        self.show_all()

        self.playerlist.connect(
            "accion", self.__re_emit_accion_list)
        self.playerlist.connect(
            "nueva-seleccion", self.__selecction_file)
        #self.widgettareas.connect(
        #    'copy_tarea', self.__copy_tarea)

        #self.base_frame.connect("copy_tarea",
        #    self.__emit_copy_tarea)

    def __selecction_file(self, widget, path):

        if not path:
            return

        if not os.path.exists(path):
            return

        self.scrolltareas.crear_tarea(path)

    def __re_emit_accion_list(self, widget, lista, accion, _iter):

        self.emit("accion-list", lista, accion, _iter)

    def reset(self):
        self.scrolltareas.limpiar()
        self.playerlist.limpiar()


class ScrollTareas(gtk.ScrolledWindow):
    """
    Area derecha de WidgetConvert:
        Contenedor de Tareas por archivo.
    """

    def __init__(self):

        gtk.ScrolledWindow.__init__(self)

        self.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)

        self.vbox = gtk.VBox()
        self.add_with_viewport(self.vbox)
        self.get_child().modify_bg(0, get_colors("windows"))

        self.show_all()

    def __accion_tarea(self, widget, accion):

        print self.__accion_tarea, widget, accion

    def __clear(self, widget):

        self.limpiar()

    def crear_tarea(self, path):

        paths = []
        for child in self.vbox.get_children():
            paths.append(child.path_origen)

        if not path in paths:
            widgetarchivo = WidgetArchivo(path)
            self.vbox.pack_start(widgetarchivo, False, False, 2)
            widgetarchivo.connect('clear-tareas', self.__clear)
            widgetarchivo.connect('accion-tarea', self.__accion_tarea)

    def limpiar(self):

        for child in self.vbox.get_children():
            child.stop()
            self.vbox.remove(child)
            child.destroy()


class WidgetArchivo(gtk.Frame):

    __gsignals__ = {
    'clear-tareas': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ()),
    'accion-tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, path):

        gtk.Frame.__init__(self)

        self.path_origen = path

        self.set_label("  %s  " % os.path.basename(self.path_origen))
        self.set_border_width(5)
        self.modify_bg(0, get_colors("drawingplayer"))

        self.panel = gtk.HPaned()
        self.panel.modify_bg(0, get_colors("windows"))

        self.iz_box = gtk.VBox()
        self.buttonsbox = ButtonsBox()

        self.panel.pack1(self.iz_box,
            resize=False, shrink=True)
        self.panel.pack2(self.buttonsbox,
            resize=True, shrink=False)

        datos = describe_archivo(self.path_origen)

        if 'video' in datos or 'application/ogg' in datos or \
            'application/octet-stream' in datos:

            videoframe = VideoFrame(
                "  Convertir Video a Formato:  ", self.path_origen)
            self.iz_box.pack_start(videoframe, False, False, 0)
            videoframe.connect("tarea", self.__sensitive_buttons)

            audioframe = AudioFrame(
                "  Extraer Audio en Formato:  ", self.path_origen)
            self.iz_box.pack_start(audioframe, False, False, 0)
            audioframe.connect("tarea", self.__sensitive_buttons)

        elif "audio" in datos:
            audioframe = AudioFrame(
                "  Convertir Audio a Formato:  ", self.path_origen)
            self.iz_box.pack_start(audioframe, False, False, 0)
            audioframe.connect("tarea", self.__sensitive_buttons)

        else:
            print "Tipo de Archivo Desconocido:", self.path_origen, datos

        self.add(self.panel)
        self.show_all()

        self.buttonsbox.connect("accion", self.__set_accion)

    def __sensitive_buttons(self, widget):
        """
        Botones de acciones iniciar y copiar tarea,
        se activan solo si hay una tarea configurada.
        """

        for frame in self.iz_box.get_children():
            event = frame.get_child()
            vbox = event.get_child()

            for check in vbox.get_children():
                if check.get_active():
                    self.buttonsbox.activar(True)
                    return

        self.buttonsbox.activar(False)

    def __set_accion(self, widget, accion):
        """
        Cuando se hace click sobre un botón de acciones.
        """

        if accion == "Iniciar Tareas":
            self.emit("accion-tarea", accion)

        elif accion == "Copiar Tarea a Toda la Lista":
            self.emit("accion-tarea", accion)

        elif accion == "Eliminar Tarea":
            self.stop()
            vbox = self.get_parent()
            vbox.remove(self)
            self.destroy()

        elif accion == "Eliminar Todas las Tareas":
            self.emit("clear-tareas")

        else:
            print "Tarea sin Definir:", self.__set_accion, accion

    def stop(self):
        print "Detener Todas las Tareas", self.stop


class VideoFrame(gtk.Frame):
    """
    Conversiones posibles para archivos de video.
    """

    __gsignals__ = {
    'tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ())}

    def __init__(self, title, path):

        gtk.Frame.__init__(self)

        self.set_label(title)
        self.set_border_width(5)
        self.modify_bg(0, get_colors("toolbars"))

        self.path_origen = path

        vbox = gtk.VBox()

        for formato in ["ogv", "mpeg", "avi"]:
            check = CheckButton(formato)
            vbox.pack_start(check, False, False, 0)
            check.connect("tarea", self.__emit_tarea)

        event = gtk.EventBox()
        event.set_border_width(5)
        event.modify_bg(0, get_colors("windows"))
        event.add(vbox)

        self.add(event)
        self.show_all()

    def __emit_tarea(self, widget):

        self.emit("tarea")


class AudioFrame(gtk.Frame):
    """
    Conversiones posibles para archivos de audio.
    """

    __gsignals__ = {
    'tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ())}

    def __init__(self, title, path):

        gtk.Frame.__init__(self)

        self.set_label(title)
        self.set_border_width(5)
        self.modify_bg(0, get_colors("toolbars"))

        self.path_origen = path

        vbox = gtk.VBox()

        for formato in ["ogg", "mp3", "wav"]:
            check = CheckButton(formato)
            vbox.pack_start(check, False, False, 0)
            check.connect("tarea", self.__emit_tarea)

        event = gtk.EventBox()
        event.set_border_width(5)
        event.modify_bg(0, get_colors("windows"))
        event.add(vbox)

        self.add(event)
        self.show_all()

    def __emit_tarea(self, widget):

        self.emit("tarea")


class CheckButton(gtk.CheckButton):

    __gsignals__ = {
    'tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, ())}

    def __init__(self, formato):

        gtk.CheckButton.__init__(self)

        self.set_label(formato)
        self.show_all()

    def do_toggled(self):

        self.emit('tarea')


class ButtonsBox(gtk.Frame):

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.set_label("  Acciones:  ")
        self.set_border_width(5)
        self.modify_bg(0, get_colors("toolbars"))

        vbox = gtk.VBox()

        iniciar = gtk.Button("Iniciar Tareas")
        iniciar.connect("clicked", self.__emit_accion)
        vbox.pack_start(iniciar, False, False, 2)
        iniciar.set_sensitive(False)

        copiar = gtk.Button("Copiar Tarea a Toda la Lista")
        copiar.connect("clicked", self.__emit_accion)
        vbox.pack_start(copiar, False, False, 2)
        copiar.set_sensitive(False)

        eliminar = gtk.Button("Eliminar Tarea")
        eliminar.connect("clicked", self.__emit_accion)
        vbox.pack_start(eliminar, False, False, 2)

        eliminar = gtk.Button("Eliminar Todas las Tareas")
        eliminar.connect("clicked", self.__emit_accion)
        vbox.pack_start(eliminar, False, False, 2)

        frame = gtk.Frame()
        frame.set_label("  Progreso  ")
        frame.set_border_width(5)
        frame.modify_bg(0, get_colors("toolbars"))

        self.progress = ProgressBar()
        frame.add(self.progress)
        vbox.pack_end(frame, False, False, 2)

        event = gtk.EventBox()
        event.set_border_width(5)
        event.modify_bg(0, get_colors("windows"))
        event.add(vbox)

        self.add(event)
        self.show_all()

    def __emit_accion(self, widget):

        self.emit("accion", widget.get_label())

    def activar(self, valor):

        event = self.get_child()
        vbox = event.get_child()

        for button in vbox.get_children()[0:2]:
            button.set_sensitive(valor)
