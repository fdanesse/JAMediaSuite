#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ScrollPage.py por:
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

from gi.repository import Gtk
from gi.repository import GtkSource


class ScrollPage(Gtk.ScrolledWindow):

    __gtype_name__ = 'JAMediaEditorScrollPage'

    def __init__(self, file_path, lenguaje, texto):

        Gtk.ScrolledWindow.__init__(self)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.add(SourceView(file_path, lenguaje, texto))
        self.show_all()


class SourceView(GtkSource.View):

    def __init__(self, file_path, lenguaje, texto):

        GtkSource.View.__init__(self)

        self.file_path = file_path
        manager = GtkSource.LanguageManager()
        self.set_buffer(GtkSource.Buffer())
        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)
        #self.set_auto_indent(True)
        #self.set_smart_home_end(True)
        self.set_highlight_current_line(True)
        self.get_buffer().set_highlight_syntax(True)
        self.get_buffer().set_language(manager.get_language(lenguaje))
        self.get_buffer().set_text(texto)
        self.show_all()

    def guardar(self):
        _buffer = self.get_buffer()
        inicio, fin = _buffer.get_bounds()
        texto = _buffer.get_text(inicio, fin, 0)
        arch = open(self.file_path, "w")
        arch.write(texto)
        arch.close()
