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

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GtkSource
from gi.repository import Pango
from gi.repository import Gdk
from gi.repository import GLib

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

icons = os.path.join(JAMediaObjectsPath, "Iconos")

from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_pixels

PATH = os.path.dirname(__file__)

home = os.environ["HOME"]

BatovideWorkSpace = os.path.join(
    home, 'BatovideWorkSpace')
    
class WorkPanel(Gtk.Paned):
    """
    Panel, área de trabajo.
        zona superior: Notebook + source view para archivos abiertos
        zona inferior: terminales.
        
    Gtk.Paned:
        Notebook_SourceView
        JAMediaObjects.JAMediaTerminal
    """
    
    __gtype_name__ = 'JAMediaEditorWorkPanel'
    
    __gsignals__ = {
    'new_select': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_BOOLEAN)),
    'close_all_files': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Paned.__init__(self,
            orientation=Gtk.Orientation.VERTICAL)
            
        from JAMediaObjects.JAMediaTerminal import JAMediaTerminal
        
        self.notebook_sourceview = Notebook_SourceView()
        self.terminal = JAMediaTerminal()
        
        self.ejecucion = False
        
        self.pack1(self.notebook_sourceview,
            resize = True, shrink = False)
        self.pack2(self.terminal,
            resize = False, shrink = True)
        
        self.show_all()
        
        # FIXME: Cambiar fuente en terminal provoca caida de la aplicación.
        #self.terminal.toolbar.remove(
        #    self.terminal.toolbar.get_children()[3])
        
        self.terminal.set_size_request(-1, 170)
        
        self.notebook_sourceview.connect('new_select',
            self.__re_emit_new_select)
        self.notebook_sourceview.connect('close_all_files',
            self.__close_all_files)
        self.terminal.connect("ejecucion", self.__set_ejecucion)
        self.terminal.connect("reset", self.detener_ejecucion)

    def __close_all_files(self, widget):
        
        self.emit('close_all_files')
        
    def __set_ejecucion(self, widget, terminal):
        """
        Cuando se ejecuta un archivo o un proyecto.
        """
        
        self.ejecucion = terminal
        self.terminal.set_sensitive(False)
        
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
                from Widgets import DialogoAlertaSinGuardar
                
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
                    from Widgets import DialogoAlertaSinGuardar
                    
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
        terminal=None, pag_indice=None):
        """
        Detiene la ejecución en proceso.
        """
        
        if self.ejecucion:
            self.ejecucion.set_interprete()
            self.ejecucion = False
            self.terminal.set_sensitive(True)
    
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

    __gtype_name__ = 'JAMediaEditorNotebook_SourceView'
    
    __gsignals__ = {
     'new_select': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_BOOLEAN)),
    'close_all_files': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Notebook.__init__(self)
        
        self.config = {
            'fuente':'Monospace',
            'tamanio':10,
            'numeracion':False,
            }
        
        self.set_scrollable(True)
        self.ultimo_view_activo = False

        self.show_all()

        self.connect('switch_page', self.__switch_page)
        
        GLib.idle_add(self.abrir_archivo, None)
        
    def do_page_removed(self, uno, dos):
        
        paginas = self.get_children()
        if not paginas:
            self.emit("close_all_files")
        
    def set_linea(self, index, texto):
        """
        Recibe la linea seleccionada en instrospeccion y
        y la selecciona en el sourceview activo.
        """

        scrolled = self.get_children()[self.get_current_page()]
        view = scrolled.get_children()[0]
        buffer = view.get_buffer()

        start, end = buffer.get_bounds()
        linea_iter = buffer.get_iter_at_line(index)

        match = linea_iter.forward_search(texto, 0, None)
        
        if match:
            match_start, match_end = match
            buffer.select_range(match_end, match_start)
            view.scroll_to_iter(match_end, 0.1, 1, 1, 0.1)

    def __switch_page(self, widget, widget_child, indice):
        """
        Cuando el usuario selecciona una lengüeta en
        el notebook, se emite la señal 'new_select'.
        """

        ### Detener inspectores y activar solo el seleccionado
        paginas = self.get_children()
        
        for pagina in paginas:
            view = pagina.get_child()
            view.new_handle(False)
            
        view = widget_child.get_child()
        view.new_handle(True)

        if view != self.ultimo_view_activo:
            self.emit('new_select', view, False)

        self.ultimo_view_activo = view
        
    def abrir_archivo(self, archivo):
        """
        Abre un archivo y agrega una página
        para él, con su código.
        """
        
        paginas = self.get_children()
        
        for pagina in paginas:
            view = pagina.get_child()
            
            if view.archivo and view.archivo == archivo:
                return
            
            ### Cuando se abre un archivo, se cierra el vacío por default.
            if not view.archivo:
                buffer = view.get_buffer()
                inicio, fin = buffer.get_bounds()
                buf = buffer.get_text(inicio, fin, 0)
                if not buf: self.remove(pagina)
            
        sourceview = SourceView(self.config)
        
        hbox = Gtk.HBox()
        label = Gtk.Label("Sin Título")
        
        boton = get_boton(
            os.path.join(icons, "button-cancel.svg"),
            pixels = get_pixels(0.5),
            tooltip_text = "Cerrar")
        
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(boton, False, False, 0)
        
        if archivo:
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
        self.show_all()
        
        boton.connect("clicked", self.__cerrar)
        
        self.set_current_page(-1)
        
        self.set_tab_reorderable(scroll, True)
        
        return False
    
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
                self.config['numeracion'] = valor
                view = pagina.get_child()
                view.set_accion(accion, self.config['numeracion'])
                
        elif accion == "Aumentar":
            for pagina in paginas:
                self.config['tamanio'] += 1

                view = pagina.get_child()
                view.set_formato(
                    self.config['fuente'],
                    self.config['tamanio'])
                    
        elif accion == "Disminuir":
            for pagina in paginas:
                if self.config['tamanio'] > 6:
                    self.config['tamanio'] -= 1
                
                view = pagina.get_child()
                view.set_formato(
                    self.config['fuente'],
                    self.config['tamanio'])
                
        ### Código.
        elif accion == "Formato":
            from JAMediaObjects.JAMediaTerminal import DialogoFormato
            
            self.get_toplevel().set_sensitive(False)
            
            dialogo = DialogoFormato(
                parent_window = self.get_toplevel(),
                fuente = self.config['fuente'],
                tamanio = self.config['tamanio'])
            
            respuesta = dialogo.run()
            
            dialogo.destroy()

            self.get_toplevel().set_sensitive(True)
            
            if respuesta == Gtk.ResponseType.ACCEPT:
                res = dialogo.get_font()
                
                self.config['fuente'] = res[0]
                self.config['tamanio'] = res[1]
                
                for pagina in paginas:
                    view = pagina.get_child()
                    
                    view.set_formato(
                        self.config['fuente'],
                        self.config['tamanio'])
                    
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
    
    __gtype_name__ = 'JAMediaEditorSourceView'
    
    def __init__(self, config):

        GtkSource.View.__init__(self)
        
        self.actualizador = False
        self.control = False
        self.archivo = False
        self.lenguaje = False
        self.tab = "    "
        
        self.set_show_line_numbers(config['numeracion'])
        
        self.lenguaje_manager = GtkSource.LanguageManager()
        
        self.lenguajes = {}
        for id in self.lenguaje_manager.get_language_ids():
            lang = self.lenguaje_manager.get_language(id)
            self.lenguajes[id] = lang.get_mime_types()

        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)
        self.set_auto_indent(True)
        
        font = "%s %s" % (config['fuente'], config['tamanio'])
        self.modify_font(Pango.FontDescription(font))

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
                self.get_buffer().begin_not_undoable_action()
                self.__set_lenguaje(archivo)
                self.get_buffer().set_text(texto)
                
                nombre = os.path.basename(self.archivo)
                GLib.idle_add(self.__set_label, nombre)
                
                self.control = os.path.getmtime(self.archivo)
                
        else:
            self.set_buffer(GtkSource.Buffer())
            self.get_buffer().begin_not_undoable_action()
            
        self.get_buffer().end_not_undoable_action()
        self.get_buffer().set_modified(False)
        
        completion = self.get_completion()
        
        prov_words = GtkSource.CompletionWords.new(None, None)
        prov_words.register(self.get_buffer())
        
        autocompletado = AutoCompletado(self.get_buffer(), self.archivo, self)
        completion.add_provider(autocompletado)
        
        completion.set_property("remember-info-visibility", True)
        completion.set_property("select-on-show", True)
        completion.set_property("show-headers", True)
        completion.set_property("show-icons", True)
        
        self.new_handle(True)

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
                
        return False
    
    def __set_lenguaje(self, archivo):
        """
        Setea los colores del texto según tipo de archivo.
        """
        
        self.lenguaje = False
        self.get_buffer().set_highlight_syntax(False)
        self.get_buffer().set_language(None)
        
        import mimetypes
        
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
            
        from Widgets import My_FileChooser
        
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
                self.control = os.path.getmtime(self.archivo)
                
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
                from Widgets import DialogoSobreEscritura
                
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
    
    def set_formato(self, fuente, tamanio):
        """
        Setea el formato de la fuente.
        
        Recibe fuente o tamaño.
            fuente es: 'Monospace 10'
        """
        
        if not fuente or not tamanio: return
    
        self.modify_font(Pango.FontDescription("%s %s" % (fuente, tamanio)))
    
    def set_accion(self, accion, valor = True):
        """
        Ejecuta acciones sobre el código.
        """
        
        buffer = self.get_buffer()
        
        if accion == "Deshacer":
            if buffer.can_undo():
                buffer.undo()
                
        elif accion == "Rehacer":
            if buffer.can_redo():
                buffer.redo()
            
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
                if buffer.get_selection_bounds():
                    start, end = buffer.get_selection_bounds()
                    texto_seleccion = buffer.get_text(start, end, 0) ### Texto selección
                    buffer.delete(start, end)
                
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
                
            from Widgets import DialogoBuscar
            
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
                
            from Widgets import DialogoReemplazar
            
            dialogo = DialogoReemplazar(self,
                parent_window = self.get_toplevel(),
                title = "Reemplazar Texto", texto = texto)

            dialogo.run()
            
            dialogo.destroy()

        elif accion == "Cerrar Archivo":
            if buffer.get_modified():
                from Widgets import DialogoAlertaSinGuardar
                
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

        elif accion == "Chequear":
            if self.lenguaje:
                if self.lenguaje.get_name() == "Python":
                    numeracion = self.get_show_line_numbers()
                    self.set_show_line_numbers(True)
                    
                    # HACK: No se debe permitir usar la interfaz de la aplicación.
                    self.get_toplevel().set_sensitive(False)
                    
                    from Widgets import DialogoErrores
                    
                    dialogo = DialogoErrores(self,
                        parent_window = self.get_toplevel())
                        
                    dialogo.run()
                    dialogo.destroy()

                    self.set_show_line_numbers(numeracion)
                    
                    # HACK: No se debe permitir usar la interfaz de la aplicación.
                    self.get_toplevel().set_sensitive(True)
                    return
                
            dialogo = Gtk.Dialog(parent = self.get_toplevel(),
                flags = Gtk.DialogFlags.MODAL,
                buttons = ["OK", Gtk.ResponseType.ACCEPT])
            
            dialogo.set_size_request(300, 100)
            dialogo.set_border_width(15)
            
            label = Gtk.Label("El Archivo no Contiene Código python\no Todavía no ha Sido Guardado.")
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

    def _marcar_error(self, linea):
        """
        Selecciona el error en la línea especificada.
        """

        # FIXME: Esto no funciona en la última línea.
        if not linea > -1:
            return

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
            
            if chars > 3:
                ### Ultimo caracter.
                start_iter = buffer.get_iter_at_line_offset(id, chars-2)
                end_iter = buffer.get_iter_at_line_offset(id, chars-1)
                
                texto = buffer.get_text(start_iter, end_iter, True)
                
                if texto == ":":
                    ### Tola la linea.
                    line_end_iter = buffer.get_iter_at_line_offset(id, chars-1)
                    texto = buffer.get_text(line_iter, line_end_iter, True)
                    
                    tabs = 0
                    if texto.startswith(self.tab):
                        tabs = len(texto.split(self.tab))-1
                    
                    GLib.idle_add(self.__forzar_identacion, tabs+1)
                    
    def __forzar_identacion(self, tabs):
        
        buffer = self.get_buffer()

        textmark = buffer.get_insert()
        textiter = buffer.get_iter_at_mark(textmark)
        id = textiter.get_line()
        
        line_iter = buffer.get_iter_at_line(id)
        chars = line_iter.get_chars_in_line()
        
        buffer.delete(line_iter, buffer.get_iter_at_line_offset(id, chars-1))
        
        for tab in range(0, tabs):
            self.__identar()
            
        return False
    
    def new_handle(self, reset):
        
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
            
        if reset:
            self.actualizador = GLib.timeout_add(1000, self.__handle)
            
    def __handle(self):
        """
        Controla posibles modificaciones externas a este archivo.
        """
        
        if self.archivo:
            if os.path.exists(self.archivo):
                if self.control:
                    if self.control != os.path.getmtime(self.archivo):
                        dialogo = Gtk.Dialog(
                            parent = self.get_toplevel(),
                            flags = Gtk.DialogFlags.MODAL,
                            buttons = [
                                "Recargar", Gtk.ResponseType.ACCEPT,
                                "Continuar sin recargar", Gtk.ResponseType.CANCEL])
                                
                        dialogo.set_border_width(15)
                        
                        label = Gtk.Label("El archivo ha sido modificado por otra aplicación.")
                        label.show()
                        
                        dialogo.vbox.pack_start(label, True, True, 0)
                        
                        response = dialogo.run()
                        dialogo.destroy()
                        
                        if Gtk.ResponseType(response) == Gtk.ResponseType.ACCEPT:
                            self.set_archivo(self.archivo)
                        
                        elif Gtk.ResponseType(response) == Gtk.ResponseType.CANCEL:
                            return False
                        
                else:
                    self.control = os.path.getmtime(self.archivo)
            
            elif not os.path.exists(self.archivo):
                dialogo = Gtk.Dialog(
                    parent = self.get_toplevel(),
                    flags = Gtk.DialogFlags.MODAL,
                    buttons = [
                        "Guardar", Gtk.ResponseType.ACCEPT,
                        "Continuar sin guardar", Gtk.ResponseType.CANCEL])
                        
                dialogo.set_border_width(15)
                
                label = Gtk.Label("El archivo fue eliminado o\n movido de lugar por otra aplicación.")
                label.show()
                
                dialogo.vbox.pack_start(label, True, True, 0)
                
                response = dialogo.run()
                dialogo.destroy()
                
                if Gtk.ResponseType(response) == Gtk.ResponseType.ACCEPT:
                    self.guardar()
                
                elif Gtk.ResponseType(response) == Gtk.ResponseType.CANCEL:
                    return False
                
        else:
            return False
        
        return True
    
