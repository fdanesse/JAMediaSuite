#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@activitycentral.com>
#   CeibalJAM - Uruguay - Activity Central
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
import pydoc

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import WebKit

import JAMediaObjects
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

DATOS = os.path.join(os.environ["HOME"], "Datos-pygi-hack")

if not os.path.exists(DATOS):
    os.mkdir(DATOS)
    os.chmod(DATOS, 0755)
    
# http://www.roojs.org/seed/gir-1.1-gtk-2.0/
PaquetesObjetos1 = ['Atk', 'Avahi', 'Clutter', 'ClutterJson',
'DBusGLib', 'Epiphany', 'Everything', 'GConf',
'GIMarshallingTests' 'GIRepository', 'GLib', 'GObject',
'GSSDP', 'GUPnP', 'Gda', 'Gdaui', 'Gdk', 'GdkPixbuf',
'Gio', 'Gladeui', 'GnomeVFS', 'GooCanvas', 'Gsf', 'Gst',
'GstApp', 'GstAudio', 'GstBase', 'GstController',
'GstInterfaces', 'GstNet', 'GstRtp', 'GstTag', 'GstVideo',
'Gtk', 'GtkClutter', 'GtkSource', 'Midgard', 'Notify',
'PanelApplet', 'Pango', 'PangoCairo', 'PangoFT2',
'PangoXft', 'Peas', 'PeasUI', 'Polkit', 'Poppler',
'Soup', 'SoupGNOME', 'TelepathyGLib', 'Unique',
'Vte', 'WebKit']
PaquetesNoObjetos1 = ['AvahiCore', 'Babl', 'Cogl', 'DBus',
'GL', 'GMenu', 'GModule', 'GnomeKeyring', 'GstCheck',
'GstFft', 'GstNetbuffer', 'GstPbutils', 'GstRiff',
'GstRtsp', 'GstSdp', 'Gtop', 'JSCore', 'PangoX', 'cairo',
'fontconfig', 'freetype2', 'libbonobo', 'libc',
'libxml2', 'sqlite3', 'xfixes', 'xft', 'xlib', 'xrandr']

# http://www.roojs.com/seed/gir-1.2-gtk-3.0/seed/
PaquetesObjetos2 = [
'AccountsService', 'Atk', 'Cally', 'Champlain', 'Clutter',
'ClutterGst', 'ClutterX11', 'DBusGLib', 'Dbusmenu',
'Dee', 'EvinceDocument', 'Wnck', 'Totem', 'Abi',
'EvinceView', 'GConf', 'GIRepository', 'GLib', 'GObject',
'GWeather', 'Gdk', 'GdkPixbuf', 'GdkX11', 'Gio', 'Gkbd',
'GnomeBluetooth', 'Gtk', 'GtkChamplain', 'GtkClutter',
'GtkSource', 'Gucharmap', 'Json', 'MPID', 'Nautilus',
'Notify', 'Pango', 'PangoCairo', 'PangoFT2', 'PangoXft',
'Peas', 'PeasGtk', 'Polkit', 'PolkitAgent', 'Soup',
'SoupGNOME', 'TelepathyGLib', 'TelepathyLogger',
'UPowerGlib', 'Vte', 'WebKit', 'GES', 'NetworkManager',
'Rsvg', 'SugarExt', 'Cheese']
# GES : http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-editing-services/html/
PaquetesNoObjetos2 = [
'Cogl', 'DBus', 'GL', 'GMenu', 'GModule',
'JSCore', 'cairo', 'fontconfig', 'freetype2',
'libxml2', 'xfixes', 'xft', 'xlib', 'xrandr']

import Funciones as FUNC

class ToolbarTry(Gtk.Toolbar):
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.show_all()

class Toolbar(Gtk.Toolbar):
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos", "ver.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
            
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","ceibaljam.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","uruguay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","licencia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("fdanesse@gmail.com")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos","salir.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        self.show_all()
        
    def salir(self, widget):
        
        self.emit('salir')
        
