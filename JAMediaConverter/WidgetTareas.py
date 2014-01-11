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

#import os

from gi.repository import Gtk
#from gi.repository import Gdk
from gi.repository import GObject
#from gi.repository import GLib

#from JAMediaObjects.JAMediaGlobales import get_boton
#from JAMediaObjects.JAMediaGlobales import get_separador
#from JAMediaObjects.JAMediaGlobales import get_pixels

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]


class WidgetTareas(Gtk.Frame):

    __gtype_name__ = 'JAMediaConverterWidgetTareas'

    __gsignals__ = {
    'copy_tarea': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.Frame.__init__(self)

        self.tipo = False
        self.tareas = {}

        self.set_label("  Tareas a Programadas:  ")
        self.set_border_width(5)

        self.base_box = Gtk.VBox()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.base_box)

        self.add(scroll)
        self.show_all()

    def go_tarea(self, path, tipo):
        """
        Cuando se selecciona un archivo en la lista
        crea una tarea para él o la selecciona si
        esta ya existe.
        """

        self.tipo = tipo
        tarea = self.tareas.get(path, False)

        if tarea:
            wid = self.tareas[path]

        else:
            if tipo == 'audio':
                from AudioConverter.WidgetAudioTarea import WidgetAudioTarea

                wid = WidgetAudioTarea(path)

            elif tipo == 'video':
                #wid = WidgetVideoTarea(path)
                pass

            self.tareas[path] = wid
            self.tareas[path].connect(
                'copy_tarea', self.__emit_copy_tarea)
            self.tareas[path].connect(
                'eliminar_tarea', self.__eliminar_tarea)
            self.base_box.pack_start(wid, False, False, 0)

        # FIXME: seleccionar y mostrar wid

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
