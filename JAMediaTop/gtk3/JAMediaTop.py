#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTop.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

# https://code.google.com/p/psutil/wiki/Documentation
# https://code.google.com/p/psutil/
# https://github.com/nicolargo/glances
# https://github.com/elventear/psutil

# http://linux.die.net/man/2/ioprio_get

import os
import sys

import gi
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GLib

CABECERA_FILEs_OPEN_by_PROCESS = [
    'COMMAND', 'PID', 'USER', 'FD',
    'TYPE', 'DEVICE', 'SIZE/OFF',
    'NODE', 'NAME'] [2:]# la primer linea de: cmd = "lsof -a -p %s" % pid

from Widgets import TopView

import JAMediaSystemState as JAMSS


class Ventana(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("JAMediaTOP")
        #self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
        #    "Iconos", "JAMedia.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        socket = Gtk.Socket()
        self.add(socket)

        jamediatop = JAMediaTop()
        socket.add_id(jamediatop.get_id())
        self.show_all()
        self.realize()

        self.connect("destroy", self.__salir)

    def __salir(self, widget=None, senial=None):
        sys.exit(0)


class JAMediaTop(Gtk.Plug):

    def __init__(self):

        Gtk.Plug.__init__(self, 0L)

        self.topview = TopView()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.topview)

        self.add(scroll)
        self.show_all()

        self.actualizador = False
        self.__new_handle(True)

    def __new_handle(self, reset):
        """
        Elimina o reinicia el actualizador.
        """
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
        if reset:
            self.actualizador = GLib.timeout_add(1000, self.__update_topview)

    def __update_topview(self):
        pids_procesos = JAMSS.get_pids()
        lista = []
        for pid in pids_procesos:
            nombre = JAMSS.get_process_name(pid)
            com = JAMSS.get_process_cmdline(pid)

            comandos = ''
            for c in com:
                comandos += "%s " % c

            comandos = comandos.strip()
            #hijos = JAMSS.get_process_threads(pid)
            lista.append([pid, nombre, comandos])
            #JAMSS.get_archivos_abiertos_por_proceso(pid)

        self.topview.set_tree(lista)
        return True


if __name__=="__main__":
    Ventana()
    Gtk.main()
