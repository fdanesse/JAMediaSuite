#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   WorkPanel.py por:
#       Cristian García     <cristian99garcia@gmail.com>
#       Ignacio Rodriguez   <nachoel01@gmail.com>
#       Flavio Danesse      <fdanesse@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import mimetypes
import pyobjects

import gi
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GtkSource
from gi.repository import Pango
from gi.repository import Gdk
from gi.repository import GLib

from Widgets import My_FileChooser
from Widgets import DialogoFormato
from Widgets import DialogoAlertaSinGuardar
from Widgets import DialogoSobreEscritura
from Widgets import DialogoBuscar
from Widgets import DialogoReemplazar
from Widgets import DialogoErrores

import JAMediaObjects
from JAMediaObjects.JAMediaTerminal import JAMediaTerminal

PATH = os.path.dirname(__file__)

home = os.environ["HOME"]

BatovideWorkSpace = os.path.join(
    home, 'BatovideWorkSpace')
    
class WorkPanel(Gtk.Paned):
    """
    Panel, área de trabajo.
        zona superior: Notebook + source view para archivos abiertos
        zona inferior: terminales.
    """
    
    __gtype_name__ = 'WorkPanel'
    
    __gsignals__ = {
    'new_select': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_BOOLEAN)),
    'update_ejecucion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}

    def __init__(self):

        Gtk.Paned.__init__(self,
            orientation=Gtk.Orientation.VERTICAL)
            
        self.notebook_sourceview = Notebook_SourceView()
        self.terminal = JAMediaTerminal()
        
        self.ejecucion = False
        
        self.pack1(self.notebook_sourceview, resize = True, shrink = False)
        self.pack2(self.terminal, resize = False, shrink = True)
        
        self.show_all()
        
        # FIXME: Cambiar fuente en terminal provoca caida de la aplicación.
        self.terminal.toolbar.remove(self.terminal.toolbar.get_children()[3])
        
        self.terminal.set_size_request(-1, 170)
        
        self.notebook_sourceview.connect('new_select', self.__re_emit_new_select)
        self.terminal.connect("ejecucion", self.__set_ejecucion)
        self.terminal.connect("reset", self.detener_ejecucion)

    def __set_ejecucion(self, widget, terminal):
        """
        Cuando se ejecuta un archivo o un proyecto.
        """
        
        self.ejecucion = terminal
        self.terminal.set_sensitive(False)
        self.emit("update_ejecucion", True)
        
    def get_default_path(self):
        """
        Devuelve el Directorio del archivo seleccionado en sourceview.
        """
        
        return self.notebook_sourceview.get_default_path()
        
    def set_linea(self, texto):
        """
        Recibe la linea seleccionada en instrospeccion y
        y la pasa a notebook_sourceview para seleccionarla.
        """
        
        self.notebook_sourceview.set_linea(texto)
        
    def __re_emit_new_select(self, widget, view, estructura):
        """
        Recibe nombre y contenido de archivo seleccionado
        en Notebook_SourceView y los envia BasePanel.
        """
        
        self.emit('new_select', view, estructura)
        
    def abrir_archivo(self, archivo):
        """
        Abre un archivo.
        """
        
        self.notebook_sourceview.abrir_archivo(archivo)
        
    def guardar_archivo(self):
        """
        Guarda un archivo.
        """
        
        self.notebook_sourceview.guardar_archivo()
        
    def guardar_archivo_como(self):
        """
        Ejecuta Guardar Como sobre el archivo seleccionado.
        """
        
        self.notebook_sourceview.guardar_archivo_como()
        
    def ejecutar(self, archivo=None):
        """
        Ejecuta un archivo. Si no se pasa archivo,
        ejecuta el seleccionado en notebooksourceview.
        """
        
        if not archivo or archivo == None:
            ### Cuando se ejecuta el archivo seleccionado.
            pagina = self.notebook_sourceview.get_current_page()
            
            # FIXME: Cuando se hace ejecutar y no hay archivos abiertos.
            # No debiera estar activo el botón ejecutar en este caso.
            if not pagina > -1: return
        
            view = self.notebook_sourceview.get_children()[pagina].get_children()[0]
            
            archivo = view.archivo
            
            ### Si el archivo tiene cambios sin guardar o nunca se guardó.
            if not archivo or archivo == None or view.get_buffer().get_modified():
                dialog = DialogoAlertaSinGuardar(parent_window = self.get_toplevel())
                
                respuesta = dialog.run()
                
                dialog.destroy()
                
                if respuesta == Gtk.ResponseType.ACCEPT:
                    self.guardar_archivo()
                    
                elif respuesta == Gtk.ResponseType.CANCEL:
                    return
                
                elif respuesta == Gtk.ResponseType.CLOSE:
                    return
                    
                archivo = view.archivo
                
        else:
            ### Cuando se ejecuta el main de proyecto.
            source = None
            
            for view in self.get_archivos_de_proyecto(self.get_parent().get_parent().proyecto["path"]):
                if view.archivo == archivo:
                    source = view
                    break
                    
            if source:
                if source.get_buffer().get_modified():
                    dialog = DialogoAlertaSinGuardar(parent_window = self.get_toplevel())
                    
                    respuesta = dialog.run()
                    
                    dialog.destroy()
                    
                    if respuesta == Gtk.ResponseType.ACCEPT:
                        source.guardar()
                        
                    elif respuesta == Gtk.ResponseType.CANCEL:
                        return
                    
                    elif respuesta == Gtk.ResponseType.CLOSE:
                        return
                    
        if archivo: self.terminal.ejecutar(archivo)
        
    def detener_ejecucion(self, widget=None, notebook=None,
        terminal=None, pag_indice=None, boton=None, label=None):
        """
        Detiene la ejecución en proceso.
        """
        
        if self.ejecucion:
            self.ejecucion.set_interprete()
            self.ejecucion = False
            self.terminal.set_sensitive(True)
            self.emit("update_ejecucion", False)
    
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
    Notebook contenedor de sourceview para
    archivos abiertos.
    """

    __gsignals__ = {
     'new_select': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_BOOLEAN))}

    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)
        
        self.show_all()

        self.connect('switch_page', self.__switch_page)
        
        GLib.idle_add(self.abrir_archivo, None)
        
    def set_linea(self, texto):
        """
        Recibe la linea seleccionada en instrospeccion y
        y la selecciona en el sourceview activo.
        """

        scrolled = self.get_children()[self.get_current_page()]
        view = scrolled.get_children()[0]
        buffer = view.get_buffer()

        start = buffer.get_start_iter()
        end = buffer.get_end_iter()

        if start.get_offset() == buffer.get_char_count():
            start = buffer.get_start_iter()

        match = start.forward_search(texto, 0, end)

        if match:
            match_start, match_end = match

            buffer.select_range(match_start, match_end)
            view.scroll_to_iter(match_end, 0.1, 1, 1, 1)
            
    def __switch_page(self, widget, widget_child, indice):
        """
        Cuando el usuario selecciona una lengüeta en
        el notebook, se emite la señal 'new_select'.
        """
        
        view = widget_child.get_child()
        
        self.emit('new_select', view, False)
        
    def abrir_archivo(self, archivo):
        """
        Abre un archivo y agrega una página
        para él, con su código.
        """

        paginas = self.get_children()
        
        for pagina in paginas:
            view = pagina.get_child()
            
            if view.archivo != None and view.archivo == archivo:
                return
        
        sourceview = SourceView()
        
        hbox = Gtk.HBox()
        label = Gtk.Label("Sin Título")
        imagen = Gtk.Image.new_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        boton = Gtk.Button()
        boton.set_relief(Gtk.ReliefStyle.NONE)
        boton.set_size_request(12, 12)
        boton.set_image(imagen)
        
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(boton, False, False, 0)
        
        if archivo and archivo != None:
            if os.path.exists(archivo):
                label.set_text(os.path.basename(archivo))

        sourceview.set_archivo(archivo)

        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        scroll.add(sourceview)

        self.append_page(scroll, hbox)

        label.show()
        boton.show()
        imagen.show()
        self.show_all()
        
        boton.connect("clicked", self.__cerrar)
        
        self.set_current_page(-1)
        
    def guardar_archivo(self):
        """
        Guarda el archivo actual.
        """
        
        paginas = self.get_children()
        
        if paginas:
            scrolled = paginas[self.get_current_page()]
            scrolled.get_children()[0].guardar()
        
    def guardar_archivo_como(self):
        """
        Ejecuta Guardar Como para archivo seleccionado.
        """
        
        paginas = self.get_children()
        
        if paginas:
            scrolled = paginas[self.get_current_page()]
            scrolled.get_children()[0].guardar_archivo_como()
        
    def set_accion(self, accion, valor=True):
        """
        Ejecuta acciones sobre el archivo seleccionado.
        """
        
        paginas = self.get_children()
        
        if not paginas: return
    
        scrolled = paginas[self.get_current_page()]
        sourceview = scrolled.get_children()[0]
        
        ### Ver.
        if accion == "Numeracion":
            for pagina in paginas:
                view = pagina.get_child()
                view.set_accion(accion)
        
        elif accion == "Aumentar":
            for pagina in paginas:
                view = pagina.get_child()
                view.set_formato(tamanio=1)
            
        elif accion == "Disminuir":
            for pagina in paginas:
                view = pagina.get_child()
                view.set_formato(tamanio=-1)
                
        ### Código.
        elif accion == "Formato":
            dialogo = DialogoFormato(parent_window = self.get_toplevel())
            
            respuesta = dialogo.run()
            
            dialogo.destroy()

            if respuesta == Gtk.ResponseType.ACCEPT:
                res = dialogo.obtener_fuente()
                
                for pagina in paginas:
                    view = pagina.get_child()
                    
                    view.set_formato(
                        tamanio=res[1],
                        fuente=res[0],
                        dialogo=True)
                        
        else:
            sourceview.set_accion(accion)
            
    def __cerrar(self, widget):
        """
        Cerrar el archivo seleccionado.
        """
        
        notebook = widget.get_parent().get_parent()
        paginas = notebook.get_n_pages()
        
        for indice in range(paginas):
            boton = self.get_tab_label(self.get_children()[indice]).get_children()[1]
            
            if boton == widget:
                self.get_children()[indice].get_child().set_accion("Cerrar Archivo")
                break
            
    def get_archivos_de_proyecto(self, proyecto_path):
        """
        Devuelve sourceview de todos los archivos abiertos
        de un proyecto según proyecto_path.
        """
        
        paginas = self.get_children()
        sourceviews = []
        
        for pagina in paginas:
            view = pagina.get_child()
            
            if not view.archivo: continue
        
            if proyecto_path in view.archivo:
                sourceviews.append(view)
            
        return sourceviews
    
    def remove_proyect(self, proyecto_path):
        """
        Cuando se elimina el proyecto desde la vista de estructura.
        """
        
        paginas = self.get_children()
        sourceviews = []
        
        for pagina in paginas:
            view = pagina.get_child()
            
            if not view.archivo: continue
        
            if proyecto_path in view.archivo:
                self.remove(pagina)
    
    def get_default_path(self):
        """
        Devuelve el Directorio del archivo seleccionado.
        """
        
        path = None
        pagina = self.get_current_page()
        
        if pagina > -1:
            view = self.get_children()[pagina].get_children()[0]
            archivo = view.archivo
            
            if archivo:
                path = os.path.dirname(view.archivo)
            
        return path
        
class SourceView(GtkSource.View):
    """
    Visor de código para archivos abiertos.
    """
    
    def __init__(self):

        GtkSource.View.__init__(self)
        
        self.archivo = False
        self.lenguaje = False
        self.tab = "    "
        
        self.lenguaje_manager = GtkSource.LanguageManager()
        
        self.lenguajes = {}
        for id in self.lenguaje_manager.get_language_ids():
            lang = self.lenguaje_manager.get_language(id)
            self.lenguajes[id] = lang.get_mime_types()

        self.set_buffer(GtkSource.Buffer())

        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)
        self.set_auto_indent(True)

        self.modify_font(Pango.FontDescription('Monospace 10'))

        completion = self.get_completion()
        completion.add_provider(AutoCompletado(self.get_buffer()))

        self.show_all()
        
        self.connect("key-press-event", self.__key_press_event)

    def set_archivo(self, archivo):
        """
        Setea el archivo cuyo codigo debe mostrarse.
        """
        
        if archivo and archivo != None:
            archivo = os.path.join(archivo.replace("//", "/"))
            
            if os.path.exists(archivo):
                self.archivo = archivo
                texto_file = open(self.archivo, 'r')
                texto = texto_file.read()
                texto_file.close()
                
                self.set_buffer(GtkSource.Buffer())
                self.__set_lenguaje(archivo)
                self.get_buffer().set_text(texto)
                
                self.get_buffer().begin_not_undoable_action()
                self.get_buffer().end_not_undoable_action()
                self.get_buffer().set_modified(False)
                
                nombre = os.path.basename(self.archivo)
                GLib.idle_add(self.__set_label, nombre)
                
        else:
            self.set_buffer(GtkSource.Buffer())
            self.get_buffer().begin_not_undoable_action()
            self.get_buffer().end_not_undoable_action()
            self.get_buffer().set_modified(False)

    def __set_label(self, nombre):
        """
        Setea la etiqueta en notebook con el nombre del archivo.
        """
        
        scroll = self.get_parent()
        notebook = scroll.get_parent()

        paginas = notebook.get_n_pages()

        for indice in range(paginas):
            page = notebook.get_children()[indice]

            if page == scroll:
                pag = notebook.get_children()[indice]
                label = notebook.get_tab_label(pag).get_children()[0]
                label.set_text(nombre)
                
    def __set_lenguaje(self, archivo):
        """
        Setea los colores del texto según tipo de archivo.
        """
        
        self.lenguaje = False
        self.get_buffer().set_highlight_syntax(False)
        self.get_buffer().set_language(None)
        
        tipo = mimetypes.guess_type(archivo)[0]
        
        if tipo:
            for key in self.lenguajes.keys():
                if tipo in self.lenguajes[key]:
                    self.lenguaje = self.lenguaje_manager.get_language(key)
                    self.get_buffer().set_language(self.lenguaje)
                    self.get_buffer().set_highlight_syntax(True)
                    break
        
    def guardar_archivo_como(self):
        """
        Abre un Filechooser para guardar como.
        """
        
        proyecto = self.get_parent().get_parent().get_parent().get_parent().get_parent().proyecto
        
        if proyecto:
            defaultpath = proyecto["path"]
            
        else:
            defaultpath = BatovideWorkSpace
            
        filechooser = My_FileChooser(
            parent_window = self.get_toplevel(),
            action_type = Gtk.FileChooserAction.SAVE,
            title = "Guardar Archivo Como . . .",
            path = defaultpath)

        filechooser.connect('load', self.__guardar_como)

    def guardar(self):
        """
        Si el archivo tiene cambios, lo guarda,
        de lo contrario ejecuta Guardar Como.
        """
        
        if self.archivo and self.archivo != None:
            buffer = self.get_buffer()
            
            if buffer.get_modified() and os.path.exists(self.archivo):
                
                inicio, fin = buffer.get_bounds()
                texto = buffer.get_text(inicio, fin, 0)

                archivo = open(self.archivo, "w")
                archivo.write(texto)
                archivo.close()
                
                buffer.set_modified(False)
                
                ### Forzando actualización de Introspección.
                self.get_parent().get_parent().emit('new_select', self, True)
            
            elif not os.path.exists(self.archivo):
                return self.guardar_archivo_como()
        
        else:
            return self.guardar_archivo_como()
            
    def __guardar_como(self, widget, archivo):
        """
        Ejecuta guardar Como.
        """
        
        if archivo and archivo != None:
            archivo = os.path.join(archivo.replace("//", "/"))
            
            if os.path.exists(archivo):
                dialog = DialogoSobreEscritura(parent_window = self.get_toplevel())
                
                respuesta = dialog.run()
                
                dialog.destroy()
                
                if respuesta == Gtk.ResponseType.ACCEPT:
                    self.archivo = os.path.join(archivo.replace("//", "/"))
                    
                    buffer = self.get_buffer()
                
                    inicio, fin = buffer.get_bounds()
                    texto = buffer.get_text(inicio, fin, 0)

                    archivo = open(self.archivo, "w")
                    archivo.write(texto)
                    archivo.close()
                    
                    self.set_archivo(self.archivo)
                    
                    ### Forzando actualización de Introspección.
                    self.get_parent().get_parent().emit('new_select', self, True)
                    
                elif respuesta == Gtk.ResponseType.CANCEL:
                    return
            
            else:
                self.archivo = os.path.join(archivo.replace("//", "/"))
            
                buffer = self.get_buffer()
                
                inicio, fin = buffer.get_bounds()
                texto = buffer.get_text(inicio, fin, 0)

                archivo = open(self.archivo, "w")
                archivo.write(texto)
                archivo.close()
                
                self.set_archivo(self.archivo)
                
                ### Forzando actualización de Introspección.
                self.get_parent().get_parent().emit('new_select', self, True)
            
    def set_formato(self, fuente=None, tamanio=None, dialogo=False):
        """
        Setea el formato de la fuente.
        
        Recibe fuente o tamaño.
            fuente es: 'Monospace 10'
        """
        
        if not fuente and not tamanio: return
    
        description =  self.get_pango_context().get_font_description()
        
        nombre = description.get_family()
        size = description.get_size()/1000
        
        if type(tamanio) == int and not dialogo:
            size += tamanio
        
        if not fuente:
            fuente = "%s %s" % (nombre, size)
            
        if not dialogo:
            self.modify_font(Pango.FontDescription("%s" % fuente))
            
        else:
            self.modify_font(Pango.FontDescription("%s %s" % (fuente, tamanio)))
        
    def set_accion(self, accion, valor = True):
        """
        Ejecuta acciones sobre el código.
        """
        
        buffer = self.get_buffer()

        if accion == "Deshacer":
            if buffer.can_undo(): buffer.undo()
            
        elif accion == "Rehacer":
            if buffer.can_redo(): buffer.redo()
            
        elif accion == "Seleccionar Todo":
            inicio, fin = buffer.get_bounds()
            buffer.select_range(inicio, fin)
            
        elif accion == "Copiar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

            if buffer.get_selection_bounds():
                inicio, fin = buffer.get_selection_bounds()
                texto = buffer.get_text(inicio, fin, 0)

                clipboard.set_text(texto, -1)
        
        elif accion == "Pegar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            texto = clipboard.wait_for_text()
            if texto != None:
                buffer.insert_at_cursor(texto)
        
        elif accion == "Cortar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

            if buffer.get_selection_bounds():
                start, end = buffer.get_selection_bounds()
                texto_seleccion = buffer.get_text(start, end, 0) ### Texto selección
                buffer.delete(start, end)
                clipboard.set_text(texto_seleccion, -1)

        elif accion == "Buscar Texto":
            try:
                inicio, fin = buffer.get_selection_bounds()
                texto = buffer.get_text(inicio, fin, 0)
                
            except:
                texto = None
                
            dialogo = DialogoBuscar(self,
                parent_window = self.get_toplevel(),
                title = "Buscar Texto", texto = texto)

            dialogo.run()
            
            dialogo.destroy()

        elif accion == "Reemplazar Texto":
            
            texto = ""
            
            try:
                inicio, fin = buffer.get_selection_bounds()
                texto = buffer.get_text(inicio, fin, 0)
                
            except:
                texto = None
                
            dialogo = DialogoReemplazar(self,
                parent_window = self.get_toplevel(),
                title = "Reemplazar Texto", texto = texto)

            dialogo.run()
            
            dialogo.destroy()

        elif accion == "Cerrar Archivo":
            if buffer.get_modified():
                
                dialog = DialogoAlertaSinGuardar(parent_window = self.get_toplevel())
                
                respuesta = dialog.run()
                
                dialog.destroy()
                
                if respuesta == Gtk.ResponseType.ACCEPT:
                    self.guardar()
                    
                elif respuesta == Gtk.ResponseType.CANCEL:
                    return
                
                elif respuesta == Gtk.ResponseType.CLOSE:
                    self.__cerrar()
                    
            else:
                self.__cerrar()
                
        elif accion == "Numeracion":
            self.set_show_line_numbers(valor)

        elif accion == "Identar":
            self.__identar()

        elif accion == "Identar con Espacios":
            # FIXME: convertir . . .
            self.tab = '    '
            #self.__identar()

        elif accion == "Identar con Tabulaciones":
            # FIXME: convertir . . .
            self.tab = '\t'
            #self.__identar()

        elif accion == "De Identar":
            self.__de_identar()

        elif accion == "Valorar":
            if self.lenguaje:
                if self.lenguaje.get_name() == "Python":
                    numeracion = self.get_show_line_numbers()
                    self.set_show_line_numbers(True)
                    
                    # HACK: No se debe permitir usar la interfaz de la aplicación.
                    self.get_toplevel().set_sensitive(False)
                    
                    dialogo = DialogoErrores(self,
                        parent_window = self.get_toplevel(),
                        tipo = "pep8")
                        
                    dialogo.run()
                    
                    dialogo.destroy()

                    self.set_show_line_numbers(numeracion)
                    
                    # HACK: No se debe permitir usar la interfaz de la aplicación.
                    self.get_toplevel().set_sensitive(True)
                    
                else:
                    dialogo = Gtk.Dialog(parent = self.get_toplevel(),
                        flags = Gtk.DialogFlags.MODAL,
                        buttons = ["OK", Gtk.ResponseType.ACCEPT])
                    
                    dialogo.set_size_request(300, 100)
                    dialogo.set_border_width(15)
                    
                    label = Gtk.Label("El Archivo no Contiene Código python.")
                    label.show()
                    
                    dialogo.vbox.pack_start(label, True, True, 0)
                    
                    dialogo.run()
                    
                    dialogo.destroy()
                    
            else:
                dialogo = Gtk.Dialog(parent = self.get_toplevel(),
                    flags = Gtk.DialogFlags.MODAL,
                    buttons = ["OK", Gtk.ResponseType.ACCEPT])
                
                dialogo.set_size_request(300, 100)
                dialogo.set_border_width(15)
                
                label = Gtk.Label("El Archivo no Contiene Código python.")
                label.show()
                
                dialogo.vbox.pack_start(label, True, True, 0)
                
                dialogo.run()
                
                dialogo.destroy()
                
        elif accion == "Chequear":
            if self.lenguaje:
                if self.lenguaje.get_name() == "Python":
                    numeracion = self.get_show_line_numbers()
                    self.set_show_line_numbers(True)
                    
                    # HACK: No se debe permitir usar la interfaz de la aplicación.
                    self.get_toplevel().set_sensitive(False)
                    
                    dialogo = DialogoErrores(self,
                        parent_window = self.get_toplevel(),
                        tipo = "pyflakes")
                        
                    dialogo.run()
                    
                    dialogo.destroy()
                    
                    self.set_show_line_numbers(numeracion)
                    
                    # HACK: No se debe permitir usar la interfaz de la aplicación.
                    self.get_toplevel().set_sensitive(True)
                    
                else:
                    dialogo = Gtk.Dialog(parent = self.get_toplevel(),
                        flags = Gtk.DialogFlags.MODAL,
                        buttons = ["OK", Gtk.ResponseType.ACCEPT])
                    
                    dialogo.set_size_request(300, 100)
                    dialogo.set_border_width(15)
                    
                    label = Gtk.Label("El Archivo no Contiene Código python.")
                    label.show()
                    
                    dialogo.vbox.pack_start(label, True, True, 0)
                    
                    dialogo.run()
                    
                    dialogo.destroy()
                    
            else:
                dialogo = Gtk.Dialog(parent = self.get_toplevel(),
                    flags = Gtk.DialogFlags.MODAL,
                    buttons = ["OK", Gtk.ResponseType.ACCEPT])
                
                dialogo.set_size_request(300, 100)
                dialogo.set_border_width(15)
                
                label = Gtk.Label("El Archivo no Contiene Código python.")
                label.show()
                
                dialogo.vbox.pack_start(label, True, True, 0)
                
                dialogo.run()
                
                dialogo.destroy()
                
    def __identar(self):
        """
        Agrega la identación especificada en el
        texto seleccionado o en la linea en que el
        usuario se encuentra parado.
        """

        buffer = self.get_buffer()
        
        if buffer.get_selection_bounds():
            start, end = buffer.get_selection_bounds()
            texto = buffer.get_text(start, end, True)
            
            id_0 = start.get_line()
            id_1 = end.get_line()
            
            for id in range(id_0, id_1 + 1):
                iter = buffer.get_iter_at_line(id)
                buffer.insert(iter, self.tab)
            
        else:
            textmark = buffer.get_insert()
            textiter = buffer.get_iter_at_mark(textmark)
            id = textiter.get_line()
            line_iter = buffer.get_iter_at_line(id)
            buffer.insert(line_iter, self.tab)

    def __de_identar(self):
        """
        Saca una tabulación a las líneas seleccionadas o en
        la linea donde se encuentra parado el usuario.
        """

        buffer = self.get_buffer()
        
        if buffer.get_selection_bounds():
            start, end = buffer.get_selection_bounds()
            
            id_0 = start.get_line()
            id_1 = end.get_line()
            
            for id in range(id_0, id_1 + 1):
                line_iter = buffer.get_iter_at_line(id)
                chars = line_iter.get_chars_in_line()
                line_end_iter = buffer.get_iter_at_line_offset(id, chars-1)
                
                texto = buffer.get_text(line_iter, line_end_iter, True)
                
                if texto.startswith(self.tab):
                    buffer.delete(line_iter, buffer.get_iter_at_line_offset(id, len(self.tab)))
            
        else:
            textmark = buffer.get_insert()
            textiter = buffer.get_iter_at_mark(textmark)
            id = textiter.get_line()

            line_iter = buffer.get_iter_at_line(id)
            chars = line_iter.get_chars_in_line()
            line_end_iter = buffer.get_iter_at_line_offset(id, chars-1)
            
            texto = buffer.get_text(line_iter, line_end_iter, True)
            
            if texto.startswith(self.tab):
                buffer.delete(line_iter, buffer.get_iter_at_line_offset(id, len(self.tab)))

    def __cerrar(self):
        """
        Cierra la página en el Notebook_SourceView
        que contiene este sourceview.
        """
        
        scroll = self.get_parent()
        notebook = scroll.get_parent()
        
        paginas = notebook.get_n_pages()

        if paginas:
            for indice in range(paginas):
                page = notebook.get_children()[indice]
                
                if page == scroll:
                    notebook.remove_page(indice)
                    break
                
        GLib.idle_add(self.destroy)

    def _marcar_error(self, linea):
        """
        Selecciona el error en la línea especificada.
        """

        if not linea > -1: return
    
        buffer = self.get_buffer()
        start, end = buffer.get_bounds()
        
        linea_iter = buffer.get_iter_at_line(linea - 1)
        linea_iter_next = buffer.get_iter_at_line(linea)
        
        texto = buffer.get_text(linea_iter, linea_iter_next, True)

        buffer.select_range(linea_iter, linea_iter_next)
        self.scroll_to_iter(linea_iter_next, 0.1, 1, 1, 1)

    def __key_press_event(self, widget, event):
        """
        Tabulador Inteligente.
        """
        
        if event.keyval == 65421:
            buffer = self.get_buffer()
        
            textmark = buffer.get_insert()
            textiter = buffer.get_iter_at_mark(textmark)
            id = textiter.get_line()

            line_iter = buffer.get_iter_at_line(id)
            chars = line_iter.get_chars_in_line()
            
            if chars > 2:
                start_iter = buffer.get_iter_at_line_offset(id, chars-2)
                end_iter = buffer.get_iter_at_line_offset(id, chars-1)
                
                texto = buffer.get_text(start_iter, end_iter, True)
                
                if texto == ":":
                    GLib.idle_add(self.__identar)
                    
class AutoCompletado(GObject.Object, GtkSource.CompletionProvider):
    
    __gtype_name__ = 'AutoCompletado'

    def __init__(self, buffer):
        
        GObject.Object.__init__(self)
        
        self.buffer = buffer

    def __set_imports(self, imports):
        """
        Guarda los datos para importaciones previas,
        para calculos de autocompletado.
        """
        
        import shelve

        pathin = os.path.join("/tmp", "shelvein")

        archivo = shelve.open(pathin)
        archivo["Lista"] = imports
        archivo.close()
        
    def __get_auto_completado(self):
        """
        Devuelve la lista de opciones posibles
        para auto completar.
        """
        
        import commands

        pathin = os.path.join("/tmp", "shelvein")
        
        pathout = os.path.join(commands.getoutput(
            'python %s %s' % (
                os.path.join(PATH, "gtkintrospection.py"),
                pathin)))
        
        lista = []
        
        if os.path.exists(pathout):
            ### Obtener lista para autocompletado.
            
            import shelve
            
            archivo = shelve.open(pathout)
            lista = archivo["Lista"]
            archivo.close()
            
        return lista
        
    def __get_auto_completado_for_self(self):
        """
        Devuelve la lista de opciones posibles
        para auto completar en caso de "self.".
        """
        
        lista = []
        
        inicio = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        end = self.buffer.get_end_iter()
        
        ini, fin = self.buffer.get_bounds()
        texto = self.buffer.get_text(ini, fin, True)
        
        if inicio:
            datos = inicio.backward_search("class ", 0, None)
            
            if datos:
                iter = datos[0].get_line()
                
                linea = self.buffer.get_text(datos[0], end, True).splitlines()[0]
                clase = linea.split("class")[1].split("(")[0].strip()
                
                posicion = texto.find(linea)
                finclase = inicio.forward_search("class ", 0, None)
                
                if finclase:
                    linea_iter = finclase[0].get_line()
                    finclase = 0
                    lineas = texto.splitlines()
                    
                    for linea in range(linea_iter + 1):
                        finclase += len(lineas[linea])
                        
                else:
                    finclase = len(texto) - 1

                texto = texto[posicion:finclase]
                objetos = pyobjects.obtener_datos(texto)
                
                for objeto in objetos:
                    lista.append(objeto)
                    
        return lista
    
    def do_activate_proposal(self, dato1, dato2):
        """
        Cuando se selecciona y clickea
        una posible solución.
        """
        
        pass
    
    def do_get_name(self, coso=None, coso2=None):
        """
        Devuelve el nombre del último
        módulo al que se auto completó.
        """
        
        pass

    def do_populate(self, context):
        """
        Cuando se producen cambios en el buffer.
        
        Metodología para autocompletado:
            * Importar todos los paquetes y módulos que se están
                importando en el archivo sobre el cual estamos auto completando.
            * Hacer el auto completado propiamente dicho, trabajando sobre
                la línea de código que se está editando.
        """
        
        ### Iterador de texto sobre el código actual.
        textiter = self.buffer.get_iter_at_mark(self.buffer.get_insert())# Gtk.TextIter
        
        ### indice de linea activa.
        indice_de_linea_activa = textiter.get_line()
        
        ### Texto de la linea activa.
        texto_de_linea_en_edicion = textiter.get_slice(
            self.buffer.get_iter_at_line(indice_de_linea_activa))
        
        ### Si hay un punto en la línea.
        if "." in texto_de_linea_en_edicion:
        
            ### Si el punto está en la última palabra.
            if "." in texto_de_linea_en_edicion.split()[-1]:
                
                ### Auto completado se hace sobre "."
                if texto_de_linea_en_edicion.endswith("."):
                    
                    palabras = texto_de_linea_en_edicion.split()
                    
                    if palabras:
                        ### Importar paquetes y modulos previos
                        inicio = self.buffer.get_start_iter()
                        texto = self.buffer.get_text(inicio, textiter, True)
                        lineas = texto.splitlines()
                        
                        imports = []
                        
                        for linea in lineas:
                            # FIXME: Analizar mejor los casos como ''', """, etc.
                            if "import " in linea and not linea.startswith("#") and \
                                not linea.startswith("\"") and not linea.startswith("'"):
                                    imports.append(linea)

                        ### ['import os', 'import sys', 'from os import path']
                        ### Esto es [] si auto completado se hace antes de los imports
                        
                        ### Auto completado se hace sobre la última palabra
                        palabra = palabras[-1]
                        palabra = palabra.split("(")[-1] # Caso:  class Ventana(gtk.
                        
                        pals = palabra.split(".")[:-1]
                        imports.append(pals) # ['import os', 'import sys', 'from os import path', ['gtk', 'gdk', '']]
                        
                        ### Guardar en un archivo.
                        self.__set_imports(imports)
                        
                        ### Obtener lista para autocompletado.
                        lista = self.__get_auto_completado()
                        
                        #FIXME: HACK para agregar opciones de "self." Debe mejorarse.
                        if texto_de_linea_en_edicion.endswith("self."):
                            for l in self.__get_auto_completado_for_self():
                                lista.append(l)
                            
                        opciones = []
                        
                        for item in lista:
                            opciones.append(GtkSource.CompletionItem.new(item,
                                item, None, None))
                            
                        context.add_proposals(self, opciones, True)
                        
                else:
                    # FIXME: Se está autocompletando.
                    # Esto debe actualizar la lista de opciones disponibles,
                    # Filtrando en la lista según el texto escrito por el usuario.
                    text = texto_de_linea_en_edicion.split(".")[-1]
                    
            else:
                context.add_proposals(self, [], True)
            
        else:
            context.add_proposals(self, [], True)
