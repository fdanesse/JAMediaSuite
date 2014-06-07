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

        #self.scrolltareas.crear_tarea(path)
        print "Crear Tarea para:", path

    def __re_emit_accion_list(self, widget, lista, accion, _iter):

        self.emit("accion-list", lista, accion, _iter)

    def reset(self):
        print "detener todo en jamediaconvert"
        print "Eliminar todas las tareas en jamediaconvert"
        print "Limpiar la lista de jamediaconvert"


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

    def crear_tarea(self, path):

        self.vbox.pack_start(WidgetArchivo(path), False, False, 2)


class WidgetArchivo(gtk.Frame):

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

            self.iz_box.pack_start(
                VideoFrame("  Convertir Video a Formato:  ",
                self.path_origen), False, False, 0)

            self.iz_box.pack_start(
                AudioFrame("  Extraer el Audio en Formato:  ",
                self.path_origen), False, False, 0)

        elif "audio" in datos:
            self.iz_box.pack_start(
                AudioFrame("  Convertir a Formato:  ",
                    self.path_origen), False, False, 0)

        else:
            print "Tipo de Archivo Desconocido:", self.path_origen, datos

        self.add(self.panel)
        self.show_all()


class VideoFrame(gtk.Frame):
    """
    Conversiones posibles para archivos de video.
    """

    def __init__(self, title, path):

        gtk.Frame.__init__(self)

        self.set_label(title)
        self.set_border_width(5)
        self.modify_bg(0, get_colors("toolbars"))

        self.path_origen = path

        vbox = gtk.VBox()

        vbox.pack_start(CheckButton("ogv"), False, False, 0)
        vbox.pack_start(CheckButton("mpeg"), False, False, 0)
        vbox.pack_start(CheckButton("avi"), False, False, 0)

        event = gtk.EventBox()
        event.set_border_width(5)
        event.modify_bg(0, get_colors("windows"))
        event.add(vbox)

        self.add(event)
        self.show_all()


class AudioFrame(gtk.Frame):
    """
    Conversiones posibles para archivos de audio.
    """

    def __init__(self, title, path):

        gtk.Frame.__init__(self)

        self.set_label(title)
        self.set_border_width(5)
        self.modify_bg(0, get_colors("toolbars"))

        self.path_origen = path

        vbox = gtk.VBox()

        vbox.pack_start(CheckButton("ogg"), False, False, 0)
        vbox.pack_start(CheckButton("mp3"), False, False, 0)
        vbox.pack_start(CheckButton("wav"), False, False, 0)

        event = gtk.EventBox()
        event.set_border_width(5)
        event.modify_bg(0, get_colors("windows"))
        event.add(vbox)

        self.add(event)
        self.show_all()


class CheckButton(gtk.CheckButton):

    #__gsignals__ = {
    #'set_data': (gobject.SIGNAL_RUN_LAST,
    #    gobject.TYPE_NONE, (gobject.TYPE_STRING,
    #    gobject.TYPE_BOOLEAN))}

    def __init__(self, formato):

        gtk.CheckButton.__init__(self)

        self.set_label(formato)
        self.show_all()

    #def do_toggled(self):

    #    self.emit('set_data', self.get_label(),
    #        self.get_active())


class ButtonsBox(gtk.Frame):

    #__gsignals__ = {
    #'set_data': (gobject.SIGNAL_RUN_LAST,
    #    gobject.TYPE_NONE, (gobject.TYPE_STRING,
    #    gobject.TYPE_BOOLEAN))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.set_label("  Acciones:  ")
        self.set_border_width(5)
        self.modify_bg(0, get_colors("toolbars"))

        vbox = gtk.VBox()

        iniciar = gtk.Button("Iniciar Tareas")
        iniciar.connect("clicked", self.__emit_accion)
        vbox.pack_start(iniciar, False, False, 2)

        copiar = gtk.Button("Copiar Tarea a Toda la Lista")
        copiar.connect("clicked", self.__emit_accion)
        vbox.pack_start(copiar, False, False, 2)

        eliminar = gtk.Button("Eliminar Tarea")
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

        print widget.get_label()
