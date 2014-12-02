#!/usr/bin/env python
# -*- coding: utf-8 -*-

# WorkPanel.py por:
#     Cristian García    <cristian99garcia@gmail.com>
#     Ignacio Rodriguez  <nachoel01@gmail.com>
#     Flavio Danesse     <fdanesse@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import os

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GLib

from SourceView import SourceView
from JAMediaTerminal.Terminal import Terminal
from Widgets import DialogoAlertaSinGuardar
from Widgets import DialogoAlertaSinGuardar
from JAMediaTerminal.Widgets import DialogoFormato

from Globales import get_pixels
from Globales import get_boton

BASE_PATH = os.path.dirname(__file__)
icons = os.path.join(BASE_PATH, "Iconos")
home = os.environ["HOME"]
BatovideWorkSpace = os.path.join(home, 'BatovideWorkSpace')


class WorkPanel(Gtk.Paned):
    """
    Panel, área de trabajo.
        zona superior: Notebook + source view para archivos abiertos
        zona inferior: terminales.

    Gtk.VPaned:
        Notebook_SourceView
        JAMediaTerminal
    """

    __gtype_name__ = 'JAMediaEditorWorkPanel'

    __gsignals__ = {
    'new_select': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING)),
    'ejecucion': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN)),
    'update': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}

    def __init__(self):

        Gtk.Paned.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.notebook_sourceview = Notebook_SourceView()
        self.terminal = Terminal()

        # Terminal en ejecución.
        self.ejecucion = False
        # Tipo: proyecto o archivo.
        self.ejecucion_activa = False

        self.pack1(self.notebook_sourceview, resize=True, shrink=False)
        self.pack2(self.terminal, resize=False, shrink=True)

        self.show_all()

        self.terminal.set_size_request(-1, 170)

        self.notebook_sourceview.connect('new_select',
            self.__re_emit_new_select)
        self.notebook_sourceview.connect('update', self.__re_emit_update)

        self.terminal.connect("ejecucion", self.__set_ejecucion)
        self.terminal.connect("reset", self.detener_ejecucion)

        GLib.idle_add(self.terminal.hide)

    def __re_emit_update(self, widget, _dict):
        """
        Emite una señal con el estado general del archivo.
        """
        self.emit("update", _dict)

    def __set_ejecucion(self, widget, terminal):
        """
        Cuando se ejecuta un archivo o un proyecto.
        """
        self.ejecucion = terminal
        self.terminal.set_sensitive(False)

    def __re_emit_new_select(self, widget, view, tipo):
        """
        Recibe nombre y contenido de archivo seleccionado
        en Notebook_SourceView y los envia BasePanel.
        """
        self.emit('new_select', view, tipo)

    def get_default_path(self):
        """
        Devuelve el Directorio del archivo seleccionado en sourceview.
        """
        return self.notebook_sourceview.get_default_path()

    def set_linea(self, index, texto):
        """
        Recibe la linea seleccionada en instrospeccion y
        y la pasa a notebook_sourceview para seleccionarla.
        """
        self.notebook_sourceview.set_linea(index, texto)

    def abrir_archivo(self, archivo):
        """
        Abre un archivo.
        """
        self.notebook_sourceview.abrir_archivo(archivo)

    def guardar_archivo(self):
        self.notebook_sourceview.guardar_archivo()

    def guardar_archivo_como(self):
        self.notebook_sourceview.guardar_archivo_como()

    def ejecutar(self, archivo=None):
        """
        Ejecuta un archivo. Si no se pasa archivo,
        ejecuta el seleccionado en notebooksourceview.
        """

        if not archivo or archivo == None:
            # Cuando se ejecuta el archivo seleccionado.
            pagina = self.notebook_sourceview.get_current_page()
            view = self.notebook_sourceview.get_children()[
                pagina].get_children()[0]

            archivo = view.archivo

            # Si el archivo tiene cambios sin guardar o nunca se guardó.
            if not archivo or archivo == None or \
                view.get_buffer().get_modified():

                dialog = DialogoAlertaSinGuardar(
                    parent_window=self.get_toplevel())

                respuesta = dialog.run()
                dialog.destroy()

                if respuesta == Gtk.ResponseType.ACCEPT:
                    self.guardar_archivo()
                elif respuesta == Gtk.ResponseType.CANCEL:
                    return
                elif respuesta == Gtk.ResponseType.CLOSE:
                    return

                archivo = view.archivo

            self.ejecucion_activa = "archivo"
            self.emit("ejecucion", self.ejecucion_activa, True)

        else:
            # Cuando se ejecuta el main de proyecto.
            source = None
            for view in self.get_archivos_de_proyecto(
                self.get_parent().get_parent().proyecto["path"]):

                if view.archivo == archivo:
                    source = view
                    break

            if source:
                if source.get_buffer().get_modified():
                    dialog = DialogoAlertaSinGuardar(
                        parent_window=self.get_toplevel())
                    respuesta = dialog.run()
                    dialog.destroy()

                    if respuesta == Gtk.ResponseType.ACCEPT:
                        source.guardar()
                    elif respuesta == Gtk.ResponseType.CANCEL:
                        return
                    elif respuesta == Gtk.ResponseType.CLOSE:
                        return

            self.ejecucion_activa = "proyecto"
            self.emit("ejecucion", self.ejecucion_activa, True)

        if archivo:
            self.terminal.ejecutar(archivo)

    def detener_ejecucion(self, widget=None, notebook=None,
        terminal=None, pag_indice=None):
        if self.ejecucion:
            self.ejecucion.set_interprete()
            self.ejecucion = False
            self.terminal.set_sensitive(True)
            self.emit("ejecucion", self.ejecucion_activa, False)
            self.ejecucion_activa = False

    def set_accion_codigo(self, accion):
        """
        Ejecuta acciones sobre el código del archivo seleccionado.
        """
        self.notebook_sourceview.set_accion(accion)

    def set_accion_archivos(self, accion):
        """
        Ejecuta acciones sobre el archivo seleccionado.
        """
        self.notebook_sourceview.set_accion(accion)

    def set_accion_ver(self, accion, valor):
        """
        Ejecuta acciones sobre el archivo seleccionado.
        """
        if accion == "Panel inferior":
            if not valor:
                self.terminal.hide()
            else:
                self.terminal.show()
        elif accion == "Numeracion":
            self.notebook_sourceview.set_accion(accion, valor)

    def get_archivos_de_proyecto(self, proyecto_path):
        """
        Devuelve sourceview de todos los archivos abiertos
        de un proyecto según proyecto_path.
        """
        return self.notebook_sourceview.get_archivos_de_proyecto(proyecto_path)

    def remove_proyect(self, proyecto_path):
        """
        Cuando se elimina el proyecto desde la vista de estructura.
        """
        self.notebook_sourceview.remove_proyect(proyecto_path)


