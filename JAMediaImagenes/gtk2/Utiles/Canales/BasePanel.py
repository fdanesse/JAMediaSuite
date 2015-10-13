#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject


class BasePanel(gtk.Table):

    def __init__(self):

        gtk.Table.__init__(self, columns=4, rows=4, homogeneous=True)

        self.set_border_width(2)

        self.__visor_imagen = gtk.Image()
        self.__visor_imagen.set_size_request(320, 240)
        self.__canales = ContenedorCanales(" Colores: ")
        self.__grises = ContenedorCanales(" Grises: ")

        self.attach_defaults(self.__visor_imagen, 0, 4, 0, 2)
        self.attach_defaults(self.__canales, 0, 4, 2, 3)
        self.attach_defaults(self.__grises, 0, 4, 3, 4)

        self.show_all()


class ContenedorCanales(gtk.Frame):

    def __init__(self, text):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(text)

        tabla = gtk.Table(columns=4, rows=1, homogeneous=True)
        lista = [" Original: ", " Rojo: ", " Verde: ", " Azul: "]
        if "Grises" in text:
            lista = [" Lightness: ", " Luminosity: ",
                " Average: ", " Percentual: "]
        for text in lista:
            _id = lista.index(text)
            tabla.attach_defaults(FrameCanal(text), _id, _id + 1, 0, 1)

        self.add(tabla)
        self.show_all()


class FrameCanal(gtk.Frame):

    def __init__(self, text):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(text)
        self.add(gtk.Image())
        self.show_all()
