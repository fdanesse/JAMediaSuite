#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Help.py por:
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

import os
from gi.repository import Gtk
from gi.repository import GdkX11
from Widgets import DialogoLoad
from HelpWidget import HelpWidget

screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()

BASEPATH = os.path.dirname(__file__)


class Help(Gtk.Window):

    __gtype_name__ = 'JAMediaEditorHelp'

    def __init__(self, parent_window):

        Gtk.Window.__init__(self)

        self.parent_window = parent_window

        self.set_title("Help de JAMediaEditor")
        self.set_icon_from_file(
            os.path.join(BASEPATH, "Iconos", "einsteintux.png"))
        self.set_transient_for(self.parent_window)
        self.set_border_width(15)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox.pack_start(Gtk.Label("Constructor de Instaladores"),
            False, False, 0)

        self.resize(w / 2, h - 40)
        self.move(w - w / 2, 40)

        self.add(self.vbox)
        self.show_all()

    def set_help(self, texto):
        for child in self.vbox.get_children():
            self.vbox.remove(child)
            child.destroy()
        t = "Cargando . . ."
        t = "%s\n%s" % (t, "Por favor espera un momento.")
        dialogo = DialogoLoad(self, t)
        dialogo.connect("running", self.__load, texto)
        dialogo.run()

    def __load(self, dialogo, texto):
        help = HelpWidget(texto)
        self.vbox.pack_start(help, True, True, 0)
        dialogo.destroy()
        self.show_all()
