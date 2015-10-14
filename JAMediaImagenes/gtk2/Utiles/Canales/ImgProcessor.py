#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk
import numpy


class ImgProcessor(gobject.GObject):

    __gsignals__ = {
    "update": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self):

        gobject.GObject.__init__(self)

        self.__file_path = False
        self.__array = False

    def __get_percentual(self, array):
        """
        The graylevel will be calculated as Percentual = R * 0.3 + G * 0.59 + B * 0.11
        """
        pixels = numpy.copy(array)
        i0 = 0
        for x in pixels:
            i1 = 0
            for i in x:
                percentual = float(pixels[i0, i1, 0]) * 0.3 + float(
                    pixels[i0, i1, 1]) * 0.59 + float(pixels[i0, i1, 2]) * 0.11
                if percentual < 0:
                    percentual = 0
                elif percentual > 255:
                    percentual = 255
                pixels[i0, i1, 0] = int(percentual)
                pixels[i0, i1, 1] = int(percentual)
                pixels[i0, i1, 2] = int(percentual)
                i1 += 1
            i0 += 1
        return pixels

    def open(self, filepath):
        """
        Se abre un nuevo archivo, el procesador se resetea.
        """
        self.__file_path = filepath
        pixbuf = gtk.gdk.pixbuf_new_from_file(filepath)
        self.__array = pixbuf.get_pixels_array()
        self.emit("update", pixbuf)

    def get_pixbuf(self, text):
        pixbuf = None
        if "Original" in text:
            array = numpy.copy(self.__array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Rojo" in text:
            pass
        elif "Verde" in text:
            pass
        elif "Azul" in text:
            pass
        elif "Lightness" in text:
            pass
        elif "Luminosity" in text:
            pass
        elif "Average" in text:
            pass
        elif "Percentual" in text:
            array = self.__get_percentual(self.__array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        return pixbuf

    def scale_full(self, widget, pixbuf):
        """
        Escala ocupando todo el espacio visible del widget donde debe dibujarse
        """
        rect = widget.get_allocation()
        src_width, src_height = pixbuf.get_width(), pixbuf.get_height()
        scale = min(float(rect.width) / src_width,
            float(rect.height) / src_height)
        new_width = int(scale * src_width)
        new_height = int(scale * src_height)
        pixbuf = pixbuf.scale_simple(new_width,
            new_height, gtk.gdk.INTERP_BILINEAR)
        return pixbuf
