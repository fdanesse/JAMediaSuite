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
        self.scrolltareas.connect(
            'accion-tarea', self.__accion_tareas)

    def __accion_tareas(self, widget, widgetarchivo, accion):
        """
        Cuando el usuario ejecuta una acción en la botonera derecha.
        """

        if accion == "Ejecutar Tarea en Archivo":
            print "insensibilizar controles que afecten proceso"
            print "iniciar tareas configuradas"

        elif accion == "Ejecutar Tareas en la Lista":
            print "insensibilizar controles que afecten proceso"
            print "iniciar tareas configuradas"

        elif accion == "Copiar Tarea a Toda la Lista":
            self.get_toplevel().set_sensitive(False)

            for filepath in self.playerlist.get_items_paths():
                # Crear el widget de tareas para cada archivo en la lista.
                self.__selecction_file(False, filepath)

            self.scrolltareas.copy_tarea(widgetarchivo.get_tareas())

            self.get_toplevel().set_sensitive(True)

        else:
            print "Tarea sin definir:", self.__accion_tarea, accion

    def __selecction_file(self, widget, path):
        """
        Cuando el usuario selecciona un archivo en la lista.
        """

        if not path:
            return

        if not os.path.exists(path):
            return

        self.scrolltareas.crear_tarea(path)

    def __re_emit_accion_list(self, widget, lista, accion, _iter):
        """
        Cuando el usuario selecciona opciones en el menu emergente de
        la lista de archivos.
        """

        self.emit("accion-list", lista, accion, _iter)

    def reset(self):
        """
        Limpia la lista de archivos y el widget de tareas.
        """

        self.scrolltareas.limpiar()
        self.playerlist.limpiar()


class ScrollTareas(gtk.ScrolledWindow):
    """
    Area derecha de WidgetConvert:
        Contenedor de Tareas por archivo.
    """

    __gsignals__ = {
    'accion-tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING))}

    def __init__(self):

        gtk.ScrolledWindow.__init__(self)

        self.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)

        self.vbox = gtk.VBox()
        self.add_with_viewport(self.vbox)
        self.get_child().modify_bg(0, get_colors("windows"))

        self.show_all()

    def __accion_tarea(self, widgetarchivo, accion):
        """
        Cuando se hace click sobre un botón de acciones.
        """

        self.emit('accion-tarea', widgetarchivo, accion)

    def __clear(self, widget):
        """
        Elimina todas las tareas.
        """

        self.limpiar()

    def copy_tarea(self, tareas):
        """
        Copia una lista de tareas asignada a un archivo,
        a todos los archivos abiertos en el widget de tareas.
        """

        for widgetarchivo in self.vbox.get_children():
            widgetarchivo.copy_tarea(tareas)

    def crear_tarea(self, path):
        """
        Crear el widget de tareas para un determinado archivo.
        """

        paths = []
        for child in self.vbox.get_children():
            paths.append(child.path_origen)

        if not path in paths:
            widgetarchivo = WidgetArchivo(path)
            self.vbox.pack_start(widgetarchivo, False, False, 2)
            widgetarchivo.connect('clear-tareas', self.__clear)
            widgetarchivo.connect('accion-tarea', self.__accion_tarea)

    def limpiar(self):
        """
        Elimina todas las tareas.
        """

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

            imageframe = ImageFrame(
                "  Extraer Imágenes en Formato:  ", self.path_origen)
            self.iz_box.pack_start(imageframe, False, False, 0)
            imageframe.connect("tarea", self.__sensitive_buttons)

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

        if accion == "Ejecutar Tarea en Archivo":
            self.emit("accion-tarea", accion)

        elif accion == "Ejecutar Tareas en la Lista":
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

    def get_tareas(self):
        """
        Devuelve las tareas configuradas para un determinado archivo.
        """

        tareas = []

        for frame in self.iz_box.get_children():
            event = frame.get_child()
            vbox = event.get_child()

            for check in vbox.get_children():
                if check.get_active():
                    tareas.append(check.get_label())

        return tareas

    def copy_tarea(self, tareas):
        """
        Setea una lista de tareas a realizar.
        """

        for frame in self.iz_box.get_children():
            event = frame.get_child()
            vbox = event.get_child()

            for check in vbox.get_children():
                if check.get_label() in tareas:
                    check.set_active(True)

                else:
                    check.set_active(False)

    def stop(self):
        print "Detener Todas las Tareas", self.stop


class ImageFrame(gtk.Frame):
    """
    Extracciones de Imágenes posibles para archivos de video.
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

        for formato in ["jpg", "png"]:
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

        iniciar = gtk.Button("Ejecutar Tarea en Archivo")
        iniciar.connect("clicked", self.__emit_accion)
        vbox.pack_start(iniciar, False, False, 2)
        iniciar.set_sensitive(False)

        iniciar = gtk.Button("Ejecutar Tareas en la Lista")
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

        for button in vbox.get_children()[0:3]:
            button.set_sensitive(valor)
