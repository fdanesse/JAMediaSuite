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

        self.__canales.connect("toggled", self.__toggled_channel)
        self.__primarios.connect("toggled", self.__toggled_channel)
        self.__grises.connect("toggled", self.__toggled_channel)

    def __toggled_channel(self, contenedor_canal, canal, active):
        self.__canales.disconnect_by_func(self.__toggled_channel)
        self.__primarios.disconnect_by_func(self.__toggled_channel)
        self.__grises.disconnect_by_func(self.__toggled_channel)
        if active:
            if "Colores" in contenedor_canal.get_label():
                if "Original" in canal:
                    # Desactivar Los demás en este canal y todos en los demás canales
                    self.__canales.desactivar(["Rojo", "Verde", "Azul"])
                    self.__primarios.desactivar_all()
                    self.__grises.desactivar_all()
                else:
                    # Permitir 2 colores sin original
                    self.__primarios.desactivar_all()
                    self.__grises.desactivar_all()
                    canales = self.__canales.get_activos()
                    if len(canales) == 3:
                        # 3 colores == original
                        self.__canales.desactivar(["Rojo", "Verde", "Azul"])
                        self.__canales.activar("Original")
                    else:
                        self.__canales.desactivar(["Original"])
            elif "Grises" in contenedor_canal.get_label():
                # Desactivar Los demás en este canal y todos en los demás canales
                self.__canales.desactivar_all()
                self.__primarios.desactivar_all()
                self.__grises.desactivar_distintos(canal)
            elif "Primarios" in contenedor_canal.get_label():
                # Desactivar Los demás en este canal y todos en los demás canales
                self.__canales.desactivar_all()
                self.__primarios.desactivar_distintos(canal)
                self.__grises.desactivar_all()
        else:
            # Si no hay ninguna activa, activar la original
            canales = self.__canales.get_activos()
            for canal in self.__primarios.get_activos():
                canales.append(canal)
            for canal in self.__grises.get_activos():
                canales.append(canal)
            if not len(canales):
                self.__canales.activar("Original")
        canales = self.__canales.get_activos()
        for canal in self.__primarios.get_activos():
            canales.append(canal)
        for canal in self.__grises.get_activos():
            canales.append(canal)
        self.__canales.connect("toggled", self.__toggled_channel)
        self.__primarios.connect("toggled", self.__toggled_channel)
        self.__grises.connect("toggled", self.__toggled_channel)
        self.view(canales)

    def run(self):
        self.__canales.open(self.__processor)
        self.__primarios.open(self.__processor)
        self.__grises.open(self.__processor)

    def view(self, canales):
        pixbuf = self.__processor.get_pixbuf_channles(self.__visor_imagen, canales)
        self.__visor_imagen.set_from_pixbuf(pixbuf)


class ContenedorCanales(gtk.Frame):

    __gsignals__ = {
    "toggled": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, gobject.TYPE_BOOLEAN))}

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
            frame_canal = FrameCanal(text)
            frame_canal.connect("toggled", self.__toggled_channel)
            tabla.attach_defaults(frame_canal, _id, _id + 1, 0, 1)

        self.add(tabla)
        self.show_all()

    def __toggled_channel(self, frame_canal, active):
        canal = frame_canal.get_label().replace(":", "").strip()
        self.emit("toggled", canal, active)

    def open(self, processor):
        for frame in self.get_child().get_children():
            frame.open(processor)

    def desactivar_all(self):
        for frame in self.get_child().get_children():
            frame.desactivar()

    def desactivar(self, canales):
        frames = self.get_child().get_children()
        for canal in canales:
            for frame in frames:
                if canal in frame.get_label():
                    frame.desactivar()

    def desactivar_distintos(self, canal):
        frames = self.get_child().get_children()
        for frame in frames:
            if not canal in frame.get_label():
                frame.desactivar()

    def activar(self, canal):
        frames = self.get_child().get_children()
        for frame in frames:
            if canal in frame.get_label():
                frame.activar()

    def get_activos(self):
        activos = []
        frames = self.get_child().get_children()
        for frame in frames:
            if frame.is_activo():
                activos.append(frame.get_label().replace(":", "").strip())
        return activos


class FrameCanal(gtk.Frame):

    __gsignals__ = {
    "toggled": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self, text):

        gtk.Frame.__init__(self)

        self.set_border_width(4)
        self.set_label(text)
        button = gtk.ToggleButton()
        button.set_image(gtk.Image())
        button.connect("toggled", self.__emit_toggled)
        self.add(button)
        self.show_all()

    def __emit_toggled(self, button):
        self.emit("toggled", button.get_active())

    def open(self, processor):
        image = self.get_child().get_image()
        pixbuf = processor.get_pixbuf(self.get_child(), self.get_label())
        image.set_from_pixbuf(pixbuf)
        if "Original" in self.get_label():
            self.get_child().set_active(True)

    def desactivar(self):
        self.get_child().set_active(False)

    def activar(self):
        self.get_child().set_active(True)

    def is_activo(self):
        return self.get_child().get_active()
