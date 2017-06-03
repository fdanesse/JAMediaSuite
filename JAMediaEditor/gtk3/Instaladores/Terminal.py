#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Terminal.py por:
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
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Vte
from gi.repository import Pango

BASE_PATH = os.path.dirname(__file__)
Width_Button = 18


class Terminal(Gtk.EventBox):
    """
    Terminal (NoteBook + Vtes) + Toolbar.
    """

    __gtype_name__ = 'TerminalInstalador'

    __gsignals__ = {
    "reset": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        self.set_border_width(5)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.terminal = VTETerminal()
        scroll.add(self.terminal)

        self.add(scroll)
        self.show_all()

        self.terminal.connect("reset", self.__re_emit_reset)

    def reset(self):
        self.terminal.reset()

    def ejecute_script(self, dirpath, interprete, path_script, param):
        self.terminal.ejecute_script(dirpath, interprete, path_script, param)

    def __re_emit_reset(self, terminal):
        self.emit("reset")


class VTETerminal(Vte.Terminal):
    """
    Terminal Configurable en distintos intérpretes.
    """

    __gsignals__ = {
    "reset": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Vte.Terminal.__init__(self)

        self.set_sensitive(False)
        self.set_encoding('utf-8')
        self.set_font(Pango.FontDescription("Monospace %s" % 10))

        # FIXME: TypeError: argument foreground: Expected Gdk.RGBA, but got gi.overrides.Gdk.Color
        #self.set_colors(Gdk.color_parse('#ffffff'),
        #    Gdk.color_parse('#000000'), [])

        self.show_all()
        self.reset()

    def reset(self, path=os.environ["HOME"], interprete="/bin/bash"):
        pty_flags = Vte.PtyFlags(0)
        try:
            self.fork_command_full(pty_flags, path,
                (interprete,), "", 0, None, None)
        except:
            self.spawn_sync(pty_flags, path,
                (interprete,), "", 0, None, None)
        self.child_focus(True)

    def do_child_exited(self, ret=0):
        """
        Cuando se hace exit en la terminal, esta se resetea.
        FIXME: ret es un parámetro nuevo de VTE.
        """
        self.emit("reset")

    def ejecute_script(self, dirpath, interprete, path_script, param):
        """
        Ejecuta un script con parámetros, en la terminal activa
        Por ejemplo:
            python setup.py sdist

            dirpath     =   directorio base donde se encuentra setup.py
            interprete  =   python en este caso
            path_script =   dirpath + 'setup.py'
            param       =   'sdist' en est caso
        """
        pty_flags = Vte.PtyFlags(0)
        try:
            self.fork_command_full(pty_flags, dirpath,
                (interprete, path_script, param), "", 0, None, None)
        except:
            self.spawn_sync(pty_flags, dirpath,
                (interprete, path_script, param), "", 0, None, None)
