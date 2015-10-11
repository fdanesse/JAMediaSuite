#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import gtk


class ImgProcessor(gobject.GObject):

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gobject.GObject.__init__(self)

        self.__pixbuf = False
        self.__array = False

    def open(self, filepath):
        self.__pixbuf = gtk.gdk.pixbuf_new_from_file(filepath)
        self.__array = self.__pixbuf.get_pixels_array()
        self.emit("update", self.__pixbuf)
