#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import gtk
from BasePanel import BasePanel

PATH = os.path.dirname(__file__)


class Canales(gtk.Window):

    def __init__(self, top, processor):

        gtk.Window.__init__(self)

        self.set_title("Canales")
        self.set_resizable(False)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_transient_for(top)
        self.__processor = processor
        self.__base_panel = BasePanel(self.__processor)
        self.add(self.__base_panel)
        self.show_all()

    def run(self):
        self.__base_panel.run()
