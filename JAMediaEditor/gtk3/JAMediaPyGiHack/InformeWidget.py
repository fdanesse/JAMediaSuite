#!/usr/bin/env python
# -*- coding: utf-8 -*-

# InformeWidget.py por:
#     Flavio Danesse     <fdanesse@gmail.com>

# This program is free software; you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110 - 1301 USA

import os
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GdkX11
from gi.repository import GtkSource

screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()


class InformeWidget(Gtk.Window):

    __gtype_name__ = 'JAMediaEditorInformeWidget'

    def __init__(self, parent_window=None):

        Gtk.Window.__init__(self)

        self.parent_window = parent_window
        self.set_title("Informe de Introspección")
        self.set_transient_for(self.parent_window)
        self.set_border_width(5)

        self.source = GtkSource.View()
        self.source.set_insert_spaces_instead_of_tabs(True)
        self.source.set_tab_width(4)
        self.source.set_auto_indent(True)
        self.source.set_highlight_current_line(True)
        self.source.set_editable(False)
        self.source.set_border_width(5)
        self.source.set_buffer(GtkSource.Buffer())

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.source)

        self.resize(w / 3, h - 40)
        self.move(w - w / 3, 40)

        #text = ""
        #_dict = self.infonotebook.introspeccion._dict
        #for key in _dict:
        #    text = "%s\n%s" % (text, _dict[key])
        #source.get_buffer().set_text(text)

        self.add(scroll)
        self.show_all()

    def setting(self, text):
        self.source.get_buffer().set_text(text)
        self.show_all()
