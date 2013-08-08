#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
#
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

# http://www.roojs.org/index.php/projects/gnome/introspection-docs.html
# http://www.roojs.org/seed/gir-1.1-gtk-2.0/
# http://www.roojs.com/seed/gir-1.2-gtk-3.0/seed/
# https://github.com/roojs/gir-1.2-gtk-2.0
# https://github.com/roojs/gir-1.2-gtk-3.0
# https://github.com/roojs/gir-1.2-gtk-3.4

import os

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects

from JAMediaObjects.JAMediaGlobales import get_separador

JAMediaObjectsPath = JAMediaObjects.__path__[0]

DATOS = os.path.join(os.environ["HOME"], "Datos-pygi-hack")

if not os.path.exists(DATOS):
    os.mkdir(DATOS)
    os.chmod(DATOS, 0755)

import Funciones as FUNC

class ToolbarTry(Gtk.Toolbar):
    """
    Barra de estado.
    """
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.show_all()
        
class Navegador(Gtk.Paned):
    """
    Panel con:
        Lista de Paquetes.
        Lista de Módulos en paquete Seleccionado.
        Visor WebKit para el doc generado sobre el módulo seleccionado.
        Terminal bash-python para pruebas.
    """
    
    __gsignals__ = {
    "info":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
        
    def __init__(self):
        
        Gtk.Paned.__init__(
            self, orientation = Gtk.Orientation.HORIZONTAL)
        
        self.api = None
        self.webview = None
        self.lista_modulos = None
        
        self.pack1(
            self.__area_izquierda_del_panel(),
            resize = False, shrink = True)
            
        self.pack2(
            self.__area_derecha_del_panel(),
            resize = True, shrink = True)
        
        self.show_all()

        self.webview.set_zoom_level(0.8)
        
        self.lista_modulos.connect('nueva-seleccion', self.__set_api)
        
        self.api.connect('objeto', self.__ver_objeto)
        self.api.connect('info', self.__re_emit_info)
    
        self.set_default_api()
        
    def set_default_api(self):
        """
        Establece Gtk como el api seleccionada por defecto.
        """
        
        model = self.lista_modulos.get_model()
        iter = model.get_iter_first()
        
        while iter:
            if model.get_value(iter, 0) == "Gtk":
                self.lista_modulos.treeselection.select_iter(iter)
                return
            
            iter = model.iter_next(iter)
            
    def __re_emit_info(self, widget, info):
        """
        Emite información para la barra de estado.
        """
        
        self.emit('info', info)
        
    def __ver_objeto(self, widget, objeto):
        """
        Recibe la clase, funcion o constante a cargar,
        del tipo:
            <class 'gi.repository.Atk.Action'>
            
        Y genera el Doc correspondiente.
        """
        
        os.chdir(DATOS)
        
        try:
            if objeto:
                archivo = os.path.join(DATOS, '%s.html' % (objeto.__name__))
                
                import pydoc
                
                pydoc.writedoc(objeto)
                self.webview.open(archivo)
                # http://nullege.com/codes/show/src@g@n@gnome-bubbles-HEAD@bubble.py/67/webkit.WebView.open
                # http://nullege.com/codes/show/src@t@u@Turpial-HEAD@turpial@ui@gtk@tweetslistwk.py/45/webkit.WebView.set_settings
                
            else:
                self.webview.open('')
                
        except:
            self.webview.open('')
            
        while Gtk.events_pending():
            Gtk.main_iteration()
        
    def __area_izquierda_del_panel(self):
        """
        Empaqueta las listas de la izquierda.
        """
        
        panel = Gtk.Paned(orientation = Gtk.Orientation.VERTICAL)
        
        scrolled_window = Gtk.ScrolledWindow()
        
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        
        scrolled_window.set_size_request(250, -1)
        
        self.lista_modulos = Lista()
        
        modulos = FUNC.get_modulos()
        
        iter = self.lista_modulos.modelo.get_iter_first()
        
        for elemento in modulos:
            iteractual = self.lista_modulos.modelo.append(iter, [elemento])
        
        scrolled_window.add_with_viewport (self.lista_modulos)
        
        panel.pack1(
            scrolled_window,
            resize = False,
            shrink = True)
        
        scrolled_window = Gtk.ScrolledWindow()
        
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        self.api = Api()
        scrolled_window.add_with_viewport (self.api)
        
        panel.pack2(
            scrolled_window,
            resize = False,
            shrink = True)
        
        return panel

    def __area_derecha_del_panel(self):
        """
        Empaqueta el visor webkit.
        """

        from gi.repository import WebKit
        
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        self.webview = WebKit.WebView()
        self.webview.set_settings(WebKit.WebSettings())
        
        scroll.add_with_viewport(self.webview)
        
        return scroll
    
    def __set_api(self, widget, valor):
        """
        Setea la lista de clases, funciones y constantes
        para el paquete cargado.
        
        Por ejemplo:
            Para Gtk:
                Listar:
                    Window
                    Widget
                    etc . . .
        """
        
        self.api.llenar(valor)
        
class Api(Gtk.TreeView):
    """
    TreeView para mostrar:
        Clases, Funciones, Constantes y Otros items del modulo.
    """
    
    __gsignals__ = {
    "objeto":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
    "info":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self)
        
        self.set_property("enable-grid-lines", True)
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        
        self.objetos = {}
        self.modulo = None
        self.objeto = None
        
        self.modelo = Gtk.TreeStore(
            GdkPixbuf.Pixbuf,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING)
            
        self.__construir_columnas()
        
        self.connect("row-activated", self.__activar, None)
        
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.TOUCH_MASK)
            
        self.connect("key-press-event", self.__keypress)
        
        self.set_model(self.modelo)
        
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.__selecciones, self.modelo)
        
        self.show_all()
    
    def __keypress(self, widget, event):
        """
        Cuando se presiona una tecla.
        """
        
        tecla = event.get_keycode()[1]
        model, iter = self.treeselection.get_selected()
        path = self.modelo.get_path(iter)
        
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
                
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
                
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        
        return False
    
    def __activar (self, treeview, path, view_column, user_param1):
        """
        Cuando se hace doble click en "Clases", "Funciones", etc . . .
        """
        
        iter = treeview.modelo.get_iter(path)
        valor = treeview.modelo.get_value(iter, 1)
        
        if treeview.row_expanded(path):
            treeview.collapse_row(path)
            
        elif not treeview.row_expanded(path):
            treeview.expand_to_path(path)

    def __selecciones(self, treeselection, modelo, path, is_selected, treestore):
        """
        Cuando se selecciona una clase, funcion, etc . . .
        """
        
        iter = modelo.get_iter(path)
        modulo =  modelo.get_value(iter, 2)
        valor = modelo.get_value(iter, 1)
        objeto = None
        
        if not is_selected and modulo != self.modulo:
            self.modulo = modulo
            #self.emit('info', self.modulo)
            
        try:
            objeto = self.objetos[valor]
            
        except:
            pass
        
        if objeto and objeto != self.objeto and not is_selected:
            self.objeto = objeto
            self.emit('objeto', self.objeto)
            
        return True
    
    def llenar(self, paquete):
        """
        Llena el treeview con los datos de un paquete.
        (Clases, funciones, constantes y otros.)
        """
        
        modulo, CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS = FUNC.get_info(paquete)
        
        if not modulo or modulo == None:
            self.emit('objeto', False)
            self.emit('info', "%s %s" % (modulo, paquete))
            
            return False
            
        self.objetos = {}
        self.objeto = None
        
        self.modelo.clear()
        
        from JAMediaObjects.JAMFileSystem import borrar
        
        for archivo in os.listdir(DATOS):
            borrar(os.path.join(DATOS, archivo))
        
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "ver.png")
        pixbufver = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "clase.png")
        pixbufclase = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "funcion.png")
        pixbuffunc = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "constante.png")
        pixbufconst = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        icono = os.path.join(JAMediaObjectsPath, "Iconos", "otros.png")
        pixbufotros = GdkPixbuf.Pixbuf.new_from_file_at_size(icono, -1, 18)
        
        iter = self.modelo.get_iter_first()
        
        iteractual = self.modelo.append(iter,[ pixbufver, paquete, str(modulo), ""])
        iterclass = self.modelo.append(iteractual,[ pixbufclase, 'Clases', str(modulo), ""])
        iterfunc = self.modelo.append(iteractual,[ pixbuffunc, 'Funciones', str(modulo), ""])
        iterconst = self.modelo.append(iteractual,[ pixbufconst, 'Constantes', str(modulo), ""])
        iterotros = self.modelo.append(iteractual,[ pixbufotros, 'Otros', str(modulo), ""])
        
        for clase in CLASES:
            self.modelo.append(iterclass,[ pixbufclase, clase[0], str(modulo), ""])
            self.objetos[clase[0]] = clase[1]
            
        for funcion in FUNCIONES:
            self.modelo.append(iterfunc,[ pixbuffunc, funcion[0], str(modulo), ""])
            self.objetos[funcion[0]] = funcion[1]
            
        for const in CONSTANTES:
            self.modelo.append(iterconst,[ pixbufconst, const[0], str(modulo), ""])
            self.objetos[const[0]] = const[1]
            
        for otros in DESCONOCIDOS:
            self.modelo.append(iterotros,[ pixbufotros, otros, str(modulo), ""])
            self.objetos[otros[0]] = otros[1]
        
        self.emit('info', "%s" % (modulo))
        
    def __construir_columnas(self):
        
        celda_de_imagen = Gtk.CellRendererPixbuf()
        columna = Gtk.TreeViewColumn(None, celda_de_imagen, pixbuf=0)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Objeto', celda_de_texto, text=1)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)

        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Modulo', celda_de_texto, text=2)
        columna.set_property('resizable', True)
        columna.set_property('visible', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
        celda_de_texto = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Reserva2', celda_de_texto, text=3)
        columna.set_property('resizable', True)
        columna.set_property('visible', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column (columna)
        
class Lista(Gtk.TreeView):
    """
    Lista de paquetes:
        Gtk, GdK, GOBject, etc . . .
    """
    
    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self)
        
        self.set_property("rules-hint", True)
        self.set_property("enable-grid-lines", True)
        self.set_property("enable-tree-lines", True)
        
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.valor_select = False
        
        self.modelo = Gtk.TreeStore(GObject.TYPE_STRING)
        
        self.__setear_columnas()
        
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.__selecciones, self.modelo)
        
        self.set_model(self.modelo)
        
        self.show_all()
        
    def __setear_columnas(self):
        
        self.append_column(self.__construir_columa('Modulos', 0, True))
        
    def __construir_columa(self, text, index, visible):
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text = index)
        
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        
        return columna
    
    def __selecciones(self, treeselection, model, path, is_selected, listore):
        """
        Cuando se selecciona un item en la lista.
        """
        
        # model y listore son ==
        iter = model.get_iter(path)
        valor = model.get_value(iter, 0)
        
        if not is_selected and self.valor_select != valor:
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)
            
        return True
    