#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject


class BasePanel(gtk.Table):

    def __init__(self, processor):

        gtk.Table.__init__(self, columns=4, rows=5, homogeneous=True)

        self.set_border_width(2)

        self.__processor = processor

        self.__visor_imagen = gtk.Image()
        self.__visor_imagen.set_size_request(320, 240)
        self.__canales = ContenedorCanales(" Colores: ")
        self.__primarios = ContenedorCanales(" Primarios: ")
        self.__grises = ContenedorCanales(" Grises: ")

        self.attach_defaults(self.__visor_imagen, 0, 4, 0, 2)
        self.attach_defaults(self.__canales, 0, 4, 2, 3)
        self.attach_defaults(self.__primarios, 0, 4, 3, 4)
        self.attach_defaults(self.__grises, 0, 4, 4, 5)

        self.show_all()

    def set_file(self, filepath):
        self.__processor.open(filepath)
        pixbuf = self.__processor.get_pixbuf(self.__visor_imagen, "Original")
        self.__visor_imagen.set_from_pixbuf(pixbuf)
        self.__canales.open(self.__processor)
        self.__primarios.open(self.__processor)
        self.__grises.open(self.__processor)


class ContenedorCanales(gtk.Frame):

    def __init__(self, text):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(text)

        tabla = gtk.Table(columns=4, rows=1, homogeneous=True)
        lista = [" Original: ", " Rojo: ", " Verde: ", " Azul: "]
        if "Grises" in text:
            lista = [" Lightness: ", " Luminosity: ", " Average: ", " Percentual: "]
        elif "Primarios" in text:
             lista = [" Cian: ", " Magenta: ", " Amarillo: "]
        for text in lista:
            _id = lista.index(text)
            tabla.attach_defaults(FrameCanal(text), _id, _id + 1, 0, 1)

        self.add(tabla)
        self.show_all()

    def open(self, processor):
        for frame in self.get_child().get_children():
            frame.open(processor)


class FrameCanal(gtk.Frame):

    def __init__(self, text):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(text)
        self.add(gtk.Image())
        self.show_all()

    def open(self, processor):
        pixbuf = processor.get_pixbuf(self.get_child(), self.get_label())
        self.get_child().set_from_pixbuf(pixbuf)
