#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTop.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

# https://pythonhosted.org/psutil/

import os
import sys
import threading
import gtk
import gobject

from Control.Control import Control
from Widgets import TopView


class Ventana(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("JAMediaTOP")
        #self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
        #    "Iconos", "JAMedia.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)

        socket = gtk.Socket()
        self.add(socket)

        jamediatop = JAMediaTop()
        socket.add_id(jamediatop.get_id())
        self.show_all()

        self.connect("destroy", self.__salir)

    def __salir(self, widget=None, senial=None):
        gtk.main_quit()
        sys.exit(0)


class JAMediaTop(gtk.Plug):

    def __init__(self):

        gtk.Plug.__init__(self, 0L)

        self.control = Control()
        self.topview = TopView()

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(
            gtk.POLICY_AUTOMATIC,
            gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(self.topview)

        self.add(scroll)
        self.show_all()

        _thread = threading.Thread(target=self.control.run)
        _thread.start()


if __name__=="__main__":
    Ventana()
    gtk.main()
