#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk


class ImgProcessor(gobject.GObject):

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gobject.GObject.__init__(self)

        self.__file_path = False
        self.__file_info = {}
        self.__pixbuf = None
        self.__original_array = False
        self.__changed = False

    def __set_file_info(self):
        """
        ({'is_writable': True,
            'extensions': ['jpeg', 'jpe', 'jpg'],
            'mime_types': ['image/jpeg'], 'name':
            'jpeg', 'description': 'JPEG'}, 275, 183)
        """
        info = gtk.gdk.pixbuf_get_file_info(self.__file_path)
        _dict = info[0]
        _dict["size"] = (info[1], info[2])
        _dict["path"] = self.__file_path
        _dict["mb"] = os.path.getsize(self.__file_path)
        return _dict

    def open(self, filepath):
        """
        Se abre un nuevo archivo, el procesador se resetea.
        """
        self.__file_path = filepath
        self.__file_info = self.__set_file_info()
        self.__pixbuf = gtk.gdk.pixbuf_new_from_file(filepath)
        self.__original_array = self.__pixbuf.get_pixels_array()
        self.__changed = False
        self.emit("update", self.__pixbuf, self.__file_info)
        return True

    def close_file(self):
        """
        ImgProcessor se resetea.
        """
        self.__file_path = False
        self.__file_info = {}
        self.__pixbuf = None
        self.__original_array = False
        self.__changed = False
        self.emit("update", self.__pixbuf, self.__file_info)

    def has_changes(self):
        """
        Devuelve si hay cambios en el array visible con respecto al array del
        archivo abierto actualmente.
        """
        return self.__changed

    def get_file_path(self):
        return self.__file_path
