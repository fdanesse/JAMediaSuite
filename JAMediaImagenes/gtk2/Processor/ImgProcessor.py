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
        self.__original_array = False
        self.__changed = False

    def open(self, filepath):
        """
        Se abre un nuevo archivo, el procesador se resetea.
        """
        self.__pixbuf = gtk.gdk.pixbuf_new_from_file(filepath)
        self.__original_array = self.__pixbuf.get_pixels_array()
        self.__changed = False
        self.emit("update", self.__pixbuf)
        return True

    def close_file(self):
        """
        ImgProcessor se resetea.
        """
        self.__pixbuf = False
        self.__original_array = False
        self.__changed = False
        self.emit("update", None)

    def has_changes(self):
        """
        Devuelve si hay cambios en el array visible con respecto al array del
        archivo abierto actualmente.
        """
        return self.__changed
