#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaGstreamer.py por:
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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

from Widgets import TextView
from Widgets import Lista


def get_inspect(elemento):
    import commands
    return commands.getoutput('gst-inspect-1.0 %s' % (elemento))


class JAMediaGstreamer(Gtk.Paned):

    __gtype_name__ = 'JAMediaGstreamerPyGiHack'

    def __init__(self):

        Gtk.Paned.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)

        # Izquierda
        self.lista = Lista()
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.lista)
        scroll.set_size_request(250, -1)
        self.pack1(scroll, resize = False, shrink = False)

        # Derecha
        self.textview = TextView()
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.textview)
        self.pack2(scroll, resize = True, shrink = True)

        self.show_all()
        self.__llenar_lista()
        self.lista.connect('nueva-seleccion', self.__get_element)

    def __llenar_lista(self):
        try:
            import gi
            gi.require_version('Gst', '1.0')
            from gi.repository import Gst

            Gst.init([])
            registry = Gst.Registry.get()
            plugins = registry.get_plugin_list()

        except:
            return

        _iter = self.lista.get_model().get_iter_first()

        for elemento in plugins:
            iteractual = self.lista.get_model().append(
                _iter, [elemento.get_name(), elemento.get_description()])

            features = registry.get_feature_list_by_plugin(elemento.get_name())
            if len(features) > 1:
                for feature in features:
                    self.lista.get_model().append(iteractual,
                        [feature.get_name(), elemento.get_description()])

    def __get_element(self, widget, path):
        self.textview.get_buffer().set_text(get_inspect(path))


def exit(self, widget=None, senial=None):
    import sys
    sys.exit(0)


if __name__ == "__main__":
    ventana = Gtk.Window()
    ventana.add(JAMediaGstreamer())
    ventana.connect("delete-event", exit)
    ventana.show_all()
    ventana.set_resizable(True)
    ventana.set_size_request(640, 480)
    ventana.set_border_width(2)
    ventana.set_position(Gtk.WindowPosition.CENTER)
    Gtk.main()
