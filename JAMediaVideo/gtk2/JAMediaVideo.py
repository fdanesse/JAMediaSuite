#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaVideo.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
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

import gtk
from gtk import gdk
import gobject

#from Globales import get_audio_directory
#from Globales import get_imagenes_directory
#from Globales import get_video_directory
from Globales import get_colors

from Toolbars import Toolbar
from Toolbars import ToolbarSalir
from BasePanel import BasePanel

BASE_PATH = os.path.dirname(__file__)

gobject.threads_init()
gtk.gdk.threads_init()


class JAMediaVideo(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("JAMediaVideo")
        self.set_icon_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMediaVideo.svg"))
        self.set_resizable(True)
        self.set_default_size(437, 328)
        self.set_border_width(4)
        self.modify_bg(0, get_colors("toolbars"))
        self.set_position(gtk.WIN_POS_CENTER)

        vbox = gtk.VBox()
        self.add(vbox)
        self.show_all()

        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.base_panel = BasePanel()

        vbox.pack_start(self.toolbar, False, True, 4)
        vbox.pack_start(self.toolbar_salir, False, True, 4)
        vbox.pack_start(self.base_panel, True, True, 0)

        self.toolbar.connect("accion", self.__set_accion)
        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar.connect("config-show", self.__config_show)
        self.toolbar.connect("nueva_camara", self.__nueva_camara)
        self.toolbar_salir.connect('salir', self.__salir)

        self.connect("delete-event", self.__salir)

        self.show_all()
        self.realize()

        gobject.idle_add(self.__run)

    def __set_accion(self, widget, modo, accion):

        self.base_panel.set_accion(modo, accion)

    def __config_show(self, toolbar, tipo):

        self.base_panel.config_show(tipo)

    def __nueva_camara(self, widget, tipo):

        self.base_panel.nueva_camara(tipo)

    def __run(self):

        self.toolbar_salir.hide()
        self.base_panel.pack_efectos()
        self.toolbar.switch("menu")

    def __confirmar_salir(self, widget=None, senial=None):

        self.toolbar_salir.run("JAMediaVideo")

    def __salir(self, widget=None, senial=None):

        self.base_panel.salir()
        gtk.main_quit()
        sys.exit(0)


if __name__ == "__main__":

    JAMediaVideo()
    gtk.main()
