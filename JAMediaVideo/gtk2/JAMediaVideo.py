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
import gc
import gtk
import gobject

gc.enable()

from Globales import get_colors
from Globales import describe_archivo

from Toolbars import Toolbar
from JAMedia.Toolbars import ToolbarSalir
from JAMedia.Toolbars import ToolbarAccion
from BasePanel import BasePanel

#FIXME: Agregar en setup.py: python-gst0.10 gstreamer0.10-plugins-base gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly gstreamer0.10-plugins-bad gstreamer0.10-tools python-gst0.10-rtsp

BASE_PATH = os.path.dirname(__file__)

gobject.threads_init()
#gtk.gdk.threads_init()


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

        self.pistas = []

        vbox = gtk.VBox()
        self.add(vbox)
        self.show_all()

        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.toolbar_accion = ToolbarAccion()
        self.base_panel = BasePanel()

        vbox.pack_start(self.toolbar, False, True, 4)
        vbox.pack_start(self.toolbar_salir, False, True, 4)
        vbox.pack_start(self.toolbar_accion, False, True, 4)
        vbox.pack_start(self.base_panel, True, True, 0)

        self.toolbar.connect("accion", self.__set_accion)
        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar.connect("config-show", self.__config_show)
        self.toolbar.connect("mode-change", self.__mode_change)

        self.toolbar_salir.connect('salir', self.__salir)
        self.base_panel.connect("accion-list", self.__accion_list)
        self.base_panel.connect("in-run", self.__jamediaconvert_in_run)
        self.base_panel.connect("pendientes", self.__jamediaconvert_info)
        self.base_panel.connect("cancel-toolbars", self.__cancel_toolbars)

        self.toolbar_accion.connect("aviso", self.__update_accions)

        self.connect("delete-event", self.__salir)

        self.show_all()
        self.realize()

        gobject.idle_add(self.__run)
        print "JAMediaVideo process:", os.getpid()

    def __jamediaconvert_info(self, widget, info):
        self.toolbar.toolbar_converter.set_info(info)

    def __update_accions(self, toolbaraccion, accion, uri):
        """
        Cuando se confirma una accion desde toolbar_accion, se
        acualiza la interfaz ya que puede que ese archivo ya no esté allí.
        """
        self.base_panel.update_accions(accion, uri)

    def __jamediaconvert_in_run(self, widget, valor):
        self.toolbar.activate_conversor(valor)

    def __accion_list(self, widget, lista, accion, _iter):
        self.__cancel_toolbars()
        acciones = ["Copiar", "Quitar", "Borrar", "Mover"]

        if accion in acciones:
            self.toolbar_accion.set_accion(lista, accion, _iter)

        elif accion == "Editar":
            text = lista.get_model().get_value(_iter, 1)
            uri = lista.get_model().get_value(_iter, 2)
            self.toolbar.switch("Convert")
            converter = self.base_panel.jamediaconvert
            converter.playerlist.lista.agregar_items([(text, uri)])

        elif accion == "limpiar":
            pass

        else:
            print "Accion en la lista sin definir:", accion

    def __set_accion(self, widget, modo, accion):
        """
        Acciones de la toolbar que se aplican sobre Base Panel.
        """
        self.__cancel_toolbars()
        if accion == "Salir":
            self.toolbar.switch("menu")

        else:
            self.base_panel.set_accion(modo, accion)

    def __config_show(self, toolbar, tipo):
        self.__cancel_toolbars()
        self.base_panel.config_show(tipo)

    def __mode_change(self, widget, tipo):
        self.__cancel_toolbars()
        self.base_panel.mode_change(tipo)

    def __run(self):
        self.__cancel_toolbars()
        self.base_panel.pack_efectos()
        if self.pistas:
            if self.pistas[0] == "jamedia":
                self.toolbar.switch("Reproducir")
                lista = self.base_panel.playerlist.lista
                gobject.idle_add(lista.agregar_items, [self.pistas[1]])
            elif self.pistas[0] == "jamediaimagenes":
                self.toolbar.switch("Ver")
                lista = self.base_panel.playerlist.lista
                gobject.idle_add(lista.agregar_items, [self.pistas[1]])
        else:
            self.toolbar.switch("menu")
        self.pistas = []
        return False

    def __confirmar_salir(self, widget=None, senial=None):
        self.__cancel_toolbars()
        self.toolbar_salir.run("JAMediaVideo")

    def __cancel_toolbars(self, widget=False):
        self.toolbar_accion.cancelar()
        self.toolbar_salir.cancelar()

    def __salir(self, widget=None, senial=None):
        self.base_panel.salir()
        gtk.main_quit()
        sys.exit(0)

    def set_pistas(self, pistas):
        self.pistas = pistas


def get_item_list(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            texto = os.path.basename(file_path)
            datos = describe_archivo(file_path)
            if 'audio' in datos or 'video' in datos or \
                'application/ogg' in datos or \
                'application/octet-stream' in datos:
                return ["jamedia", [texto, file_path]]
            elif "image" in datos:
                return ["jamediaimagenes", [texto, file_path]]
    return False


if __name__ == "__main__":
    jamediavideo = JAMediaVideo()
    if len(sys.argv) > 1:
        lista = get_item_list(sys.argv[1])
        if lista:
            jamediavideo.set_pistas(lista)
            print lista
    gtk.main()
