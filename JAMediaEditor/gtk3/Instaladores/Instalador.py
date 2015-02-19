#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Instalador.py por:
#       Flavio Danesse      <fdanesse@gmail.com>

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

from gi.repository import Gtk
from gi.repository import GdkX11

screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()


class Instalador(Gtk.Window):
    """
    Dialogo para presentar Información de Instaladores.
    """

    __gtype_name__ = 'JAMediaEditorInstalador'

    def __init__(self, parent_window, path):

        Gtk.Window.__init__(self)

        self.parent_window = parent_window
        self.set_title("Constructor de Instaladores de Proyecto")
        self.set_transient_for(self.parent_window)
        self.set_border_width(15)

        self.resize(w / 2, h - 40)
        self.move(w - w / 2, 40)

        #self.add(scroll)
        self.show_all()
