#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   NoteBookDirectorios.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM - Uruguay

import os

from gi.repository import Gtk
from gi.repository import GObject

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_pixels

icons = os.path.join(JAMediaObjectsPath, "Iconos")

from Directorios import Directorios


class NoteBookDirectorios(Gtk.Notebook):

    __gtype_name__ = 'JAMediaExplorerNoteBookDirectorios'

    __gsignals__ = {
    "info": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "borrar": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT)),
    "montaje": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    "no-paginas": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)

        self.copiando = False
        self.cortando = False
        self.ver_ocultos = False

        self.show_all()

        self.connect('switch_page', self.__switch_page)

    def recargar(self, valor):
        """
        Recarga todas las lengüetas.
        """

        self.ver_ocultos = valor

        paginas = self.get_children()

        for pagina in paginas:
            directorio = pagina.get_child()
            directorio.load(directorio.path)

    def do_page_removed(self, scroll, num):

        paginas = self.get_children()

        if not paginas:
            self.emit('no-paginas')

    def __switch_page(self, widget, widget_child, indice):

        paginas = self.get_children()

        for pagina in paginas:
            directorio = pagina.get_child()

            if directorio != widget_child.get_child():
                directorio.new_handle(False)

        model, iter_ = widget_child.get_child(
            ).get_selection().get_selected()

        if iter_:
            directorio = model.get_value(iter_, 2)
            self.emit('info', directorio)
            self.emit('montaje', widget_child.get_child().path)

        directorio = widget_child.get_child()
        directorio.new_handle(True)

    def load(self, path):

        paginas = self.get_children()

        if not paginas:
            self.add_leer(path)

        else:
            scrolled = paginas[self.get_current_page()]
            scrolled.get_children()[0].load(path)

            label = self.get_tab_label(scrolled).get_children()[0]

            texto = path
            if len(texto) > 15:
                texto = " . . . " + str(path[-15:])

            label.set_text(texto)

    def __action_add_leer(self, widget, path):

        self.add_leer(path)

    def add_leer(self, path):
        """
        Carga un Directorio y Agrega una Lengüeta para él.
        """

        directorios = Directorios()

        hbox = Gtk.HBox()

        texto = path
        if len(texto) > 15:
            texto = " . . . " + str(path[-15:])

        label = Gtk.Label(texto)

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
        directorios.connect('accion', self.__set_accion)
        directorios.connect('add-leer', self.__action_add_leer)

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

    def __set_accion(self, widget, path, accion):

        iter_ = widget.get_model().get_iter(path)
        direccion = widget.get_model().get_value(iter_, 2)

        if accion == "Copiar":
            self.copiando = direccion
            self.cortando = False

        elif accion == "Pegar":
            if self.cortando:
                from JAMediaObjects.JAMFileSystem import mover
                dire, wid, it = self.cortando

                if mover(dire, direccion):
                    if wid:
                        if wid != widget:
                            wid.get_model().remove(it)

                    widget.collapse_row(path)
                    widget.expand_to_path(path)
                    self.cortando = False
                    #self.copiando = False

            else:
                if self.copiando:
                    from JAMediaObjects.JAMFileSystem import copiar

                    if copiar(self.copiando, direccion):
                        widget.collapse_row(path)
                        widget.expand_to_path(path)
                        #self.copiando = False
                        self.cortando = False

        elif accion == "Cortar":
            self.cortando = (
                direccion, widget, iter_)
            self.copiando = False

    def __emit_borrar(self, widget, direccion, modelo, iter_):
        """
        Cuando se selecciona borrar en el menu de un item.
        """

        self.emit('borrar', direccion, modelo, iter_)

    def __cerrar(self, widget):
        """
        Cerrar la lengüeta seleccionada.
        """

        notebook = widget.get_parent().get_parent()
        paginas = notebook.get_n_pages()

        for indice in range(paginas):
            boton = self.get_tab_label(
                self.get_children()[indice]).get_children()[1]

            if boton == widget:
                self.get_children()[indice].get_child().new_handle(False)
                self.remove_page(indice)
                break
