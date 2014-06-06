#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetConverter.py por:
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
#import Pango
import gobject

from Converter.PipelineConverter import PipelineConverter

from Globales import get_colors
from Globales import describe_archivo

gobject.threads_init()
gtk.gdk.threads_init()


class WidgetConverter(gtk.Frame):
    """
    * Conversor de formatos para archivos de audio.
    * Extractor de audio de archivos de video.
    """

    __gsignals__ = {
    'copy_tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    'eliminar_tarea': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self, path):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(os.path.basename(path))
        self.modify_bg(0, get_colors("window"))

        self.path = path
        self.estado = False

        hbox = gtk.HBox()
        hbox.set_border_width(4)

        # checkbuttons + barras de progreso.
        self.frame_formatos = Tareas(self.path)

        hbox.pack_start(
            self.frame_formatos,
            False, False, 5)

        # Botones.
        vbox = gtk.VBox()

        self.boton_ejecutar = gtk.Button(
            "Ejecutar Esta Tarea")
        self.boton_ejecutar.connect(
            "clicked", self.__ejecutar_tarea)
        event = gtk.EventBox()
        event.set_border_width(4)
        event.modify_bg(0, get_colors("window"))
        event.add(self.boton_ejecutar)
        vbox.pack_start(event, False, False, 5)

        boton = gtk.Button("Copiar a Toda la Lista")
        boton.connect("clicked", self.__emit_copy)
        event = gtk.EventBox()
        event.set_border_width(4)
        event.modify_bg(0, get_colors("window"))
        event.add(boton)
        vbox.pack_start(event, False, False, 5)

        boton = gtk.Button("Borrar Tarea")
        boton.connect("clicked", self.__detener_eliminar)
        event = gtk.EventBox()
        event.set_border_width(4)
        event.modify_bg(0, get_colors("window"))
        event.add(boton)
        vbox.pack_start(event, False, False, 5)

        frame = gtk.Frame()
        frame.modify_bg(0, get_colors("window"))
        frame.set_label(" Acciones: ")
        frame.set_border_width(4)
        frame.add(vbox)
        hbox.pack_start(frame, False, False, 5)
        '''
        frame = Gtk.Frame()
        frame.modify_bg(0, get_colors("window"))
        frame.set_label(" Estado: ")
        frame.set_border_width(5)

        self.infowidget = Gtk.TextView()
        self.infowidget.set_editable(False)
        self.infowidget.set_border_width(10)
        self.infowidget.modify_font(
            Pango.FontDescription("Monospace %s" % 7))

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.infowidget)
        frame.add(scroll)

        hbox.pack_start(frame, True, True, 0)
        '''
        self.add(hbox)
        self.show_all()

        self.frame_formatos.connect("end", self.__end)
        self.frame_formatos.connect("info", self.__set_info)

    def __detener_eliminar(self, widget):
        """
        Cuando se hace click en eliminar tarea.
        """

        self.frame_formatos.stop()
        self.emit('eliminar_tarea')

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

        else:
            print "FIXME: Alertar No hay tarea definida."

    def __end(self, widget):
        """
        Cuando Todos los procesos han concluido.
        """

        # FIXME: Ver como alertar, o eliminar la tarea.
        self.boton_ejecutar.set_sensitive(True)
        self.estado = False

    def __emit_copy(self, widget):
        """
        Extiende la tarea configurada a todos
        los archivos en la lista, siempre que estos
        sean del mismo tipo (audio o video) y si su formato
        actual lo permite (ejemplo: no se convierte mp3 a mp3).
        """

        self.emit('copy_tarea', self.frame_formatos.tarea)

    def __set_info(self, widget, info):
        '''
        buf = self.infowidget.get_buffer()

        text = buf.get_text(
            buf.get_start_iter(),
            buf.get_end_iter(), True)

        if text:
            info = "%s\n%s" % (text, info)

        buf.set_text(info)
        '''
        print info

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


class Tareas(gtk.Frame):

    __gsignals__ = {
    "end": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "info": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self, path):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(" Archivos de Salida: ")
        self.modify_bg(0, get_colors("window"))

        self.path = path
        self.tarea = {
            'mp3': False,
            'ogg': False,
            'wav': False,
            'ogv': False,
            }

        self.barras = {}
        self.players = {}

        extension = os.path.splitext(
            os.path.split(self.path)[1])[1].replace('.', "")

        vbox = gtk.VBox()

        datos = describe_archivo(self.path)

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

        # FIXME: hack: extension != 'ogg' (algunos ogg solo tienen audio)
        if extension != 'ogv' and extension != 'ogg' and \
            ('video' in datos or 'application/ogg' in datos or \
            'application/octet-stream' in datos):
            vbox.pack_start(
                self.__get_item_format('ogv'),
                True, True, 0)

        self.add(vbox)
        self.show_all()

    def __get_item_format(self, formato):
        """
        Checkbuttons para seleccionar formatos
        de salida.
        """

        box = gtk.HBox()

        boton = CheckButton(formato)
        boton.connect('set_data', self.__set_data)
        box.pack_start(boton, True, True, 5)

        barra = BarraProgreso()
        box.pack_start(barra,
            False, False, 0)

        self.barras[formato] = barra

        return box

    def __set_data(self, widget, formato, active):
        """
        Setea datos de tarea según selecciones del usuario
        en los checkbuttons.
        """

        self.tarea[formato] = active

    def __procesar_tareas(self):

        if not self.players:
            self.set_sensitive(True)
            self.emit("end")
            return

        formato = self.players.keys()[0]

        self.players[formato] = PipelineConverter(
            self.path, formato)

        self.players[formato].connect('endfile', self.__set_end)
        self.players[formato].connect('newposicion', self.__set_posicion)
        self.players[formato].connect('info', self.__set_info)

        self.players[formato].play()

        return False

    def __set_end(self, player):
        """
        Cuando todos los procesos han terminado
        se emite end.
        """

        self.barras[player.codec].set_progress(100.0)

        del(self.players[player.codec])
        del(player)

        gobject.idle_add(self.__procesar_tareas)

    def __set_info(self, player, info):

        self.emit("info", info)

    def __set_posicion(self, player, posicion):

        self.barras[player.codec].set_progress(float(posicion))
        return True

    def setear(self, tarea):
        """
        Configura la tarea segun copia desde otro item.
        """

        for key in self.barras.keys():
            self.barras[key].set_progress(0.0)

        for hbox in self.get_child().get_children():
            check = hbox.get_children()[0]

            if check.get_label() in tarea.keys():
                valor = tarea.get(check.get_label(), False)
                check.set_active(valor)

    def stop(self):
        """
        Detiene todos los procesos.
        """

        for formato in self.players.keys():
            if self.players[formato]:
                self.players[formato].stop()
                del(self.players[formato])

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

        self.__set_info(None, "")
        self.set_sensitive(False)

        for formato in formatos:
            self.players[formato] = None

            self.players[formato] = PipelineConverter(
                self.path, formato)

            self.players[formato].connect('endfile', self.__set_end)
            #self.players[formato].connect('estado', self.__set_estado)
            self.players[formato].connect('newposicion', self.__set_posicion)
            self.players[formato].connect('info', self.__set_info)

            #self.players[formato].play()

        gobject.idle_add(self.__procesar_tareas)

        return True


class CheckButton(gtk.CheckButton):

    __gsignals__ = {
    'set_data': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN))}

    def __init__(self, formato):

        gtk.CheckButton.__init__(self)
        self.set_label(formato)
        self.show_all()

    def do_toggled(self):

        self.emit('set_data', self.get_label(),
            self.get_active())


class BarraProgreso(gtk.ProgressBar):

    def __init__(self):

        gtk.ProgressBar.__init__(self)

        self.set_size_request(200, 5)
        self.modify_bg(0, get_colors("window"))

        self.valor = 0.0

        #self.modify_font(
        #    Pango.FontDescription("Monospace %s" % 6))
        self.set_show_text(True)

        #self.set_margin_bottom(10)
        #self.set_margin_left(10)
        #self.set_margin_right(10)
        #self.set_margin_top(10)

        self.show_all()

    def set_progress(self, valor=0):

        if valor > 0:
            valor = valor / 100

        else:
            valor = 0.0

        if self.valor != valor:
            self.valor = valor
            self.set_fraction(self.valor)
            self.queue_draw()
