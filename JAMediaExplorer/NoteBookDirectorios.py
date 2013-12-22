#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   NoteBookDirectorios.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM - Uruguay

import os

from gi.repository import Gtk
from gi.repository import GObject

from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_pixels

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

icons = os.path.join(JAMediaObjectsPath, "Iconos")

from Directorios import Directorios


class NoteBookDirectorios(Gtk.Notebook):

    __gtype_name__ = 'JAMediaExplorerNoteBookDirectorios'

    __gsignals__ = {
    "info": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "borrar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)

        self.show_all()

    def load(self, path):

        paginas = self.get_children()

        if not paginas:
            self.__add(path)

        else:
            scrolled = paginas[self.get_current_page()]
            scrolled.get_children()[0].load(path)

    def __add(self, path):
        """
        Carga un Directorio y Agrega una Lengüeta para él.
        """

        directorios = Directorios()

        hbox = Gtk.HBox()
        label = Gtk.Label("Sin Título")

        boton = get_boton(
            os.path.join(icons, "button-cancel.svg"),
            pixels=get_pixels(0.5),
            tooltip_text="Cerrar")

        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(boton, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add(directorios)

        self.append_page(scroll, hbox)

        label.show()
        boton.show()
        self.show_all()

        directorios.connect('info', self.__emit_info)
        directorios.connect('borrar', self.__emit_borrar)

        directorios.load(path)

        boton.connect("clicked", self.__cerrar)

        self.set_current_page(-1)

        self.set_tab_reorderable(scroll, True)

        return False

    def __emit_info(self, widget, path):
        """
        Cuando el usuario selecciona un archivo
        o directorio en la estructura de directorios,
        pasa la informacion del mismo a la ventana principal.
        """

        self.emit('info', path)

    def __emit_borrar(self, widget, direccion, modelo, iter_):
        """
        Cuando se selecciona borrar en el menu de un item.
        """

        self.emit('borrar', direccion, modelo, iter_)

    def __cerrar(self, widget):
        """
        Cerrar la lengueta seleccionada.
        """

        notebook = widget.get_parent().get_parent()
        paginas = notebook.get_n_pages()

        for indice in range(paginas):
            boton = self.get_tab_label(
                self.get_children()[indice]).get_children()[1]

            if boton == widget:
                self.remove_page(indice)
                break
