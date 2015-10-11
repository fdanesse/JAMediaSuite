#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk

PATH = os.path.dirname(__file__)


class JAMediaImagenes(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("JAMediaImagenes")
        #self.set_icon_from_file(os.path.join(BASE_PATH,
        #    "Iconos", "JAMedia.svg"))
        #self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_resizable(True)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)

        self.basebox = gtk.VBox()

        self.add(self.basebox)

        self.show_all()

        self.connect("delete-event", self.__salir)
        self.resize(640, 480)

        print "JAMediaImagenes process:", os.getpid()

    def __salir(self, widget=None, senial=None):
        gtk.main_quit()
        sys.exit(0)


if __name__ == "__main__":
    JAMediaImagenes()
    gtk.main()
