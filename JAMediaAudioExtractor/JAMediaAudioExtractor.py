#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaAudioExtractor.py por:
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
from gi.repository import Gst
from gi.repository import GstVideo
from gi.repository import GObject
from gi.repository import GdkX11
from gi.repository import GLib

from Extractor import Extractor

GObject.threads_init()
Gst.init([])


def get_data(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    """

    import commands

    datos = commands.getoutput(
        'file -ik %s%s%s' % ("\"", archivo, "\""))

    retorno = ""

    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)

    return retorno


PATH = os.path.dirname(__file__)

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(
    PATH, "Estilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)


class JAMediaAudioExtractor(Gtk.Plug):

    __gtype_name__ = 'JAMediaAudioExtractor'

    __gsignals__ = {
    "salir": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, origen, codec):
        """
        JAMediaAudioExtractor: Gtk.Plug para embeber en otra aplicacion.
        """

        Gtk.Plug.__init__(self, 0L)

        #self.set_size_request(320, 240)

        self.player = False
        self.lista = origen
        self.codec = codec  # FIXME: setear Menu

        basebox = Gtk.VBox()
        hbox = Gtk.HBox()
        vbox = Gtk.VBox()

        from JAMediaObjects.JAMediaWidgets import BarraProgreso
        from Widgets import Widget_extractor
        from Widgets import Menu
        from Widgets import InfoBox

        self.menu = Menu()
        self.widget_extractor = Widget_extractor()
        self.barradeprogreso = BarraProgreso()
        self.barradeprogreso.set_sensitive(False)
        self.barradeprogreso2 = BarraProgreso()
        self.barradeprogreso2.set_sensitive(False)

        basebox.pack_start(self.menu, False, False, 0)
        basebox.pack_start(hbox, True, True, 0)

        vbox.pack_start(self.widget_extractor, True, True, 0)
        vbox.pack_start(self.barradeprogreso, False, False, 0)
        vbox.pack_start(self.barradeprogreso2, False, False, 0)

        self.info_widget = InfoBox()

        hbox.pack_start(vbox, True, True, 0)
        hbox.pack_start(self.info_widget, False, False, 0)

        self.add(basebox)

        self.show_all()
        self.realize()

        self.connect("embedded", self.__embed_event)
        self.menu.connect('load', self.__add_file)
        self.menu.connect('accion_formato', self.__set_formato)

        if self.lista:
            GLib.idle_add(self.play)

    def __set_formato(self, widget, formato):

        self.codec = formato

    def __add_file(self, widget, lista):
        """
        Agrega archivos a la lista a procesar.
        """

        for origen in lista:
            if os.path.isdir(origen):
                for archivo in os.listdir(origen):
                    arch = os.path.join(origen, archivo)

                    datos = get_data(arch)
                    if "video" in datos or \
                        'audio' in datos or \
                        'application/ogg' in datos:
                        if not arch in self.lista:
                            self.lista.append(arch)

            elif os.path.isfile(origen):
                datos = get_data(origen)
                if "video" in datos or \
                    'audio' in datos or \
                    'application/ogg' in datos:
                    if not origen in self.lista:
                        self.lista.append(origen)

        if self.lista and not self.player:
            GLib.idle_add(self.play)

    def __embed_event(self, widget):
        """
        No hace nada por ahora.
        """

        print "JAMediaAudioExtractor => OK"

    def play(self):
        """
        Comienza a Procesar los archivos en la lista.
        """

        self.menu.set_sensitive(False)

        self.info_widget.reset()

        if self.lista:
            self.barradeprogreso2.set_progress(
                100.0 * 1.0 / float(len(self.lista)))

        else:
            self.barradeprogreso2.set_progress(100.0)

        if not self.lista or self.player:
            dialog = Gtk.Dialog(
                title="JAMedia Audio Extractor",
                parent=self.get_toplevel(),
                flags=Gtk.DialogFlags.MODAL,
                buttons=[
                    "OK", Gtk.ResponseType.ACCEPT])

            dialog.set_size_request(300, 100)
            dialog.set_border_width(10)

            label = Gtk.Label(
                "Sin Archivos para Procesar.")

            label.show()
            dialog.vbox.add(label)

            dialog.run()
            dialog.destroy()

            self.menu.set_sensitive(True)
            return

        origen = self.lista[0]
        self.lista.remove(origen)

        self.player = Extractor(
            self.widget_extractor.visor.get_property(
            'window').get_xid(), origen, self.codec)

        self.widget_extractor.set_extraccion(origen)

        self.player.connect('endfile', self.__set_end)
        #self.player.connect('estado', self.__set_estado)
        self.player.connect('newposicion', self.__set_posicion)
        self.player.connect('info', self.__set_info)

        self.player.play()

        return False

    def stop(self):
        """
        Detiene todos los procesos y actualiza los widgets.
        """

        if self.player:
            self.player.stop()
            self.widget_extractor.reset()
            self.barradeprogreso.set_progress(0.0)
            self.barradeprogreso2.set_progress(0.0)
            self.info_widget.reset()

            if self.player:
                del(self.player)
                self.player = False

    def __set_end(self, player):

        self.stop()
        GLib.idle_add(self.play)

    #def __set_estado(self, player, estado):

    #    #print "Estado:", estado
    #    pass

    def __set_info(self, player, info):

        self.info_widget.set_info(info)

    def __set_posicion(self, player, posicion):

        self.barradeprogreso.set_progress(float(posicion))
        self.info_widget.set_cantidad(len(self.lista))

        if float(posicion) == 100.0:
            # Pista de audio siempre termina antes
            # sin no se envia a la salida por default.
            self.stop()
            self.play()
