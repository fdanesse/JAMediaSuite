#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetAudioTarea.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM! - Uruguay
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
from gi.repository import GObject
from gi.repository import GLib

from JAMediaObjects.JAMediaGlobales import get_boton
#from JAMediaObjects.JAMediaGlobales import get_separador
from JAMediaObjects.JAMediaGlobales import get_pixels

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]


class WidgetAudioTarea(Gtk.Frame):
    """
    * Conversor de formatos para archivos de audio.
    * Extractor de audio de archivos de video.
    """

    __gtype_name__ = 'JAMediaConverterWidgetAudioTarea'

    __gsignals__ = {
    'copy_tarea': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    'eliminar_tarea': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, path):

        Gtk.Frame.__init__(self)

        self.set_border_width(5)
        self.set_label(os.path.basename(path))

        self.path = path
        self.estado = False
        self.tarea = {
            'mp3': [False, False],
            'ogg': [False, False],
            'wav': [False, False],
            }

        self.boton_ejecutar = False
        self.control_tarea = False

        hbox = Gtk.HBox()
        hbox.set_border_width(5)

        self.frame_formatos = self.__get_frame_format()
        boton = Gtk.Button("Borrar Tarea")
        boton.connect("clicked", self.__detener_eliminar)

        hbox.pack_start(
            self.frame_formatos,
            False, False, 5)
        hbox.pack_start(
            self.__get_controles(),
            False, False, 5)

        hbox.pack_end(
            boton,
            False, False, 5)

        self.add(hbox)
        self.show_all()

    def __get_controles(self):
        """
        * visor, barra de progreso, boton stop
        * boton ejecutar tarea
        * boton copiar tarea
        """

        box = Gtk.VBox()

        self.control_tarea = ControlTarea(self.path)
        box.pack_start(self.control_tarea, False, False, 5)

        self.boton_ejecutar = Gtk.Button("Ejecutar Esta Tarea")
        self.boton_ejecutar.connect("clicked", self.__ejecutar_tarea)
        box.pack_start(self.boton_ejecutar, True, True, 5)

        boton = Gtk.Button("Ejecutar en Todos los Archivos")
        boton.connect("clicked", self.__emit_copy_tarea)
        box.pack_start(boton, True, True, 5)

        return box

    def __get_frame_format(self):
        """
        Frame para Checkbuttons para seleccionar formatos
        de salida y quitar voz.
        """

        extension = os.path.splitext(
            os.path.split(self.path)[1])[1].replace('.', "")

        frame_formatos = Gtk.Frame()
        frame_formatos.set_border_width(5)
        frame_formatos.set_label(" Archivos de Salida: ")

        vbox = Gtk.VBox()

        if extension != 'mp3':
            vbox.pack_start(
                self.__get_item_format('mp3'),
                True, True, 0)

        if extension != 'ogg':
            vbox.pack_start(
                self.__get_item_format('ogg'),
                True, True, 0)

        if extension != 'wav':
            vbox.pack_start(
                self.__get_item_format('wav'),
                True, True, 0)

        frame_formatos.add(vbox)

        return frame_formatos

    def __get_item_format(self, formato):
        """
        Checkbuttons para seleccionar formatos
        de salida y quitar voz.
        """

        box = Gtk.HBox()

        boton = CheckButton(formato, formato)
        boton.connect('set_data', self.__set_data)
        box.pack_start(boton, True, True, 5)

        boton = CheckButton('Quitar voz', formato)
        boton.connect('set_data', self.__set_data)
        box.pack_start(boton, True, True, 5)

        return box

    def setear(self, tarea):
        """
        Configura la tarea segun copia desde otro item.
        """

        for hbox in self.frame_formatos.get_child().get_children():
            formato, voz = hbox.get_children()

            formato.set_active(tarea[formato.get_label()][0])
            voz.set_active(tarea[formato.get_label()][1])

    def __detener_eliminar(self, widget):
        """
        Cuando se hace click en eliminar tarea.
        """

        # FIXME: detener tarea
        self.emit('eliminar_tarea')

    def __set_data(self, widget, label, active, formato):
        """
        Setea datos de tarea según selecciones del usuario
        en los checkbuttons.
        """

        if 'Quitar voz' in label:
            self.tarea[formato][1] = active

            if active:
                widget.get_parent().get_children()[0].set_active(True)

            return

        if 'mp3' in formato:
            self.tarea[formato][0] = active

            if not active:
                widget.get_parent().get_children()[1].set_active(False)

        elif 'ogg' in formato:
            self.tarea[formato][0] = active

            if not active:
                widget.get_parent().get_children()[1].set_active(False)

        elif 'wav' in formato:
            self.tarea[formato][0] = active

            if not active:
                widget.get_parent().get_children()[1].set_active(False)

    def __ejecutar_tarea(self, widget):
        """
        Ejecuta la tarea configurada.
        """

        elementos = []

        for key in self.tarea.keys():
            if self.tarea[key][0]:
                # elemento = key, tarea[key][1]
                # key = mp3, tarea[key][1] = sin voz
                elementos.append([key, self.tarea[key][1]])

        if not elementos:
            print "FIXME: Alertar No hay tarea definida."
            return

        self.frame_formatos.set_sensitive(False)
        self.boton_ejecutar.hide()
        self.estado = True
        self.control_tarea.run(elementos)
        # FIXME: cambiar estado o eliminar tarea al detener o terminar.

    def __emit_copy_tarea(self, widget):
        """
        Extiende la tarea configurada a todos
        los archivos en la lista, siempre que estos
        sean del mismo tipo (audio o video) y si su formato
        actual lo permite (ejemplo: no se convierte mp3 a mp3).
        """

        for key in self.tarea.keys():
            if self.tarea[key][0]:
                self.emit('copy_tarea', self.tarea)
                return


