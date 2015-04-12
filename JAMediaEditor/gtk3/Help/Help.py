#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Help.py por:
#   Flavio Danesse <fdanesse@gmail.com>

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
    "bash Clase 0": os.path.join(BASEPATH, "bash", "000.html"),
    "Programar Clase 0": os.path.join(BASEPATH, "ProgramarPython", "000.html"),
    "help instaladores": os.path.join(BASEPATH, "JAMediaEditor", "Instaladores.html"),
    "help deb": os.path.join(BASEPATH, "JAMediaEditor", "InstaladorDEB.html"),
    #"help rmp": format_RPM,
    "help python": os.path.join(BASEPATH, "JAMediaEditor", "InstaladorPYTHON.html"),
    "help sin root": os.path.join(BASEPATH, "JAMediaEditor", "InstaladorSINROOT.html"),
    "help sugar": os.path.join(BASEPATH, "JAMediaEditor", "InstaladorSUGAR.html"),
    }


def get_separador(draw=False, ancho=0, expand=False):
    separador = Gtk.SeparatorToolItem()
    separador.props.draw = draw
    separador.set_size_request(ancho, -1)
    separador.set_expand(expand)
    return separador


def get_boton(archivo, flip=False, rotacion=None,
    pixels=0, tooltip_text=None):
    if not pixels:
        pixels = 37
    boton = Gtk.ToolButton()
    imagen = Gtk.Image()
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, pixels, pixels)
    if flip:
        pixbuf = pixbuf.flip(True)
    if rotacion:
        pixbuf = pixbuf.rotate_simple(rotacion)
    imagen.set_from_pixbuf(pixbuf)
    boton.set_icon_widget(imagen)
    imagen.show()
    boton.show()
    if tooltip_text:
        boton.set_tooltip_text(tooltip_text)
        boton.TOOLTIP = tooltip_text
    return boton


class Help(Gtk.Window):

    __gtype_name__ = 'JAMediaEditorHelp'

    def __init__(self, parent_window, titulo):

        Gtk.Window.__init__(self)

        self.parent_window = parent_window

        self.set_title("Help de JAMediaEditor")
        self.set_icon_from_file(
            os.path.join(BASEPATH, "Iconos", "einsteintux.png"))
        self.set_transient_for(self.parent_window)
        self.set_border_width(15)

        self.toolbar = Toolbar(titulo)
        self.helpwidget = HelpWidget()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(self.helpwidget, True, True, 0)

        self.resize(w / 2, h - 40)
        self.move(w - w / 2, 40)

        self.add(vbox)
        self.show_all()

        self.toolbar.connect("zoom", self.helpwidget.zoom)

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


class Toolbar(Gtk.EventBox):

    __gtype_name__ = 'HelpToolbar'

    __gsignals__ = {
    "zoom": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self, titulo):

        Gtk.EventBox.__init__(self)

        toolbar = Gtk.Toolbar()
        toolbar.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse('#edf5ff'))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)
        #toolbar.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse('#ffffff'))

        image = Gtk.Image()
        arch = os.path.join(BASEPATH, "Iconos", "einsteintux.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(arch, 100, 100)
        image.set_from_pixbuf(pixbuf)
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(image)
        toolbar.insert(item, -1)

        label = Gtk.Label(titulo)
        label.modify_font(Pango.FontDescription("%s %s" % ("Monospace", 12)))
        label.modify_fg(0, Gdk.Color(0, 0, 65000))
        item = Gtk.ToolItem()
        item.set_expand(True)
        item.add(label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASEPATH, "Iconos", "Zoomout.svg")
        boton = get_boton(archivo, flip=False, pixels=18,
            tooltip_text="Alejar")
        boton.connect("clicked", self.__emit_zoom)
        toolbar.insert(boton, -1)

        archivo = os.path.join(BASEPATH, "Iconos", "Zoomin.svg")
        boton = get_boton(archivo, flip=False, pixels=18,
            tooltip_text="Acercar")
        boton.connect("clicked", self.__emit_zoom)
        toolbar.insert(boton, -1)

        self.add(toolbar)
        self.show_all()

    def __emit_zoom(self, widget):
        self.emit('zoom', widget.TOOLTIP)


class HelpWidget(Gtk.ScrolledWindow):

    #__gtype_name__ = 'HelpWidget'

    def __init__(self):

        Gtk.ScrolledWindow.__init__(self)

        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.webview = WebKit.WebView()
        self.webview.set_settings(WebKit.WebSettings())
        self.webview.set_zoom_level(0.8)
        self.add(self.webview)
        self.show_all()

    def zoom(self, widget, zoom):
        x = float("{:.2f}".format(self.webview.get_zoom_level()))
        if zoom == "Alejar":
            x -= 0.1
            if x < 0.3:
                x = 0.3
        elif zoom == "Acercar":
            x += 0.1
            if x > 3.0:
                x = 3.0
        self.webview.set_zoom_level(x)


class DialogoLoad(Gtk.Dialog):

    __gtype_name__ = 'HelpDialogoLoad'

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
