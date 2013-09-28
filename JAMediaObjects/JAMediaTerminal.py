#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTerminal.py por:
#       Flavio Danesse      <fdanesse@gmail.com>
#                           CeibalJAM! - Uruguay

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
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import Vte
#from gi.repository import Pango
from gi.repository import GLib

BASEPATH = os.path.dirname(__file__)

from JAMediaGlobales import get_separador
from JAMediaGlobales import get_boton
from JAMediaGlobales import get_pixels

Width_Button = 0.5

#FAMILIES = Gtk.Window().get_pango_context().list_families()

class JAMediaTerminal(Gtk.Box):
    """
    Terminal (NoteBook + Vtes) + Toolbar.
    """
    
    __gtype_name__ = 'JAMediaTerminal'
    
    __gsignals__ = {
    "ejecucion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
    "reset":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_PYOBJECT, GObject.TYPE_INT,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT))}
        
    def __init__(self):
        
        Gtk.Box.__init__(self,
            orientation = Gtk.Orientation.VERTICAL)
        
        self.notebook = NoteBookTerminal()
        self.toolbar = ToolbarTerminal()
        
        self.pack_start(self.notebook, True, True, 0)
        self.pack_start(self.toolbar, False, False, 0)
        
        self.show_all()
        
        self.toolbar.connect('accion', self.__accion_terminal)
        self.toolbar.connect('reset', self.__reset_terminal)
        self.toolbar.connect('formato', self.__set_formato)
        
        self.notebook.agregar_terminal()
        self.notebook.connect("reset", self.__re_emit_reset)
        
    def __set_formato(self, widget):
        """
        Abre el Diálogo de Formato y Setea el tipo y tamaño de
        fuentes en las terminales según selección del usuario.
        """
        
        #string = self.notebook.fuente.to_string()
        #tamanio = int(string.split(" ")[-1])
        #fuente = string.replace("%s" % tamanio, "").strip()
        
        dialogo = DialogoFormato(
            parent_window = self.get_toplevel())#,
            #fuente = fuente,
            #tamanio = tamanio)
        
        respuesta = dialogo.run()
        
        font = ""
        if respuesta == Gtk.ResponseType.ACCEPT:
            font = "%s %s" % dialogo.get_font()
            
        dialogo.destroy()
        
        if font: self.notebook.set_font(font)
        
    def __re_emit_reset(self, notebook, terminal, pag_indice, boton, label):
        """
        Cuando se resetea una terminal, se emite la señal reset con:
            1- Notebook contenedor de terminales.
            2- Terminal reseteada.
            3- Indice de la página que le corresponde en el notebook.
            4- Botón cerrar de la lengueta específica.
            5- Etiqueta de la lengüeta específica.
        """
        
        self.emit("reset", notebook, terminal, pag_indice, boton, label)
        
    def __reset_terminal(self, widget, interprete):
        """
        Resetea la terminal en interprete según valor.
        """
        
        self.notebook.reset_terminal(interprete = interprete)
        
    def __accion_terminal(self, widget, accion):
        """
        Soporte para clipboard.
        """
        
        self.notebook.accion_terminal(accion)
        
    def ejecutar(self, archivo):
        """
        Ejecuta un archivo en una nueva terminal.
        """
        
        if os.path.exists(archivo):

            path = os.path.basename(archivo)
            
            terminal = self.notebook.agregar_terminal(
                path=path,
                interprete='/bin/bash',
                ejecutar=archivo)
        
            self.emit("ejecucion", terminal)
    
    def ejecute_script(self, dirpath, interprete, path_script, param):
        """
        Ejecuta un script con parámetros, en la terminal activa
        
        Por ejemplo:
            python setup.py sdist
            
            dirpath     =   directorio base donde se encuentra setup.py
            interprete  =   python en este caso
            path_script =   dirpath + 'setup.py'
            param       =   'sdist' en est caso
        """
        
        terminal = self.notebook.get_children()[self.notebook.get_current_page()]
        
        pty_flags = Vte.PtyFlags(0)
        
        terminal.fork_command_full(
            pty_flags,
            dirpath,
            (interprete, path_script, param),
            "", 0, None, None)
            
