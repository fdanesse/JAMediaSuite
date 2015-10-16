#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject

BASE_PATH = os.path.dirname(__file__)


class ToolbarPrincipal(gtk.Toolbar):

    def __init__(self):

        gtk.Toolbar.__init__(self)

        """
        abrir
        guardar
        guardar como
        zoom-in
        zoom-out
        original resolution
        fullwidget
        rotar izquierda
        rotar derecha
        anterior
        siguiente
        """
        self.show_all()