class AutoCompletado(GObject.Object, GtkSource.CompletionProvider):
    
    __gtype_name__ = 'AutoCompletado'

    def __init__(self, buffer, archivo, parent):
        
        GObject.Object.__init__(self)
        
        self.parent = parent
        self.archivo = archivo
        self.buffer = buffer
        self.opciones = []
        self.priority = 1
        
        from SpyderHack.SpyderHack import SpyderHack
        
        self.spyder_hack = SpyderHack()
    
    def do_get_name(self):
        return "AutoCompletado"
    
    def do_populate(self, context):
        """
        Cuando se producen cambios en el buffer.
        
        Metodología para autocompletado:
            * Importar todos los paquetes y módulos que se están
                importando en el archivo sobre el cual estamos auto completando.
            * Hacer el auto completado propiamente dicho, trabajando sobre
                la línea de código que se está editando.
        """
        
        textiter = context.get_iter()                                   ### Iterador de texto sobre el código actual.
        indice_de_linea_activa = textiter.get_line()                    ### indice de linea activa.
        texto_de_linea_en_edicion = textiter.get_slice(
            self.buffer.get_iter_at_line(indice_de_linea_activa))       ### Texto de la linea activa.
        
        expresion = ''
        ### Auto completado se hace sobre "."
        if texto_de_linea_en_edicion.endswith("."):
            
            expresion = str(texto_de_linea_en_edicion.split()[-1][:-1]).strip()
         
            if expresion:
                if "(" in expresion: # Para el caso en que el usuario se encuentra escribiendo class V(Gtk.
                    expresion = expresion.split("(")[-1].strip()
                    
                lista = self.__get_list(expresion)
                
                opciones = []
                self.opciones = []
                
                for item in lista:
                    self.opciones.append(item)
                    opciones.append(
                        GtkSource.CompletionItem.new(
                            item, item, None, None))
                
                context.add_proposals(self, opciones, True)
                
        else:
            ### Actualizando Autocompletado cuando está Visible.
            text = texto_de_linea_en_edicion.split(".")[-1]
            
            new_opciones = []
            opciones = []
            
            for opcion in self.opciones:
                if opcion.startswith(text): # http://docs.python.org/release/2.5.2/lib/string-methods.html
                    new_opciones.append(opcion)
                    opciones.append(GtkSource.CompletionItem.new(
                        opcion, opcion, None, None))
                        
            self.opciones = new_opciones
            context.add_proposals(self, opciones, True)
        
    def __get_list(self, expresion):
        """
        Devuelve la lista de opciones para autocompletado.
        """
        
        if self.archivo:
            workpath = os.path.dirname(self.archivo)
            
        elif self.parent.get_toplevel().base_panel.proyecto:
            workpath = self.parent.get_toplevel().base_panel.proyecto.get("path", "")
            
        else:
            home = os.environ["HOME"]
            workpath = os.path.join(
                home, 'BatovideWorkSpace')
        
        return self.spyder_hack.Run(workpath, expresion, self.buffer)
        
GObject.type_register(AutoCompletado)
