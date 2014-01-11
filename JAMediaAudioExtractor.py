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
import sys

from gi.repository import Gtk

import JAMediaObjects
from JAMediaAudioExtractor.JAMediaAudioExtractor import JAMediaAudioExtractor


class Ventana(Gtk.Window):

    __gtype_name__ = 'Ventana'

    def __init__(self, origen, codec):

        Gtk.Window.__init__(self)

        self.set_title("JAMedia Audio Extractor")

        self.set_resizable(False)
        #self.set_size_request(320, 240)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.socket = Gtk.Socket()
        self.add(self.socket)

        self.jamediaaudioextractor = JAMediaAudioExtractor(
            origen, codec)
        self.socket.add_id(
            self.jamediaaudioextractor.get_id())

        self.show_all()
        self.realize()

        self.connect("delete-event", self.__exit)
        self.jamediaaudioextractor.connect("salir", self.__exit)

    def __exit(self, widget=None, senial=None):

        if self.jamediaaudioextractor:
            self.jamediaaudioextractor.stop()

        sys.exit(0)


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


if __name__ == "__main__":

    origen = False

    if len(sys.argv) > 1:
        origen = sys.argv[1]

    codec = "mp3"
    lista = []

    if len(sys.argv) > 2:
        codec = str(sys.argv[2]).lower()

    if origen:
        # Directorio
        if os.path.isdir(origen):
            for archivo in os.listdir(origen):
                arch = os.path.join(origen, archivo)

                datos = get_data(arch)
                if "video" in datos or \
                    'audio' in datos or \
                    'application/ogg' in datos:
                    lista.append(arch)

        # Archivo
        elif os.path.isfile(origen):
            datos = get_data(arch)
            if "video" in datos or \
                'audio' in datos or \
                'application/ogg' in datos:
                lista.append(origen)

    Ventana(lista, codec)
    Gtk.main()
