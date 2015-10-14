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
        self.__pixbuf = None

    def __get_color(self, array, color):
        print color
        pixels = numpy.copy(array)
        i0 = 0
        for x in pixels:
            i1 = 0
            for i in x:
                if "Rojo" in color:
                    pixels[i0, i1, 1] = 0
                    pixels[i0, i1, 2] = 0
                elif "Verde" in color:
                    pixels[i0, i1, 0] = 0
                    pixels[i0, i1, 2] = 0
                elif "Azul" in color:
                    pixels[i0, i1, 0] = 0
                    pixels[i0, i1, 1] = 0
                elif "Cian" in color:
                    pixels[i0, i1, 0] = 0
                elif "Magenta" in color:
                    pixels[i0, i1, 1] = 0
                elif "Amarillo" in color:
                    pixels[i0, i1, 2] = 0
                i1 += 1
            i0 += 1
        return pixels

    def __get_lightness(self, array):
        """
        The graylevel will be calculated as Lightness = 1/2 × (max(R,G,B) + min(R,G,B))
        """
        pixels = numpy.copy(array)
        i0 = 0
        for x in pixels:
            i1 = 0
            for i in x:
                ma = pixels[i0, i1, numpy.argmax(pixels[i0, i1])]
                mi = pixels[i0, i1, numpy.argmin(pixels[i0, i1])]
                lightness = 1.0 / 2.0 * (float(ma) + float(mi))
                if lightness < 0:
                    lightness = 0
                elif lightness > 255:
                    lightness = 255
                pixels[i0, i1, 0] = int(lightness)
                pixels[i0, i1, 1] = int(lightness)
                pixels[i0, i1, 2] = int(lightness)
                i1 += 1
            i0 += 1
        return pixels

    def __get_luminosity(self, array):
        """
        The graylevel will be calculated as Luminosity = 0.21 × R + 0.72 × G + 0.07 × B
        """
        pixels = numpy.copy(array)
        i0 = 0
        for x in pixels:
            i1 = 0
            for i in x:
                #R = 0.2126
                #G = 0.7152
                #B = 0.0722
                luminosity = 0.21 * pixels[i0, i1, 0] + 0.72 * \
                    pixels[i0, i1, 1] + 0.07 * pixels[i0, i1, 2]
                if luminosity < 0:
                    luminosity = 0
                elif luminosity > 255:
                    luminosity = 255
                pixels[i0, i1, 0] = int(luminosity)
                pixels[i0, i1, 1] = int(luminosity)
                pixels[i0, i1, 2] = int(luminosity)
                i1 += 1
            i0 += 1
        return pixels

    def __get_average(self, array):
        """
        The graylevel will be calculated as Average Brightness = (R + G + B) / 3
        """
        pixels = numpy.copy(array)
        i0 = 0
        for x in pixels:
            i1 = 0
            for i in x:
                average = numpy.mean(pixels[i0, i1])
                pixels[i0, i1, 0] = int(average)
                pixels[i0, i1, 1] = int(average)
                pixels[i0, i1, 2] = int(average)
                i1 += 1
            i0 += 1
        return pixels

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
        self.__pixbuf = gtk.gdk.pixbuf_new_from_file(filepath)
        self.__array = self.__pixbuf.get_pixels_array()
        self.emit("update", self.__pixbuf)

    def get_pixbuf(self, widget, text):
        pixbuf = self.scale_full(widget, self.__pixbuf)
        array = pixbuf.get_pixels_array()
        if "Original" in text:
            pass
        elif "Rojo" in text or "Verde" in text or "Azul" in text or "Cian" in text or "Magenta" in text or "Amarillo" in text:
            array = self.__get_color(array, text)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Lightness" in text:
            array = self.__get_lightness(array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Luminosity" in text:
            array = self.__get_luminosity(array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Average" in text:
            array = self.__get_average(array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Percentual" in text:
            array = self.__get_percentual(array)
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
