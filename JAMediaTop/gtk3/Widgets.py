#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

import os
import sys

import gi
from gi.repository import Gtk
from gi.repository import GObject

import JAMediaSystemState as JAMSS


class TopView(Gtk.TreeView):

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.TreeStore(
            GObject.TYPE_INT, GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_property("enable-grid-lines", True)
        self.set_property("enable-tree-lines", True)
        #self.set_tooltip_text("Click Derecho para Opciones")

        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.__setear_columnas()
        self.show_all()

        #self.set_sensitive(False)

        #self.treeselection = self.get_selection()
        #self.treeselection.set_select_function(self.selecciones, self.modelo)

        self.connect("row-expanded", self.__expandir, None)
        #self.connect("row-activated", self.activar, None)
        #self.connect("row-collapsed", self.colapsar, None)

    def __add_threads(self, pid, iteractual):
        """
        Agrega al treview los procesos hijos de un
        determinado proceso segun pid.
        """
        model = self.get_model()
        thread_ids = JAMSS.get_process_threads(pid)

        for thread in thread_ids:
            thread = int(thread)
            nombre = JAMSS.get_process_name(thread)
            com = JAMSS.get_process_cmdline(pid)

            comandos = ''
            for c in com:
                comandos += "%s " % c

            comandos = comandos.strip()
            model.append(iteractual, [thread, nombre, comandos])
            #iter_child = model.iter_children(iteractual)
            #path = model.get_path(iter_child)
            #GLib.idle_add(self.expand_to_path, path)

    def __setear_columnas(self):
        self.append_column(self.__construir_columa('Pid', 0, True))
        self.append_column(self.__construir_columa('Proceso', 1, True))
        self.append_column(self.__construir_columa('Ejecutable', 2, True))

    def __construir_columa(self, text, index, visible):
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('resizable', True)
        columna.set_property('visible', visible)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna

    def __expandir(self, treeview, iter, path, user_param1):
        """
        Cuando se expande una fila, se agregan los datos
        de procesos hijos del proceso en este path.
        """
        model = self.get_model()
        iter_child = model.iter_children(iter)
        pid = model.get_value(iter_child, 0)
        self.__add_threads(pid, iter_child)

    def set_tree(self, datos):
        """
        Setea el treeview con los datos de procesos en top.
        Manda expandir el nuevo path en el treeview, lo cual
        desencadena la secuencia de agregado de hijos del proceso.
        """
        model = self.get_model()
        model.clear()

        iter = model.get_iter_first()
        for dato in datos:
            pid = int(dato[0])

            if 'running' in JAMSS.get_process_status(pid)[1]:
                iteractual = model.append(iter, dato)
                self.__add_threads(pid, iteractual)
                path = model.get_path(iteractual)
                self.expand_to_path(path)
