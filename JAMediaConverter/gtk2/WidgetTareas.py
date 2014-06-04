#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WidgetTareas.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay
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

import gtk
import gobject

from WidgetConverter import WidgetConverter

from Globales import get_colors

gobject.threads_init()
gtk.gdk.threads_init()


class WidgetTareas(gtk.EventBox):

    #__gsignals__ = {
    #'copy_tarea': (gobject.SIGNAL_RUN_LAST,
    #    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(2)
        self.modify_bg(0, get_colors("toolbars"))

        self.base_frame = BaseFrame()

        self.add(self.base_frame)
        self.show_all()

    def go_tarea(self, path):
        """
        Cuando se selecciona un archivo en la lista
        crea una tarea para él.
        """
        self.base_frame.go_tarea(path)


class BaseFrame(gtk.Frame):

    #__gsignals__ = {
    #'copy_tarea': (gobject.SIGNAL_RUN_LAST,
    #    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gtk.Frame.__init__(self)

        self.tareas = {}

        self.set_label("  Tareas:  ")
        self.set_border_width(4)
        self.modify_bg(0, get_colors("window"))

        self.base_box = gtk.VBox()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(self.base_box)
        scroll.get_child().modify_bg(0, get_colors("window"))
        scroll.get_child().set_border_width(5)

        self.add(scroll)
        self.show_all()
    '''
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
        tarea.get_parent().remove(tarea)
        tarea.destroy()
    '''
    def go_tarea(self, path):
        """
        Cuando se selecciona un archivo en la lista
        crea una tarea para él.
        """

        if not self.tareas.get(path, False):
            self.tareas[path] = WidgetConverter(path)
            #self.tareas[path].connect(
            #    'copy_tarea', self.__emit_copy_tarea)
            #self.tareas[path].connect(
            #    'eliminar_tarea', self.__eliminar_tarea)
            self.base_box.pack_start(
                self.tareas[path], False, False, 0)
