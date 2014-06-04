#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaConverter.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

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
import gobject
import gtk

from BasePanel import BasePanel
#from Widgets import Toolbar

from Globales import get_colors

BASEPATH = os.path.dirname(__file__)

gobject.threads_init()
gtk.gdk.threads_init()


class Ventana(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("JAMedia Converter")

        self.set_icon_from_file(
            os.path.join(BASEPATH,
            "Iconos", "JAMediaConvert.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)
        self.modify_bg(0, get_colors("toolbars"))

        vbox = gtk.VBox()
        base_panel = BasePanel()

        #self.toolbar = Toolbar()

        #vbox.pack_start(
        #    self.toolbar, False, False, 0)
        vbox.pack_start(
            base_panel, True, True, 0)

        self.add(vbox)

        self.show_all()
        self.realize()

        #self.toolbar.connect(
        #    'salir', self.__salir)
        #self.toolbar.connect(
        #    'load', self.__load_files)

        self.connect("delete-event", self.__salir)

    '''
    def __load_files(self, widget, lista):
        """
        Agrega archivos a la lista a procesar.
        """

        items = []

        for origen in lista:
            if os.path.isdir(origen):
                for archivo in os.listdir(origen):
                    arch = os.path.join(origen, archivo)
                    datos = get_data(arch)

                    if 'audio' in datos or \
                        'video' in datos or \
                        'application/ogg' in datos or \
                        'application/octet-stream' in datos:
                        items.append([os.path.basename(arch), arch])

            elif os.path.isfile(origen):
                datos = get_data(origen)

                if 'audio' in datos or \
                    'video' in datos or \
                    'application/ogg' in datos or \
                    'application/octet-stream' in datos:
                    items.append([os.path.basename(origen), origen])

        self.lista.limpiar()

        if items:
            self.lista.agregar_items(items)
    '''

    def __salir(self, widget=None, senial=None):

        #for key in self.widgettareas.tareas.keys():
        #    widtarea = self.widgettareas.tareas[key]
        #    widtarea.stop()

        import sys
        sys.exit(0)


if __name__ == "__main__":
    Ventana()
    gtk.main()
