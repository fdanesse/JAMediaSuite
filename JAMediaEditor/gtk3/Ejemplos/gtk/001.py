#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk

class Ventana(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)
        self.show_all()

Ventana()
gtk.main()