class Navegador(Gtk.HPaned):
    
    __gsignals__ = {
    "info":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
        
    def __init__(self):
        
        Gtk.HPaned.__init__(self)
        
        self.api = None
        self.descriptor = None
        
        self.pack1(
            self.area_izquierda_del_panel(),
            resize = False, shrink = True)
            
        self.pack2(
            self.area_derecha_del_panel(),
            resize = True, shrink = True)
        
        self.show_all()

        self.api.connect('objeto', self.ver_objeto)
        self.api.connect('info', self.re_emit_info)
    
    def re_emit_info(self, widget, objeto):
        
        self.emit('info', objeto)
        
    def ver_objeto(self, widget, objeto):
        
        os.chdir(DATOS)
        
        try:
            if objeto:
                pydoc.writedoc(objeto)
                archivo = os.path.join(DATOS, '%s.html' % (objeto.__name__))
                self.descriptor.open(archivo)
                
            else:
                self.descriptor.open('')
                
        except:
            self.descriptor.open('')
        
    def area_izquierda_del_panel(self):
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        frame = Gtk.Frame()
        frame.set_label("Objects")
        frame.set_label_align(0.5, 0.5)
        combo = Gtk.ComboBoxText()
        
        for item in PaquetesObjetos1:
            combo.append_text(item)
            
        combo.connect('changed', self.get_item)
        frame.add(combo)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("No Objects")
        frame.set_label_align(0.5, 0.5)
        combo2 = Gtk.ComboBoxText()
        
        for item in PaquetesNoObjetos1:
            combo2.append_text(item)
            
        combo2.connect('changed', self.get_item)
        frame.add(combo2)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("gir-1.1-gtk-2.0")
        frame.set_label_align(0.5, 0.5)
        frame.add(hbox)
        vbox.pack_start(frame, False, False, 0)
        
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        
        frame = Gtk.Frame()
        frame.set_label("Objects")
        frame.set_label_align(0.5, 0.5)
        combo = Gtk.ComboBoxText()
        
        for item in PaquetesObjetos2:
            combo.append_text(item)
            
        combo.connect('changed', self.get_item)
        frame.add(combo)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("No Objects")
        frame.set_label_align(0.5, 0.5)
        combo2 = Gtk.ComboBoxText()
        
        for item in PaquetesNoObjetos2:
            combo2.append_text(item)
            
        combo2.connect('changed', self.get_item)
        frame.add(combo2)
        hbox.pack_start(frame, True, True, 2)
        
        frame = Gtk.Frame()
        frame.set_label("gir-1.2-gtk-3.0")
        frame.set_label_align(0.5, 0.5)
        frame.add(hbox)
        vbox.pack_start(frame, False, False, 0)
        
        scrolled_window = Gtk.ScrolledWindow()
        
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        self.api = Api()
        scrolled_window.add_with_viewport (self.api)
        vbox.pack_start(scrolled_window, True, True, 0)
        
        combo.set_active(0)
        
        return vbox

    def area_derecha_del_panel(self):
        
        scrolled_window = Gtk.ScrolledWindow()
        
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        self.descriptor = WebKit.WebView()
        scrolled_window.add_with_viewport(self.descriptor)
        
        return scrolled_window
    
    def get_item(self, widget):
        
        self.api.llenar( [widget.get_active_text()] )
        
class Api(Gtk.TreeView):
    """TreeView para mostrar:
    Clases, Funciones, Constantes y Otros items del modulo."""
    
    __gsignals__ = {
    "objeto":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "info":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self)
        
        self.set_property("enable-grid-lines", True)
        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        
        self.objetos = {}
        self.modulo = None
        self.objeto = None
        
        self.modelo = TreeStoreModelAPI()
        self.construir_columnas()
        
        self.connect("row-activated", self.activar, None)
        
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.TOUCH_MASK)
            
        self.connect("key-press-event", self.keypress)
        
        self.set_model(self.modelo)
        
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.selecciones, self.modelo)
        
        self.show_all()
    
    def keypress(self, widget, event):
        """Cuando se presiona una tecla."""
        
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
    
    def activar (self, treeview, path, view_column, user_param1):
        """Cuando se hace doble click en "Clases", "Funciones", etc . . ."""
        
        iter = treeview.modelo.get_iter(path)
        valor = treeview.modelo.get_value(iter, 1)
        objeto = None
        
        try:
            objeto = self.objetos[valor]
            
        except:
            pass
        
        if treeview.row_expanded(path):
            treeview.collapse_row(path)
            
        elif not treeview.row_expanded(path):
            treeview.expand_to_path(path)

    def selecciones(self, treeselection, modelo, path, is_selected, treestore):
        """Cuando se selecciona una clase, funcion, etc . . ."""
        
        iter = modelo.get_iter(path)
        modulo =  modelo.get_value(iter, 2)
        valor = modelo.get_value(iter, 1)
        objeto = None
        
        if not is_selected and modulo != self.modulo:
            self.modulo = modulo
            self.emit('info', self.modulo )
            
        try:
            objeto = self.objetos[valor]
            
        except:
            pass
        
        if objeto and objeto != self.objeto and not is_selected:
            self.objeto = objeto
            self.emit('objeto', self.objeto)
            
        return True
    
    def llenar(self, paquetes):
        """Llena el treeview con los datos de un modulo."""
        
        self.modelo.clear()
        
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
        for paq in paquetes:
            modulo, CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS = FUNC.get_info(paq)
            
            if not modulo or not CLASES:
                self.emit('objeto', None)
                self.emit('info', "El Objeto %s no se ha Podido Localizar."  % (paq))
                return
                
            iteractual = self.modelo.append(iter,[ pixbufver, paq, str(modulo), ""])
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
                
            self.emit('info', "El Objeto %s se ha Cargado Correctamente."  % (paq))
                
    def construir_columnas(self):
        
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
        
class TreeStoreModelAPI(Gtk.TreeStore):
    
    def __init__(self):
        
        Gtk.TreeStore.__init__(
            self, GdkPixbuf.Pixbuf,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING)
        