#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import gtk
from BasePanel import BasePanel

PATH = os.path.dirname(__file__)


class Canales(gtk.Window):

    def __init__(self, top):

        gtk.Window.__init__(self)

        self.set_title("Canales")
        #self.set_icon_from_file(os.path.join(PATH,
        #    "iconos", "JAMediaImagenes.svg"))
        self.set_resizable(True)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_transient_for(top)

        self.__base_panel = BasePanel()

        self.add(self.__base_panel)

        self.show_all()
        self.resize(640, 480)
