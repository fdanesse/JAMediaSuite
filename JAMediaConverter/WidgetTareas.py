#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetTareas.py por:
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

from gi.repository import Gtk
from gi.repository import GObject

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]


class WidgetTareas(Gtk.Frame):

    __gtype_name__ = 'JAMediaConverterWidgetTareas'

    __gsignals__ = {
    'copy_tarea': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.Frame.__init__(self)

        self.tareas = {}

        self.set_label("  Tareas:  ")
        self.set_border_width(5)

        self.base_box = Gtk.VBox()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.base_box)

        self.add(scroll)
        self.show_all()

    def __emit_copy_tarea(self, widget, tarea):
        """
        Extiende la tarea configurada a todos
        los archivos en la lista, siempre que estos
        sean del mismo tipo (audio o video) y si su formato
        actual lo permite (ejemplo: no se convierte mp3 a mp3).
        """

        self.emit('copy_tarea', tarea)

    def __eliminar_tarea(self, tarea):
        """
        Cuando el usuario hace click en eliminar tarea.
        """

        del(self.tareas[tarea.path])
        tarea.destroy()

    def go_tarea(self, path):
        """
        Cuando se selecciona un archivo en la lista
        crea una tarea para él.
        """

        if not self.tareas.get(path, False):
            from Converter.WidgetConverter import WidgetConverter

            self.tareas[path] = WidgetConverter(path)
            self.tareas[path].connect(
                'copy_tarea', self.__emit_copy_tarea)
            self.tareas[path].connect(
                'eliminar_tarea', self.__eliminar_tarea)
            self.base_box.pack_start(
                self.tareas[path], False, False, 0)