class Notebook_SourceView(Gtk.Notebook):
    """
    Notebook contenedor de sourceview para archivos abiertos.
    """

    __gtype_name__ = 'JAMediaEditorNotebook_SourceView'

    __gsignals__ = {
    'new_select': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING)),
    'update': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}

    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.config = {
            'fuente': 'Monospace',
            'tamanio': 10,
            'numeracion': True,
            }

        self.set_scrollable(True)
        self.ultimo_view_activo = False

        self.show_all()

        self.connect('switch_page', self.__switch_page)

        GLib.idle_add(self.abrir_archivo, False)

    def __switch_page(self, widget, widget_child, indice):
        """
        Cuando el usuario selecciona una lengüeta en el notebook.
        """
        # Detener inspectores y activar solo el seleccionado
        paginas = self.get_children()
        for pagina in paginas:
            view = pagina.get_child()
            view.new_handle(False)

        view = widget_child.get_child()
        if self.ultimo_view_activo != view:
            self.ultimo_view_activo = view
            view.new_handle(True)
            tipo = False
            if view.lenguaje:
                tipo = view.lenguaje.get_name().lower()

            self.emit('new_select', view, tipo)

    def __re_emit_update(self, widget, _dict):
        """
        Emite una señal con el estado general del archivo.
        """
        self.emit("update", _dict)

    def __re_emit_force_select(self, widget, view, lenguaje):
        """
        Forzando Instrospección en Panel Lateral.
        """
        self.emit('new_select', view, lenguaje)

    def __cerrar(self, widget):
        """
        Cerrar el archivo seleccionado.
        """
        notebook = widget.get_parent().get_parent()
        paginas = notebook.get_n_pages()
        for indice in range(paginas):
            boton = self.get_tab_label(
                self.get_children()[indice]).get_children()[1]

            if boton == widget:
                self.get_children()[
                    indice].get_child().set_accion("Cerrar Archivo")
                break

    def set_linea(self, index, texto):
        """
        Recibe la linea seleccionada en instrospeccion y
        y la selecciona en el sourceview activo.
        """

        scrolled = self.get_children()[self.get_current_page()]
        view = scrolled.get_children()[0]
        _buffer = view.get_buffer()

        start, end = _buffer.get_bounds()
        linea_iter = _buffer.get_iter_at_line(index)

        match = linea_iter.forward_search(texto, 0, None)

        if match:
            match_start, match_end = match
            _buffer.select_range(match_end, match_start)
            view.scroll_to_iter(match_end, 0.1, 1, 1, 0.1)

    def abrir_archivo(self, archivo):
        """
        Abre un archivo y agrega una página para él, con su código.
        """
        #try:
        paginas = self.get_children()
        for pagina in paginas:
            view = pagina.get_child()
            if view.archivo and archivo:
                arch1 = os.path.join(view.archivo)
                arch2 = os.path.join(archivo)
                if arch1 == archivo:
                    return False

        sourceview = SourceView(self.config)

        hbox = Gtk.HBox()
        label = Gtk.Label("Sin Título")

        boton = get_boton(os.path.join(icons, "button-cancel.svg"),
            pixels=get_pixels(0.5), tooltip_text="Cerrar")

        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(boton, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(sourceview)
        self.append_page(scroll, hbox)

        sourceview.set_archivo(archivo)

        label.show()
        boton.show()
        self.show_all()

        boton.connect("clicked", self.__cerrar)
        self.set_current_page(-1)
        self.set_tab_reorderable(scroll, True)

        """
        # FIXME: Cuando se abre un archivo, se cierra el vacío por default.
        if len(paginas) > 1:
            for pagina in paginas:
                view = pagina.get_child()

                if not view.archivo:
                    buffer = view.get_buffer()
                    inicio, fin = buffer.get_bounds()
                    buf = buffer.get_text(inicio, fin, 0)

                    if not buf:
                        self.remove(pagina)
                        break
        """

        sourceview.connect("update", self.__re_emit_update)
        sourceview.connect("force-select", self.__re_emit_force_select)

        #except:
        #    print "FIXME: No se ha podido abrir:", archivo

        return False

    def guardar_archivo(self):
        paginas = self.get_children()
        if paginas:
            scrolled = paginas[self.get_current_page()]
            scrolled.get_children()[0].guardar()

    def guardar_archivo_como(self):
        paginas = self.get_children()
        if paginas:
            scrolled = paginas[self.get_current_page()]
            scrolled.get_children()[0].guardar_archivo_como()

    def set_accion(self, accion, valor=True):
        """
        Ejecuta acciones sobre el archivo seleccionado.
        """
        paginas = self.get_children()
        if not paginas:
            return

        scrolled = paginas[self.get_current_page()]
        sourceview = scrolled.get_children()[0]

        # Ver.
        if accion == "Numeracion":
            for pagina in paginas:
                self.config['numeracion'] = valor
                view = pagina.get_child()
                view.set_accion(accion, self.config['numeracion'])

        elif accion == "Aumentar":
            for pagina in paginas:
                self.config['tamanio'] += 1
                view = pagina.get_child()
                view.set_formato(self.config['fuente'], self.config['tamanio'])

        elif accion == "Disminuir":
            for pagina in paginas:
                if self.config['tamanio'] > 6:
                    self.config['tamanio'] -= 1

                view = pagina.get_child()
                view.set_formato(self.config['fuente'], self.config['tamanio'])

        # Código.
        elif accion == "Formato":
            self.get_toplevel().set_sensitive(False)
            dialogo = DialogoFormato(parent_window=self.get_toplevel(),
                fuente=self.config['fuente'], tamanio=self.config['tamanio'])

            respuesta = dialogo.run()
            dialogo.destroy()
            self.get_toplevel().set_sensitive(True)

            if respuesta == Gtk.ResponseType.ACCEPT:
                res = dialogo.get_font()
                self.config['fuente'] = res[0]
                self.config['tamanio'] = res[1]

                for pagina in paginas:
                    view = pagina.get_child()
                    view.set_formato(self.config['fuente'],
                    self.config['tamanio'])

        else:
            sourceview.set_accion(accion)

    def do_page_removed(self, scroll, num):
        paginas = self.get_children()
        if not paginas:
            self.abrir_archivo(False)
        self.get_toplevel().set_sensitive(True)

    def get_archivos_de_proyecto(self, proyecto_path):
        """
        Devuelve sourceview de todos los archivos abiertos
        de un proyecto según proyecto_path.
        """
        paginas = self.get_children()
        sourceviews = []
        for pagina in paginas:
            view = pagina.get_child()
            if not view.archivo:
                continue
            if proyecto_path in view.archivo:
                sourceviews.append(view)
        return sourceviews

    def remove_proyect(self, proyecto_path):
        """
        Cuando se elimina el proyecto desde la vista de estructura.
        """
        paginas = self.get_children()
        for pagina in paginas:
            view = pagina.get_child()
            if not view.archivo:
                continue
            if proyecto_path in view.archivo:
                self.remove(pagina)

    def get_default_path(self):
        """
        Devuelve el Directorio del archivo seleccionado.
        """
        path = False
        pagina = self.get_current_page()
        if pagina > -1:
            view = self.get_children()[pagina].get_children()[0]
            archivo = view.archivo
            if archivo:
                path = os.path.dirname(view.archivo)
        return path