class CheckButton(Gtk.CheckButton):

    __gtype_name__ = 'JAMediaConverterCheckButton'

    __gsignals__ = {
    'set_data': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN, GObject.TYPE_STRING))}

    def __init__(self, text, formato):

        Gtk.CheckButton.__init__(self)

        self.set_label(text)

        self.formato = formato

        self.show_all()

    def do_toggled(self):

        self.emit(
            'set_data', self.get_label(),
            self.get_active(), self.formato)


class ControlTarea(Gtk.Frame):

    def __init__(self, path):

        Gtk.Frame.__init__(self)

        self.set_border_width(5)
        self.set_label(" Progreso: ")

        self.path = path
        self.player = False

        hbox = Gtk.HBox()
        hbox.set_border_width(5)

        self.drawing = Gtk.DrawingArea()
        self.drawing.set_size_request(80, 60)
        self.drawing.modify_bg(0, Gdk.Color(0, 0, 0))

        hbox.pack_start(
            self.drawing,
            False, False, 5)

        from JAMediaObjects.JAMediaWidgets import BarraProgreso

        self.barra = BarraProgreso()
        self.barra.set_size_request(200, -1)
        self.barra.set_border_width(10)
        self.barra.set_sensitive(False)
        #self.barradeprogreso2.set_progress(
        #    100.0 * 1.0 / float(len(self.lista)))
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1), tooltip_text="Detener")
        boton.connect("clicked", self.__stop)

        hbox.pack_start(
            self.barra,
            False, False, 0)
        hbox.pack_start(
            boton,
            False, False, 0)

        self.add(hbox)

        self.connect('realize', self.__realize)

        self.show_all()

    def __realize(self, widget):

        GLib.idle_add(self.hide)

    def __stop(self, widget):
        """
        Detiene la ejecucion de la tarea.
        """

        pass
        # detener tarea.
        # reactivar controles

    def run(self, tareas):
        """
        Ejecuta la tarea.
        """

        from AudioExtractor import AudioExtractor

        self.show()

        from gi.repository import GdkX11
        from gi.repository import GstVideo

        # Crear y Lanzar Pipeline.
        ventana_id = self.drawing.get_property(
            'window').get_xid()
        self.player = AudioExtractor(
            ventana_id, self.path, tareas)

        self.player.connect('endfile', self.__set_end)
        #self.player.connect('estado', self.__set_estado)
        self.player.connect('newposicion', self.__set_posicion)
        self.player.connect('info', self.__set_info)

        self.player.play()

    def __set_end(self, player):

        #self.stop()
        #GLib.idle_add(self.play)
        pass

    def __set_info(self, player, info):

        #self.info_widget.set_info(info)
        pass

    def __set_posicion(self, player, posicion):

        self.barra.set_progress(float(posicion))
        #self.info_widget.set_cantidad(len(self.lista))

        if float(posicion) == 100.0:
            # Pista de audio siempre termina antes
            # si no se envia a la salida por default.
            #self.stop()
            #self.play()
            pass
