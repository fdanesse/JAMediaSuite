#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay

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
from gi.repository import GObject

from Widgets import Toolbar
from BaseBox import BaseBox

BASE_PATH = os.path.dirname(__file__)


class JAMediaPyGiHack(Gtk.Box):

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.toolbar = Toolbar()
        self.pack_start(self.toolbar, False, False, 0)

        self.basebox = BaseBox()
        self.pack_start(self.basebox, True, True, 0)

        self.show_all()

        self.toolbar.connect("import", self.__import)
        self.toolbar.connect("accion-menu", self.__set_accion)
        self.toolbar.connect("salir", self.__emit_salir)

        self.toolbar.connect("buscar", self.__buscar)
        self.toolbar.connect("accion", self.__buscar_mas)
        self.toolbar.connect("informe", self.__informar)

        self.basebox.connect("update", self.__update)
        self.basebox.connect("nobusquedas", self.__desactivar_busquedas)

    def __informar(self, widget):
        """
        Abre nueva lengueta en Workpanel con la información de Introspección
        del archivo seleccionado.
        """
        # FIXME: Continuar Desarrollo de esta funcionalidad
        #text = ""
        #_dict = self.infonotebook.introspeccion._dict
        #for key in _dict:
        #    text = "%s\n%s" % (text, _dict[key])
        #source = GtkSource.View()
        #source.set_insert_spaces_instead_of_tabs(True)
        #source.set_tab_width(4)
        #source.set_auto_indent(True)
        #source.set_highlight_current_line(True)
        #source.set_editable(False)
        #source.set_border_width(5)
        #source.set_buffer(GtkSource.Buffer())
        #win = Gtk.Window()
        #win.set_transient_for(self.get_toplevel())
        #win.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#f0e6aa"))
        #win.set_title("Informe de Introspección")
        #win.set_border_width(5)
        #win.set_position(Gtk.WindowPosition.CENTER)
        #win.set_size_request(400, 400)
        #scroll = Gtk.ScrolledWindow()
        #scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        #scroll.add(source)
        #source.get_buffer().set_text(text)
        #win.add(scroll)
        #win.show_all()
        print self.__informar

    def __buscar(self, widget, text):
        self.basebox.buscar(text)

    def __buscar_mas(self, widget, accion, text):
        self.basebox.buscar_mas(accion, text)

    def __emit_salir(self, widget):
        self.emit('salir')

    def __update(self, widget, view):
        self.toolbar.update(view)
        self.toolbar.activar_busquedas(self.basebox.check_busquedas())

    def __desactivar_busquedas(self, widget):
        self.toolbar.activar_busquedas(False)

    def __set_accion(self, widget, menu, wid_lab, valor):
        self.basebox.set_accion(menu, wid_lab, valor)

    def __import(self, widget, paquete, modulo):
        self.basebox.import_modulo(paquete, modulo)


class Ventana(Gtk.Window):

    __gtype_name__ = 'VentanaJAMediaPyGiHack'

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("JAMediaPygiHack")

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.maximize()
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        jamediapygihack = JAMediaPyGiHack()
        self.add(jamediapygihack)

        self.show_all()
        self.realize()

        jamediapygihack.connect("salir", self.__salir)
        self.connect("delete-event", self.__salir)

    def __salir(self, widget=None, senial=None):
        import sys
        sys.exit(0)


if __name__ == "__main__":
    Ventana()
    Gtk.main()
