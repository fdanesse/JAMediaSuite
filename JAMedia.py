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
from gi.repository import GLib
from gi.repository import GObject

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMedia.JAMedia import JAMediaPlayer

GObject.threads_init()


class Ventana(Gtk.Window):

    __gtype_name__ = 'Ventana'

    def __init__(self):

        super(Ventana, self).__init__()

        self.set_title("JAMedia")

        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.pistas = ""

        self.socket = Gtk.Socket()
        self.add(self.socket)

        self.jamediaplayer = JAMediaPlayer()
        self.socket.add_id(self.jamediaplayer.get_id())

        self.show_all()
        self.realize()

        self.connect("delete-event", self.__salir)
        self.jamediaplayer.connect('salir', self.__salir)

        GLib.idle_add(self.__setup_init)

    def set_pistas(self, pistas):
        """
        Cuando se abre con una lista de archivos.
        """

        self.pistas = pistas

    def __setup_init(self):

        self.jamediaplayer.setup_init()
        self.jamediaplayer.pack_standar()
        self.jamediaplayer.pack_efectos()

        if self.pistas:
            GLib.idle_add(
                self.jamediaplayer.set_nueva_lista,
                self.pistas)

        return False

    def __salir(self, widget=None, senial=None):

        import sys
        import commands

        commands.getoutput('killall mplayer')
        sys.exit(0)


def get_item_list(path):

    if os.path.exists(path):
        if os.path.isfile(path):
            archivo = os.path.basename(path)

            from JAMediaObjects.JAMFileSystem import describe_archivo

            datos = describe_archivo(path)

            if 'audio' in datos or \
                'video' in datos or \
                'application/ogg' in datos:
                    return [archivo, path]

    return False

if __name__ == "__main__":

    import sys

    items = []

    if len(sys.argv) > 1:

        for campo in sys.argv[1:]:
            path = os.path.join(campo)

            if os.path.isfile(path):
                item = get_item_list(path)

                if item:
                    items.append(item)

            elif os.path.isdir(path):

                for arch in os.listdir(path):
                    newpath = os.path.join(path, arch)

                    if os.path.isfile(newpath):
                        item = get_item_list(newpath)

                        if item:
                            items.append(item)

        if items:
            jamedia = Ventana()
            jamedia.set_pistas(items)

        else:
            jamedia = Ventana()

    else:
        jamedia = Ventana()

    Gtk.main()
