#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Help.py por:
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

import os
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Pango
from gi.repository import GdkPixbuf

from gi.repository import WebKit

screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()

BASEPATH = os.path.dirname(__file__)

_dict = {
    "Programar Clase 0": os.path.join(BASEPATH, "ProgramarPython", "001.html"),
    #"help instaladores": format_INSTALADORES,
    #"help deb": format_DEB,
    #"help rmp": format_RPM,
    #"help python": format_PYTHON,
    #"help sin root": format_SINROOT,
    #"help sugar": format_SUGAR,
    }


class Help(Gtk.Window):

    __gtype_name__ = 'JAMediaEditorHelp'

    def __init__(self, parent_window):

        Gtk.Window.__init__(self)

        self.parent_window = parent_window

        self.set_title("Help de JAMediaEditor")
        self.set_icon_from_file(
            os.path.join(BASEPATH, "Iconos", "einsteintux.png"))
        self.set_transient_for(self.parent_window)
        self.set_border_width(15)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        image = Gtk.Image()
        arch = os.path.join(BASEPATH, "Iconos", "einsteintux.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(arch, 100, 100)
        image.set_from_pixbuf(pixbuf)
        hbox.pack_start(image, False, False, 0)
        label = Gtk.Label(u"Sistema de Ayuda de JAMediaEditor")
        label.modify_font(Pango.FontDescription("%s %s" % ("Monospace", 12)))
        label.modify_fg(0, Gdk.Color(0, 0, 65000))
        hbox.pack_start(label, True, True, 0)
        vbox.pack_start(hbox, False, False, 0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.helpwidget = HelpWidget()
        self.vbox.pack_start(self.helpwidget, True, True, 0)
        vbox.pack_start(self.vbox, True, True, 0)

        self.resize(w / 2, h - 40)
        self.move(w - w / 2, 40)

        self.add(vbox)
        self.show_all()

    def set_help(self, texto):
        t = "Cargando . . ."
        t = "%s\n%s" % (t, "Por favor espera un momento.")
        dialogo = DialogoLoad(self, t)
        dialogo.connect("running", self.__load, texto)
        dialogo.run()

    def __load(self, dialogo, texto):
        print "Cargando Ayuda:", texto
        dialogo.destroy()
        arch = _dict.get(texto, False)
        if arch:
            if os.path.exists(arch):
                self.helpwidget.webview.open(arch)
            else:
                self.helpwidget.webview.open("")
        else:
            self.helpwidget.webview.open("")


class HelpWidget(Gtk.EventBox):

    #__gtype_name__ = 'HelpWidget'

    def __init__(self):

        Gtk.EventBox.__init__(self)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.webview = WebKit.WebView()
        self.webview.set_settings(WebKit.WebSettings())
        self.webview.set_zoom_level(0.8)
        scroll.add(self.webview)

        self.add(scroll)
        self.show_all()


class DialogoLoad(Gtk.Dialog):

    #__gtype_name__ = 'DialogoLoad'

    __gsignals__ = {
        "running": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, parent, texto):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL)

        self.set_decorated(False)
        self.set_border_width(15)

        label = Gtk.Label(texto)
        label.set_justify(Gtk.Justification.CENTER)
        label.show()
        self.vbox.pack_start(label, True, True, 5)

        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):
        GLib.timeout_add(500, self.__emit_running)

    def __emit_running(self):
        self.emit("running")
        return False
