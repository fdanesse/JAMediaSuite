#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetAudioConverter.py por:
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


class WidgetAudioConverter(Gtk.Frame):
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

        hbox = Gtk.HBox()
        hbox.set_border_width(5)

        # checkbuttons + barras de progreso.
        self.frame_formatos = Tareas(self.path)

        hbox.pack_start(
            self.frame_formatos,
            False, False, 5)

        # Botones.
        vbox = Gtk.VBox()

        self.boton_ejecutar = Gtk.Button("Ejecutar Esta Tarea")
        self.boton_ejecutar.connect("clicked", self.__ejecutar_tarea)
        vbox.pack_start(self.boton_ejecutar, True, True, 5)

        boton = Gtk.Button("Copiar a Toda la Lista")
        boton.connect("clicked", self.__emit_copy)
        vbox.pack_start(boton, True, True, 5)

        boton = Gtk.Button("Borrar Tarea")
        boton.connect("clicked", self.__detener_eliminar)
        vbox.pack_start(boton, False, False, 5)

        hbox.pack_start(vbox, False, False, 5)

        self.add(hbox)
        self.show_all()

        self.frame_formatos.connect("end", self.__end)

    def __detener_eliminar(self, widget):
        """
        Cuando se hace click en eliminar tarea.
        """

        self.frame_formatos.stop()
        self.emit('eliminar_tarea')

    def stop(self):

        self.frame_formatos.stop()

    def setear(self, tarea):
        """
        Configura la tarea según copia desde otro item.
        """

        if self.estado:
            return

        self.frame_formatos.setear(tarea)
        #GLib.idle_add(self.__ejecutar_tarea, None)

    def __ejecutar_tarea(self, widget):
        """
        Ejecuta la tarea configurada.
        """

        if self.estado:
            print "Esta tarea se encuentra en ejecución"
            return

        if self.frame_formatos.run():
            self.boton_ejecutar.set_sensitive(False)
            self.estado = True
            print "FIXME: cambiar estado o eliminar tarea al detener o terminar."

        else:
            print "FIXME: Alertar No hay tarea definida."

    def __end(self, widget):
        """
        Cuando Todos los procesos han concluido.
        """

        self.boton_ejecutar.set_sensitive(True)
        self.estado = False
        print "FIXME: Tarea Concluida."

    def __emit_copy(self, widget):
        """
        Extiende la tarea configurada a todos
        los archivos en la lista, siempre que estos
        sean del mismo tipo (audio o video) y si su formato
        actual lo permite (ejemplo: no se convierte mp3 a mp3).
        """

        self.emit('copy_tarea', self.frame_formatos.tarea)


class Tareas(Gtk.Frame):

    __gsignals__ = {
    "end": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, path):

        Gtk.Frame.__init__(self)

        self.path = path
        self.tarea = {
            'mp3': False,
            'ogg': False,
            'wav': False,
            }

        self.barras = {}
        self.players = {}

        extension = os.path.splitext(
            os.path.split(self.path)[1])[1].replace('.', "")

        self.set_border_width(5)
        self.set_label(" Archivos de Salida: ")

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

        self.add(vbox)

        self.show_all()

    def __get_item_format(self, formato):
        """
        Checkbuttons para seleccionar formatos
        de salida y quitar voz.
        """

        box = Gtk.HBox()

        boton = CheckButton(formato)
        boton.connect('set_data', self.__set_data)
        box.pack_start(boton, True, True, 5)

        from JAMediaObjects.JAMediaWidgets import BarraProgreso

        barra = BarraProgreso()
        barra.set_size_request(200, -1)
        barra.set_border_width(10)
        barra.set_sensitive(False)

        box.pack_start(barra,
            False, False, 0)

        self.barras[formato] = barra

        return box

    def __set_data(self, widget, formato, active):
        """
        Setea datos de tarea según selecciones del usuario
        en los checkbuttons.
        """

        if 'mp3' in formato:
            self.tarea[formato] = active

        elif 'ogg' in formato:
            self.tarea[formato] = active

        elif 'wav' in formato:
            self.tarea[formato] = active

    def setear(self, tarea):
        """
        Configura la tarea segun copia desde otro item.
        """

        for key in self.barras.keys():
            self.barras[key].set_progress(0.0)

        for hbox in self.get_child().get_children():
            formato = hbox.get_children()[0]
            formato.set_active(tarea[formato.get_label()])

    def stop(self):
        """
        Detiene todos los procesos.
        """

        for formato in self.players.keys():
            self.players[formato].stop()

    def run(self):
        """
        Ejecuta la tarea configurada.
        """

        formatos = []

        for key in self.tarea.keys():
            if self.tarea[key]:
                formatos.append(key)

        if not formatos:
            return False

        self.set_sensitive(False)
        print "FIXME: cambiar estado o eliminar tarea al detener o terminar."

        from AudioConverter import AudioConverter

        for formato in formatos:
            self.players[formato] = AudioConverter(
                False, self.path, formato)

            self.players[formato].connect('endfile', self.__set_end)
            #self.players[formato].connect('estado', self.__set_estado)
            self.players[formato].connect('newposicion', self.__set_posicion)
            self.players[formato].connect('info', self.__set_info)

            self.players[formato].play()

        return True

    def __set_end(self, player):
        """
        Cuando todos los procesos han terminado
        se emite end.
        """

        del(self.players[player.codec])
        del(player)

        if not self.players:
            self.set_sensitive(True)
            self.emit("end")

    def __set_info(self, player, info):

        print info

    def __set_posicion(self, player, posicion):

        self.barras[player.codec].set_progress(float(posicion))

        if float(posicion) == 100.0:
            # Pista de audio siempre termina antes
            # si no se envia a la salida por default.
            #self.stop()
            #self.play()
            pass

        return True


class CheckButton(Gtk.CheckButton):

    __gtype_name__ = 'JAMediaConverterCheckButton'

    __gsignals__ = {
    'set_data': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN))}

    def __init__(self, formato):

        Gtk.CheckButton.__init__(self)

        self.set_label(formato)

        self.show_all()

    def do_toggled(self):

        self.emit('set_data', self.get_label(),
            self.get_active())
