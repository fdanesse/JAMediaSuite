#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject


class BasePanel(gtk.VPaned):

    def __init__(self):

        gtk.VPaned.__init__(self)

        self.set_border_width(2)

        self.__visor_imagen = gtk.Image()
        self.__vbox_canales = gtk.VBox()

        self.__canales = ContenedorCanales("canales")
        self.__grises = ContenedorCanales("grises")

        self.__vbox_canales.pack_start(self.__canales, False, False, 0)
        self.__vbox_canales.pack_start(self.__grises, False, False, 0)

        self.pack1(self.__visor_imagen, resize=True, shrink=True)
        self.pack2(self.__vbox_canales, resize=False, shrink=False)

        self.show_all()


class ContenedorCanales(gtk.Frame):

    def __init__(self, text):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(text)
        #self.set_size_request(-1, 100)

        tabla = gtk.Table(columns=4, rows=1, homogeneous=True)
        lista = [" Original ", " Rojo (R = red) ",
            " Verde (G = green) ", " Azul (B = blue) "]
        if text == "grises":
            lista = [" Lightness ", " Luminosity ",
                " Average ", " Percentual "]
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
