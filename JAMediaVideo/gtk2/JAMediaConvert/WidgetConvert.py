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
from Converter.JAMediaConverter import JAMediaConverter

from Globales import get_colors
from Globales import describe_archivo
from Globales import get_audio_directory
from Globales import get_imagenes_directory
from Globales import get_video_directory

PR = False


class WidgetConvert(gtk.HPaned):

    __gsignals__ = {
    "accion-list": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    "in-run": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN, )),
    "pendientes": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.set_border_width(2)
        self.modify_bg(0, get_colors("window"))

        self.tareas_pendientes = []

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
        self.scrolltareas.connect("tareas", self.__info_num_tareas)

    def __info_num_tareas(self, widget, num):
        self.__emit_pendientes("Archivos a Procesar: %s" % num)

    def __accion_tareas(self, widget, widgetarchivo, accion):
        """
        Cuando el usuario ejecuta una acción en la botonera derecha.
        """

        if accion == "Ejecutar Tarea en Archivo":
            self.tareas_pendientes = [widgetarchivo]
            gobject.idle_add(self.__run_stack_tareas)

        elif accion == "Ejecutar Tareas en la Lista":
            self.tareas_pendientes = []

            for tarea in self.scrolltareas.vbox.get_children():
                tarea.hide()
                self.tareas_pendientes.append(tarea)

            gobject.idle_add(self.__run_stack_tareas)

        elif accion == "Copiar Tarea a Toda la Lista":
            self.get_toplevel().set_sensitive(False)

            for filepath in self.playerlist.get_items_paths():
                self.__selecction_file(False, filepath)

            self.scrolltareas.copy_tarea(widgetarchivo.get_tareas())
            self.__emit_pendientes("Archivos a Procesar: %s" % len(
                self.scrolltareas.vbox.get_children()))
            self.get_toplevel().set_sensitive(True)

        else:
            # Al recibir end, continúa
            gobject.idle_add(self.__run_stack_tareas)

    def __run_stack_tareas(self):

        if PR:
            print "WidgetConvert", "__run_stack_tareas"

        if not self.tareas_pendientes:
            self.emit("in-run", False)
            widgetarchivo = self.scrolltareas.vbox.get_children()[0]
            self.playerlist.select_valor(widgetarchivo.path_origen)
            self.playerlist.set_sensitive(True)

            for tarea in self.scrolltareas.vbox.get_children():
                tarea.show()

            gobject.timeout_add(6, self.__emit_pendientes,
                "No Hay Tareas Pendientes.")

        else:
            widgetarchivo = self.tareas_pendientes[0]
            self.tareas_pendientes.remove(widgetarchivo)

            self.emit("in-run", True)
            self.playerlist.select_valor(widgetarchivo.path_origen)
            self.playerlist.set_sensitive(False)
            gobject.timeout_add(6, self.__emit_pendientes,
                "Archivos Pendientes: %s" % str(len(
                self.tareas_pendientes) + 1))

            for tarea in self.scrolltareas.vbox.get_children():
                tarea.hide()

            widgetarchivo.show()
            widgetarchivo.play()

        return False

    def __emit_pendientes(self, info):
        self.emit("pendientes", info)
        return False

    def __selecction_file(self, widget, path):
        """
        Cuando el usuario selecciona un archivo en la lista.
        """

        if not path:
            return

        if not os.path.exists(path):
            return

        self.scrolltareas.crear_tarea(path)
        self.__emit_pendientes("Archivos a Procesar: %s" % len(
            self.scrolltareas.vbox.get_children()))

    def __re_emit_accion_list(self, widget, lista, accion, _iter):
        """
        Cuando el usuario selecciona opciones en el menu emergente de
        la lista de archivos.
        """

        if accion == "limpiar":
            self.reset()

        else:
            self.emit("accion-list", lista, accion, _iter)

    def reset(self):
        """
        Limpia la lista de archivos y el widget de tareas.
        """

        self.tareas_pendientes = []
        self.scrolltareas.limpiar()
        self.playerlist.limpiar()

    def quitar(self, path):
        """
        Quita el Widget de tareas de un archivo en particular.
        """

        for widgetarchivo in self.scrolltareas.vbox.get_children():
            if widgetarchivo.path_origen == path:
                self.scrolltareas.vbox.remove(widgetarchivo)
                widgetarchivo.destroy()
                break


