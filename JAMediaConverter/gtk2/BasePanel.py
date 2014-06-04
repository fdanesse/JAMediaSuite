#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BasePanel.py por:
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

from WidgetTareas import WidgetTareas
from JAMedia.PlayerList import PlayerList

from Globales import get_colors

BASEPATH = os.path.dirname(__file__)

gobject.threads_init()
gtk.gdk.threads_init()


class BasePanel(gtk.HPaned):

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.playerlist = PlayerList()
        self.playerlist.set_mime_types(["audio/*", "video/*"])
        self.widgettareas = WidgetTareas()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(self.playerlist)
        scroll.get_child().modify_bg(0, get_colors("toolbars"))
        event = gtk.EventBox()
        event.modify_bg(0, get_colors("toolbars"))
        event.add(scroll)
        event.set_size_request(200, -1)

        self.pack1(event, resize=False, shrink=True)
        self.pack2(self.widgettareas, resize=True, shrink=True)

        self.show_all()

        self.playerlist.connect(
            "accion", self.__re_emit_accion_list)
        self.playerlist.connect(
            "nueva-seleccion", self.__selecction_file)
        #self.widgettareas.connect(
        #    'copy_tarea', self.__copy_tarea)

    def __re_emit_accion_list(self, widget, lista, accion, _iter):
        print accion, _iter
    #    self.emit("accion-list", lista, accion, _iter)

    def __selecction_file(self, widget, path):
        self.widgettareas.go_tarea(path)

    '''
    def __copy_tarea(self, widget, tarea):
        """
        Extiende la tarea configurada a todos
        los archivos en la lista, siempre que estos
        sean del mismo tipo (audio o video) y si su formato
        actual lo permite (ejemplo: no se convierte mp3 a mp3).
        """

        model = self.lista.get_model()
        item = model.get_iter_first()

        it = None

        while item:
            it = item
            item = model.iter_next(item)

            if it:
                path = model.get_value(it, 2)
                widtarea = self.widgettareas.tareas.get(path, False)

                if not widtarea:
                    self.widgettareas.go_tarea(path)

        for key in self.widgettareas.tareas.keys():
            widtarea = self.widgettareas.tareas[key]

            if not widtarea.estado:
                widtarea.setear(tarea)
    '''
