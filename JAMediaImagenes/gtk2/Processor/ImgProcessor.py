#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk
import numpy


class ImgProcessor(gobject.GObject):

    def __init__(self):

        gobject.GObject.__init__(self)

        self.__file_path = False
        self.__array = False
        self.__pixbuf = None
        self.__file_info = {}

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
        self.__file_info = _dict

    def __get_colors(self, array, color):
        R, G, B = color
        pixels = numpy.copy(array)
        i0 = 0
        for x in pixels:
            i1 = 0
            for i in x:
                if not R:
                    pixels[i0, i1, 0] = 0
                if not G:
                    pixels[i0, i1, 1] = 0
                if not B:
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

    def close_file(self):
        self.__file_path = False
        self.__array = False
        self.__pixbuf = None
        self.__file_info = {}

    def open(self, filepath):
        """
        Se abre un nuevo archivo, el procesador se resetea.
        """
        self.__file_path = filepath
        self.__pixbuf = gtk.gdk.pixbuf_new_from_file(filepath)
        self.__array = self.__pixbuf.get_pixels_array()
        self.__set_file_info()
        return self.__file_info

    def get_pixbuf_channles(self, widget, canales):
        if widget:
            pixbuf = self.scale_full(widget, self.__pixbuf.copy())
        else:
            pixbuf = self.__pixbuf.copy()
        array = pixbuf.get_pixels_array()
        if "Original" in canales:
            pass
        elif "Rojo" in canales or "Verde" in canales or "Azul" in canales:
            R = "Rojo" in canales
            G = "Verde" in canales
            B = "Azul" in canales
            array = self.__get_colors(array, (R, G, B))
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)

        elif "Lightness" in canales:
            array = self.__get_lightness(array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Luminosity" in canales:
            array = self.__get_luminosity(array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Average" in canales:
            array = self.__get_average(array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)
        elif "Percentual" in canales:
            array = self.__get_percentual(array)
            pixbuf = gtk.gdk.pixbuf_new_from_array(
                array, gtk.gdk.COLORSPACE_RGB, 8)

        return pixbuf

    def get_file_path(self):
        return self.__file_path

    def scale_full(self, widget, pixbuf):
        """
        Escala ocupando todo el espacio visible del widget donde debe dibujarse
        pero sin perder proporciones de la imagen.
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

    def save_png(self, path, canales):
        pixbuf = self.get_pixbuf_channles(False, canales)
        if not path.split(".")[-1] == "png":
            path = "%s%s" % (path, ".png")
        pixbuf.save(path, "png")