class NoteBookTerminal(Gtk.Notebook):
    """
    Notebook Contenedor de Terminales.
    """
    
    __gtype_name__ = 'NoteBookTerminal'
    
    __gsignals__ = {
    "reset":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_INT, GObject.TYPE_PYOBJECT,
        GObject.TYPE_PYOBJECT))}
        
    def __init__(self):
        
        Gtk.Notebook.__init__(self)
        
        self.set_scrollable(True)
        
        #self.fuente = Pango.FontDescription("Monospace %s" % 10)
        
        self.show_all()
        
        self.connect('switch_page', self.__switch_page)
        
    def set_font(self, fuente):
        """
        Setea la fuente en las terminales.
        """
        
        #self.fuente = Pango.FontDescription(fuente)
        
        terminales = self.get_children()
        
        if not terminales: return
    
        #for terminal in terminales:
        #    terminal.re_set_font(self.fuente)
        
    def agregar_terminal(self, path = os.environ["HOME"],
        interprete = "/bin/bash", ejecutar = None):
        """
        Agrega una nueva Terminal al Notebook.
        """
        
        ### Label.
        hbox = Gtk.HBox()
        
        archivo = os.path.join(
            BASEPATH,
            "Iconos", "button-cancel.svg")
            
        boton = get_boton(archivo,
            pixels = get_pixels(Width_Button), tooltip_text = "Cerrar")
        
        text = "bash"
        
        if "bash" in interprete:
            text = "bash"
            
        elif "python" in interprete:
            text = "python"
            
        if "ipython" in interprete: text = "ipython"
            
        label = Gtk.Label(text)

        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(boton, False, False, 0)
        
        ### Area de Trabajo.
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC)
            
        terminal = Terminal(
            path=path,
            interprete=interprete,
            archivo=ejecutar)#,
            #fuente=self.fuente)
            
        scroll.add(terminal)
        
        self.append_page(scroll, hbox)

        label.show()
        
        self.show_all()
        
        boton.connect("clicked", self.__cerrar)
        terminal.connect("reset", self.__re_emit_reset)
        
        self.set_current_page(-1)
        
        return terminal
    
    def __re_emit_reset(self, terminal):
        """
        Cuando se resetea una terminal.
        """
        
        paginas = self.get_n_pages()
        
        for pag_indice in range(paginas):
            if terminal == self.get_nth_page(pag_indice):
                boton = self.get_tab_label(self.get_children()[pag_indice]).get_children()[1]
                label = self.get_tab_label(self.get_children()[pag_indice]).get_children()[0]
                break
            
        self.emit("reset", terminal, pag_indice, boton, label)
        
    def __switch_page(self, widget, widget_child, indice):
        """
        Cuando el usuario selecciona una lengüeta en el notebook.
        """
        
        widget_child.child_focus(True)
        
    def reset_terminal(self, path = os.environ["HOME"],
        interprete = "/bin/bash"):
        """
        Resetea la terminal activa, a un determinado interprete.
        """
        
        if not self.get_children():
            self.agregar_terminal(path, interprete)
            return
        
        text = "bash"
        
        if "bash" in interprete:
            text = "bash"
            
        elif "python" in interprete:
            text = "python"

        if "ipython" in interprete: text = "ipython"
        
        label = self.get_tab_label(self.get_children()[self.get_current_page()]).get_children()[0]
        label.set_text(text)
        
        terminal = self.get_children()[self.get_current_page()].get_child()
        terminal.set_interprete(path = path, interprete = interprete)
        
    def accion_terminal(self, accion):
        """
        Soporte para clipboard y agregar una terminal nueva.
        """
        
        if self.get_children():
            terminal = self.get_children()[self.get_current_page()].get_child()
            terminal.child_focus(True)
            
            if accion == 'copiar':
                if terminal.get_has_selection():
                    terminal.copy_clipboard()
                    
            elif accion == 'pegar':
                terminal.paste_clipboard()
                
            elif accion == "agregar":
                self.agregar_terminal()
            
        else:
            self.agregar_terminal()
            
            terminal = self.get_children()[self.get_current_page()].get_child()
            terminal.child_focus(True)
            
            if accion == 'copiar':
                if terminal.get_has_selection():
                    terminal.copy_clipboard()
                    
            elif accion == 'pegar':
                terminal.paste_clipboard()
        
    def __cerrar(self, widget):
        """
        Cerrar la terminal a través de su botón cerrar.
        """
        
        paginas = self.get_n_pages()
        
        for indice in range(paginas):
            boton = self.get_tab_label(self.get_children()[indice]).get_children()[1]
            
            if boton == widget:
                self.remove_page(indice)
                break
        
