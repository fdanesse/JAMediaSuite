#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMedia.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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
from gi.repository import GObject
from gi.repository import GLib

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects

from JAMediaObjects.JAMediaGlobales import get_separador
from JAMediaObjects.JAMediaGlobales import get_pixels
from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_color

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaAudioExtractor.JAMediaAudioExtractor import JAMediaAudioExtractor
from JAMediaVideoConvert.JAMediaVideoConvert import JAMediaVideoConvert
from JAMedia.JAMedia import JAMediaPlayer


class Ventana(Gtk.Window):

    __gtype_name__ = 'Ventana'

    def __init__(self):

        super(Ventana, self).__init__()

        self.set_title("JAMedia Converter")

        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.pistas = ""

        vbox = Gtk.VBox()
        toolbar = Toolbar()
        vbox.pack_start(
            toolbar, False, False, 0)

        self.audioextractorsocket = Gtk.Socket()
        self.audioextractor = JAMediaAudioExtractor([], 'ogg')

        vbox.pack_start(
            self.audioextractorsocket, True, True, 0)

        self.videoconvertsocket = Gtk.Socket()
        self.videoconvert = JAMediaVideoConvert([], 'ogg')

        vbox.pack_start(
            self.videoconvertsocket, True, True, 0)

        self.jamediasocket = Gtk.Socket()
        self.jamediaplayer = JAMediaPlayer()

        vbox.pack_start(
            self.jamediasocket, True, True, 0)

        self.add(vbox)

        self.show_all()
        self.realize()

        toolbar.connect('switch', self.__switch)
        toolbar.connect('salir', self.__salir)
        self.connect("delete-event", self.__salir)
        #self.jamediaplayer.connect('salir', self.__salir)

        GLib.idle_add(self.__setup_init)

    def __switch(self, widget, tipo):

        if tipo == 'jamedia':
            self.audioextractorsocket.hide()
            self.videoconvertsocket.hide()
            self.jamediasocket.show()

        elif tipo == 'videoconvert':
            self.audioextractorsocket.hide()
            self.jamediasocket.hide()
            self.videoconvertsocket.show()

        elif tipo == 'audioextractor':
            self.videoconvertsocket.hide()
            self.jamediasocket.hide()
            self.audioextractorsocket.show()

    '''
    def set_pistas(self, pistas):
        """
        Cuando se abre con una lista de archivos.
        """

        self.pistas = pistas
    '''
    def __setup_init(self):

        self.jamediasocket.add_id(
            self.jamediaplayer.get_id())

        self.audioextractorsocket.add_id(
            self.audioextractor.get_id())

        self.videoconvertsocket.add_id(
            self.videoconvert.get_id())

        self.jamediaplayer.setup_init()
        self.jamediaplayer.pack_standar()
        self.jamediaplayer.pack_efectos()
        '''
        if self.pistas:
            GLib.idle_add(
                self.jamediaplayer.set_nueva_lista,
                self.pistas)
        '''

        self.__switch(None, 'jamedia')

        return False

    def __salir(self, widget=None, senial=None):

        import sys

        if self.audioextractor:
            self.audioextractor.stop()

        if self.videoconvert:
            self.videoconvert.stop()

        #import commands

        #commands.getoutput('killall mplayer')
        sys.exit(0)


class Toolbar(Gtk.Toolbar):

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'switch': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Reproductor")
        boton.connect(
            "clicked", self.__emit_switch, 'jamedia')
        self.insert(boton, -1)

        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaExtractor.svg")
        self.jamedia = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        self.jamedia.set_tooltip_text("Extractor de Audio")
        self.jamedia.connect(
            "clicked", self.__emit_switch, 'audioextractor')
        self.insert(self.jamedia, -1)

        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaConvert.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Conversor de Video")
        boton.connect(
            "clicked", self.__emit_switch, 'videoconvert')
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.show_all()

    def __emit_switch(self, widget, tipo):

        self.emit('switch', tipo)

    def __salir(self, widget):
        """
        Cuando se hace click en el boton salir.
        """

        self.emit('salir')


if __name__ == "__main__":
    Ventana()
    Gtk.main()
