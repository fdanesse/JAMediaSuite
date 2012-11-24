#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import commands

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

def get_inspect(elemento):
    """Devuelve inspect de elemento."""
    
    return commands.getoutput('gst-inspect-1.0 %s' % (elemento))

def get_gst_elements():
    """Devulve la lista de elementos
    Gstreamer instalados en el sistema."""
    
    returndata = []
    
    inspect = commands.getoutput('gst-inspect-1.0')
    elementos = inspect.split('\n')
    
    for elemento in elementos:
        partes = elemento.split(':')
        
        if len(partes) == 5:
            returndata.append(partes)
            
        else:
            while len(partes) < 5:
                partes.append('')
            returndata.append(partes)
            
    return returndata

def get_video_filters():
    """Devuelve la lista de nombres de efectos
    de video instalados en el sistema.
    
    No se utiliza en ninguna aplicación."""
    
    efectos = []
    
    for elemento in get_gst_elements():
        
        try:
            datos = get_inspect(elemento[1])
            
            if 'gst-plugins-good' in datos and \
                ('Filter/Effect/Video' in datos or 'Transform/Effect/Video' in datos):
                print "Agregar:", elemento[1]
                efectos.append(elemento[1])
                
        except:
            print "Error:", elemento[1]
            
    return efectos

class Ventana(Gtk.Window):
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMedia Gstreamer Introspector.")
        #self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
        #    "Iconos", "JAMedia.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        hpanel = Gtk.HPaned()
        self.lista = Lista()
        self.textview = TextView()
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport (self.textview)
        
        hpanel.pack1(scroll, resize = True, shrink = True)
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport (self.lista)
        
        hpanel.pack2(scroll, resize = True, shrink = True)
        
        self.add(hpanel)
        
        self.show_all()
        self.realize()
        
        self.lista.connect('nueva-seleccion', self.get_element)
        self.connect("destroy", self.salir)
        
        for elemento in get_gst_elements():
            try:
                self.lista.modelo.append(elemento)
            except:
                print "Error:", elemento
        
    def salir(self, widget = None, senial = None):
        
        sys.exit(0)
        
    def get_element(self, widget, path):
        
        self.textview.get_buffer().set_text(get_inspect(path))

class Lista(Gtk.TreeView):
    
    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self)
        
        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.valor_select = None
        
        self.modelo = Gtk.ListStore(
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING,
            GObject.TYPE_STRING)
            
        self.setear_columnas()
        
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.selecciones, self.modelo)
        
        self.set_model(self.modelo)
        self.show_all()
        
    def setear_columnas(self):
        
        self.append_column(self.construir_columa('Elemento', 1, True))
        self.append_column(self.construir_columa('Descripción', 2, True))
        self.append_column(self.construir_columa('Paquete', 0, True))
        self.append_column(self.construir_columa('Otros', 3, True))
        
    def construir_columa(self, text, index, visible):
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna
    
    def selecciones(self, treeselection, model, path, is_selected, listore):
        """Cuando se selecciona un item en la lista."""
        
        # model y listore son ==
        iter = model.get_iter(path)
        valor =  model.get_value(iter, 1)
        
        if not is_selected and self.valor_select != valor:
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)
            
        return True
        
class TextView(Gtk.TextView):
    
    def __init__(self):
        
        Gtk.TextView.__init__(self)
        
        self.set_editable(False)
        self.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        
        self.set_buffer(Gtk.TextBuffer())
        
        self.show_all()
        
if __name__ == "__main__":
    
    Ventana()
    Gtk.main()
    