class Terminal(Vte.Terminal):
    """
    Terminal Configurable en distintos intérpretes.
    """
    
    __gtype_name__ = 'Terminal'
    
    __gsignals__ = {
    "reset":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
        
    def __init__(self,
        path = os.environ["HOME"],
        interprete = "/bin/bash",
        archivo = None):#,
        #fuente = Pango.FontDescription("Monospace %s" % 10)):
        
        Vte.Terminal.__init__(self)
        
        self.set_encoding('utf-8')
        #self.set_font(fuente)
        
        self.set_colors(
            Gdk.color_parse('#ffffff'),
            Gdk.color_parse('#000000'),[])
        
        self.path = path
        self.interprete = interprete
        
        self.show_all()

        self.__reset(archivo=archivo)
        
    def re_set_font(self, fuente):
        """
        Setea la fuente.
        """
        
        self.set_font(fuente)
        
    def do_child_exited(self):
        """
        Cuando se hace exit en la terminal,
        esta se resetea.
        """
        
        self.__reset()
        self.emit("reset")
        
    def set_interprete(self, path = os.environ["HOME"],
        interprete = "/bin/bash"):
        """
        Setea la terminal a un determinado interprete.
        """
        
        self.path = path
        self.interprete = interprete

        self.__reset()
        
    def __reset(self, archivo = None):
        """
        Reseteo de la Terminal.
        """
        
        if archivo:
            interprete = "/bin/bash"
            
            try:
                import mimetypes
                
                if "python" in mimetypes.guess_type(archivo)[0]:
                    interprete = "python"
                    
                    if os.path.exists(os.path.join("/bin", interprete)):
                        interprete = os.path.join("/bin", interprete)
                        
                    elif os.path.exists(os.path.join("/usr/bin", interprete)):
                        interprete = os.path.join("/usr/bin", interprete)
                        
                    elif os.path.exists(os.path.join("/sbin", interprete)):
                        interprete = os.path.join("/sbin", interprete)
                        
                    elif os.path.exists(os.path.join("/usr/local", interprete)):
                        interprete = os.path.join("/usr/local", interprete)
                        
            except:
                ### Cuando se intenta ejecutar un archivo no ejecutable.
                return self.set_interprete()
                
            path = os.path.dirname(archivo)
            
            pty_flags = Vte.PtyFlags(0)
            
            self.fork_command_full(
                pty_flags,
                path,
                (interprete,archivo),
                "", 0, None, None)
                
        else:
            interprete = self.interprete
            path = self.path
        
            pty_flags = Vte.PtyFlags(0)
            
            self.fork_command_full(
                pty_flags,
                path,
                (interprete,),
                "", 0, None, None)
        
        self.child_focus(True)

class ToolbarTerminal(Gtk.Toolbar):
    """
    Toolbar de JAMediaTerminal.
    """
    
    __gtype_name__ = 'ToolbarTerminal'
    
    __gsignals__ = {
    "accion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "reset":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "formato":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self,
            orientation = Gtk.Orientation.HORIZONTAL)
            
        ### Interpretes disponibles.
        bash_path = None
        python_path = None
        
        paths = os.environ["PATH"].split(':')
        
        for path in paths:
            if 'bash' in os.listdir(path):
                bash_path = os.path.join(path, 'bash')
                
            if 'python' in os.listdir(path):
                python_path = os.path.join(path, 'python')
                
            if bash_path and python_path: break
        
        for path in paths:
            if 'ipython' in os.listdir(path):
                python_path = os.path.join(path, 'ipython')
        
        ### Construcción.
        archivo = os.path.join(
            BASEPATH,
            "Iconos", "edit-copy.svg")
            
        boton = get_boton(archivo,
            pixels = get_pixels(Width_Button), tooltip_text = "Copiar")
        
        boton.connect("clicked", self.__emit_accion, "copiar")
        self.insert(boton, -1)
        
        archivo = os.path.join(
            BASEPATH,
            "Iconos", "editpaste.svg")
            
        boton = get_boton(archivo,
            pixels = get_pixels(Width_Button), tooltip_text = "Pegar")
        
        boton.connect("clicked", self.__emit_accion, "pegar")
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        ### Botón Formato.
        archivo = os.path.join(
            BASEPATH,
            "Iconos", "font.svg")
            
        boton = get_boton(archivo,
            pixels = get_pixels(Width_Button), tooltip_text = "Fuente")
        
        boton.connect("clicked", self.__emit_formato)
        self.insert(boton, -1)
        
        ### Botón Agregar.
        archivo = os.path.join(
            BASEPATH,
            "Iconos", "tab-new.svg")
            
        boton = get_boton(archivo,
            pixels = get_pixels(Width_Button), tooltip_text = "Nueva Terminal")
        
        boton.connect("clicked", self.__emit_accion, "agregar")
        self.insert(boton, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 10, expand = False), -1)
            
        ### Botón bash.
        archivo = os.path.join(
            BASEPATH,
            "Iconos", "bash.svg")
            
        boton = get_boton(archivo,
            pixels = get_pixels(Width_Button), tooltip_text = "Terminal bash")
        
        boton.connect("clicked", self.__emit_reset, bash_path)
        self.insert(boton, -1)
        
        ### Botón python.
        archivo = os.path.join(
            BASEPATH,
            "Iconos", "python.svg")
            
        boton = get_boton(archivo,
            pixels = get_pixels(Width_Button), tooltip_text = "Terminal python")
        
        boton.connect("clicked", self.__emit_reset, python_path)
        self.insert(boton, -1)
        
        self.show_all()
        
    def __emit_formato(self, widget):
        
        self.emit('formato')
        
    def __emit_reset(self, widget, path):
        
        self.emit('reset', path)
        
    def __emit_accion(self, widget, accion):
        
        self.emit('accion', accion)

