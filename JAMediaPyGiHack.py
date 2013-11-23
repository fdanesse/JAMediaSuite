#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
#       Flavio Danesse <fdanesse@gmail.com>, <fdanesse@activitycentral.com>
#       CeibalJAM - Uruguay - Activity Central

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

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]


class Ventana(Gtk.Window):

    __gtype_name__ = 'VentanaJAMediaPyGiHack'

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("JAMediaPygiHack")

        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "PygiHack.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.maximize()
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        from JAMediaPyGiHack.JAMediaPyGiHack import JAMediaPyGiHack

        jamediapygihack = JAMediaPyGiHack()
        self.add(jamediapygihack)

        self.show_all()
        self.realize()

        jamediapygihack.connect("salir", self.__salir)
        self.connect("delete-event", self.__salir)

    def __salir(self, widget=None, senial=None):

        import sys
        sys.exit(0)

if __name__ == "__main__":
    Ventana()
    Gtk.main()
