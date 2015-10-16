#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gobject
import gtk
import numpy


def calc_luminosity(pixel):
    """
    The graylevel will be calculated as
        Luminosity = 0.21 × R + 0.72 × G + 0.07 × B
    R = 0.2126
    G = 0.7152
    B = 0.0722
    """
    luminosity = int(0.21 * float(pixel[0]) + 0.72 * float(
        pixel[1]) + 0.07 * float(pixel[2]))
    pixel[:] = luminosity


def calc_percentual(pixel):
    """
    The graylevel will be calculated as
        Percentual = R * 0.3 + G * 0.59 + B * 0.11
    """
    percentual = int(float(pixel[0]) * 0.3 + float(
        pixel[1]) * 0.59 + float(pixel[2]) * 0.11)
    pixel[:] = percentual


def calc_average(pixel):
    """
    The graylevel will be calculated as Average Brightness = (R + G + B) / 3
    """
    average = numpy.mean(pixel)
    pixel[:] = int(average)


def calc_lightness(pixel):
    """
    The graylevel will be calculated as
        Lightness = 1/2 × (max(R,G,B) + min(R,G,B))
    La luminosidad se define como el promedio entre el mayor y el menor
    componente de color RGB. Esta definición pone los colores primarios y
    secundarios en un plano que pasa a mitad de camino entre el blanco y
    el negro.
    https://es.wikipedia.org/wiki/Modelo_de_color_HSL
    """
    #numpy.argmax([pixel[0], pixel[1], pixel[2]])
    ma = max([pixel[0], pixel[1], pixel[2]])
    #numpy.argmin([pixel[0], pixel[1], pixel[2]])
    mi = min([pixel[0], pixel[1], pixel[2]])
    lightness = int(1.0 / 2.0 * (float(ma) + float(mi)))
    pixel[:] = int(lightness)


def map_luminosity(pixels):
    map(calc_luminosity, pixels[:])


def map_percentual(pixels):
    map(calc_percentual, pixels[:])


def map_average(pixels):
    map(calc_average, pixels[:])


def map_lightness(pixels):
    map(calc_lightness, pixels[:])


#Escalar = pixels = pixels[::2,::2,:] (Recortar con pasos)
#Recortar = pixels = pixels[50:-50, 200:, :]


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
        if not R:
            pixels[:, :, 0] = 0
        if not G:
            pixels[:, :, 1] = 0
        if not B:
            pixels[:, :, 2] = 0
        return pixels

    def __get_lightness(self, array):
        pixels = numpy.copy(array)
        map(map_lightness, pixels)
        return pixels

    def __get_luminosity(self, array):
        pixels = numpy.copy(array)
        map(map_luminosity, pixels)
        return pixels

    def __get_average(self, array):
        pixels = numpy.copy(array)
        map(map_average, pixels)
        return pixels

    def __get_percentual(self, array):
        pixels = numpy.copy(array)
        map(map_percentual, pixels)
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
        if not self.__pixbuf:
            return None
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