class DialogoFormato(Gtk.Dialog):
    """
    Selector de fuente y tamaño.
    """
    
    __gtype_name__ = 'DialogoFormato'
    
    def __init__(self, parent_window = False, fuente = "Monospace", tamanio = 10):

        Gtk.Dialog.__init__(self,
            parent = parent_window,
            flags = Gtk.DialogFlags.MODAL,
            buttons = [
                "Aceptar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])
                
        self.fuente = fuente
        self.tamanio = tamanio
        
        box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        ### Lista de Fuentes.
        treeview_fuentes = TreeViewFonts(self.fuente)
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add(treeview_fuentes)
        
        box.pack_start(scroll, True, True, 0)
        
        ### Tamaños.
        treeview_tamanios = TreeViewTamanio(self.tamanio)

        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add(treeview_tamanios)
        
        box.pack_start(scroll, True, True, 0)
        
        self.vbox.pack_start(box, True, True, 0)
        
        ### Preview.
        self.preview = Gtk.Label("Texto")
        #self.preview.modify_font(
        #    Pango.FontDescription("%s %s" % (self.fuente, self.tamanio)))

        eventbox = Gtk.EventBox()
        eventbox.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))
        eventbox.add(self.preview)
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add_with_viewport(eventbox)
        
        scroll.set_size_request(-1, 100)
        
        self.vbox.pack_start(scroll, False, False, 2)
        
        self.set_size_request(400, 400)
        self.set_border_width(15)

        self.show_all()
        
        treeview_fuentes.connect("nueva-seleccion", self.__set_font)
        treeview_tamanios.connect("nueva-seleccion", self.__set_tamanio)

    def __set_font(self, widget, fuente):
        """
        Cuando se cambia la fuente.
        """
        pass
        #if self.fuente != fuente:
        #    self.fuente = fuente
        #    self.preview.modify_font(Pango.FontDescription("%s %s" % (self.fuente, self.tamanio)))
        
    def __set_tamanio(self, widget, tamanio):
        """
        Cuando se cambia el tamaño.
        """
        pass
        #if self.tamanio != tamanio:
        #    self.tamanio = tamanio
        #    self.preview.modify_font(Pango.FontDescription("%s %s" % (self.fuente, self.tamanio)))
    
    def get_font(self):
        """
        Devuelve fuente y tamaño seleccionados.
        """
        
        return (self.fuente, self.tamanio)
    
