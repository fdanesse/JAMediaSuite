#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Es un simple Lanzador de:
        JAMediaObjects.JAMediaGstreamer.JAMediaVideoEfectos.Ventana()
"""

import os
import sys

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaGstreamer.JAMediaVideoEfectos import Ventana


class Run(Ventana):
    
    def __init__(self):
        
        Ventana.__init__(self)
        
        self.show_all()

if __name__ == "__main__":
    
    Run()
    Gtk.main()
    