class ScrollTareas(gtk.ScrolledWindow):
    """
    Area derecha de WidgetConvert:
        Contenedor de Tareas por archivo.
    """

    __gsignals__ = {
    'accion-tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING)),
    "tareas": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_INT, ))}

    def __init__(self):

        gtk.ScrolledWindow.__init__(self)

        self.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)

        self.vbox = gtk.VBox()
        self.add_with_viewport(self.vbox)
        self.get_child().modify_bg(0, get_colors("windows"))

        self.show_all()

        self.vbox.connect("remove", self.__change_number_tareas)
        # FIXME: Por algún motivo esto no funciona.
        #self.vbox.connect("add", self.__change_number_tareas)

    def __change_number_tareas(self, vbox, widget):
        self.emit("tareas", len(self.vbox.get_children()))

    def __accion_tarea(self, widgetarchivo, accion):
        """
        Cuando se hace click sobre un botón de acciones.
        """

        self.emit('accion-tarea', widgetarchivo, accion)

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
            widgetarchivo.connect('clear-tareas', self.limpiar)
            widgetarchivo.connect('accion-tarea', self.__accion_tarea)

    def limpiar(self, widget=False):
        """
        Elimina todas las tareas.
        """

        for child in self.vbox.get_children():
            child.salir()
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
        self.temp_tareas = []
        self.player = False

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

        if 'video' in datos or 'application/ogg' in datos:
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

        elif "audio" in datos or 'application/octet-stream' in datos:
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
            vbox = self.get_parent()
            vbox.remove(self)
            self.destroy()

        elif accion == "Eliminar Todas las Tareas":
            self.emit("clear-tareas")

        else:
            print "Tarea sin Definir:", self.__set_accion, accion

    def __play_stack_tareas(self, player=False):

        if PR:
            print "WidgetConvert", "__play_stack_tareas"

        if self.player:
            # FIXME: stop hace que la aplicación se cuelgue.
            #self.player.stop()
            #del(self.player)
            self.player = False

        if not self.temp_tareas:
            self.emit("accion-tarea", "end")
            self.__in_run(False)
            self.buttonsbox.set_info("  Tareas Procesadas  ")
            self.buttonsbox.progress.set_progress(100.0)
            return

        codec = self.temp_tareas[0]
        self.temp_tareas.remove(codec)

        dirpath_destino = ""

        if codec in ["jpg", "png"]:
            dirpath_destino = get_imagenes_directory()

        elif codec in ["ogg", "mp3", "wav"]:
            dirpath_destino = get_audio_directory()

        elif codec in ["ogv", "mpeg", "avi"]:
            dirpath_destino = get_video_directory()

        self.__in_run(True)

        gobject.idle_add(self.__new_jamedia_converter,
            codec, dirpath_destino)

    def __new_jamedia_converter(self, codec, dirpath_destino):

        if PR:
            print "WidgetConvert", "__new_jamedia_converter"

        self.player = JAMediaConverter(
            self.path_origen, codec, dirpath_destino)

        self.player.connect("endfile", self.__play_stack_tareas)
        self.player.connect("newposicion", self.__process_tarea)
        self.player.connect("info", self.__info_tarea)

        #gobject.idle_add(self.player.play)
        self.player.play()
        return False

    def __info_tarea(self, player, info):
        self.buttonsbox.set_info(info)

    def __process_tarea(self, player, posicion):
        self.buttonsbox.set_progress(float(posicion))

    def __in_run(self, valor):
        """
        Cuando se ejecutan tareas, se desactivan las botoneras.
        """

        for frame in self.iz_box.get_children():
            vbox = frame.get_child()

            for check in vbox.get_children():
                check.set_sensitive(not valor)

        self.buttonsbox.set_sensitive(not valor)

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

    def salir(self):
        if self.player:
            self.player.stop()
            del(self.player)
            self.player = False

    def play(self):
        self.temp_tareas = self.get_tareas()
        self.__play_stack_tareas()


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
            # FIXME: No Implementados
            check.set_sensitive(False)
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

        self.frame_info = gtk.Frame()
        self.frame_info.set_label("  Progreso  ")
        self.frame_info.set_border_width(5)
        self.frame_info.modify_bg(0, get_colors("toolbars"))

        self.progress = ProgressBar()
        self.frame_info.add(self.progress)
        vbox.pack_end(self.frame_info, False, False, 2)

        event = gtk.EventBox()
        event.set_border_width(5)
        event.modify_bg(0, get_colors("windows"))
        event.add(vbox)

        self.add(event)
        self.show_all()

    def __emit_accion(self, widget):
        self.emit("accion", widget.get_label())
        self.queue_draw()

    def set_info(self, info):
        self.frame_info.set_label("  %s  " % info)
        self.queue_draw()

    def set_progress(self, posicion):
        self.progress.set_progress(posicion)
        self.queue_draw()

    def activar(self, valor):
        event = self.get_child()
        vbox = event.get_child()

        for button in vbox.get_children()[0:3]:
            button.set_sensitive(valor)