class TreeViewFonts(Gtk.TreeView):
    
    __gtype_name__ = 'TreeViewFonts'
    
    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}
    
    def __init__(self, fuente):
        
        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING))
            
        self.fuente = fuente
        
        self.__setear_columnas()
        
        treeselection = self.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.SINGLE)
        treeselection.set_select_function(self.__selecciones, self.get_model())
        
        self.show_all()
        
        GLib.idle_add(self.__init)
        
    def __setear_columnas(self):
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Fuente", Gtk.CellRendererText(), markup=0)
        columna.set_sort_column_id(0)
        columna.set_property('visible', True)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        
        self.append_column(columna)
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Nombre", Gtk.CellRendererText(), text=1)
        columna.set_sort_column_id(1)
        columna.set_property('visible', False)
        #columna.set_property('resizable', False)
        #columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        
        self.append_column(columna)
    
    def __init(self):
        
        self.get_model().clear()
        
        ### Cargar las fuentes.
        fuentes = []
        
        #for family in FAMILIES:
        #    name = family.get_name()
        #    fuentes.append(name)
            
        fuentes.sort()
        
        for fuente in fuentes:
            texto = '<span font="%s">%s</span>' % (fuente, fuente)
            self.get_model().append([texto, fuente])
            
        ### Seleccionar la fuente inicial.
        model = self.get_model()
        item = model.get_iter_first()
        
        while item:
            if model.get_value(item, 1) == self.fuente:
                self.get_selection().select_path(model.get_path(item))
                self.scroll_to_cell(model.get_path(item))
                return False
            
            item = model.iter_next(item)
        
        return False
    
    def __selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """
        
        iter = model.get_iter(path)
        fuente = model.get_value(iter, 1)
        
        if self.fuente != fuente:
            self.fuente = fuente
            self.scroll_to_cell(path)
            self.emit('nueva-seleccion', self.fuente)

        return True
        
class TreeViewTamanio(Gtk.TreeView):
    
    __gtype_name__ = 'TreeViewTamanio'
    
    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_INT, ))}
    
    def __init__(self, tamanio):
        
        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GObject.TYPE_INT))
            
        self.__setear_columnas()
        
        self.tamanio = tamanio
        
        treeselection = self.get_selection()
        treeselection.set_mode(Gtk.SelectionMode.SINGLE)
        treeselection.set_select_function(self.__selecciones, self.get_model())
        
        self.show_all()
        
        GLib.idle_add(self.__init)
        
    def __setear_columnas(self):
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Tamaño", Gtk.CellRendererText(), text=0)
        columna.set_sort_column_id(0)
        columna.set_property('visible', True)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        
        self.append_column(columna)
        
    def __init(self):
        
        self.get_model().clear()
        
        for num in range(8,21):
            self.get_model().append([num])
        
        ### Seleccionar el tamaño inicial.
        model = self.get_model()
        item = model.get_iter_first()
        
        while item:
            if model.get_value(item, 0) == self.tamanio:
                self.get_selection().select_path(model.get_path(item))
                self.scroll_to_cell(model.get_path(item))
                return False
            
            item = model.iter_next(item)
        
        return False
    
    def __selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """
        
        iter = model.get_iter(path)
        tamanio = model.get_value(iter, 0)
        
        if self.tamanio != tamanio:
            self.tamanio = tamanio
            self.scroll_to_cell(path)
            self.emit('nueva-seleccion', self.tamanio)

        return True
    
if __name__=="__main__":
    import sys
    ventana = Gtk.Window()
    ventana.add(JAMediaTerminal())
    ventana.show_all()
    ventana.connect("destroy", sys.exit)
    Gtk.main()
    