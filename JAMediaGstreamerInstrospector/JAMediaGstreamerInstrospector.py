#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import commands

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Gst

from Widgets import Toolbar
from Widgets import TextView
from Widgets import Lista

Gst.init([])

registry = Gst.Registry.get()
plugins = registry.get_plugin_list()

def get_inspect(elemento):
    """Devuelve inspect de elemento."""
    
    return commands.getoutput('gst-inspect-1.0 %s' % (elemento))

class JAMediaGstreamerInstrospector(Gtk.Plug):

    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Plug.__init__(self, 0L)
        
        self.toolbar = None
        self.textview = None
        self.lista = None
        
        self.show_all()
        
        self.connect("embedded", self.embed_event)
        
    def setup_init(self):
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbar = Toolbar()
        self.lista = Lista()
        
        panel_base = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        
        # Izquierda
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.lista)
        scroll.set_size_request(250, -1)
        
        panel_base.pack1(scroll, resize = False, shrink = False)
        
        # Derecha
        self.textview = TextView()
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.textview)
        panel_base.pack2(scroll, resize = True, shrink = True)
        
        # Todo
        vbox.pack_start(self.toolbar, False, False, 0)
        vbox.pack_start(panel_base, True, True, 0)
        
        self.add(vbox)
        
        self.show_all()
        
        self.llenar_lista()
        
        self.toolbar.connect('salir', self.salir)
        self.lista.connect('nueva-seleccion', self.get_element)
        
    def llenar_lista(self):
        
        iter = self.lista.modelo.get_iter_first()
        
        for elemento in plugins:
            
            iteractual = self.lista.modelo.append(iter, [elemento.get_name(), elemento.get_description()])
            
            features = registry.get_feature_list_by_plugin(elemento.get_name())
            
            if len(features) > 1:
                for feature in features:
                    self.lista.modelo.append(
                        iteractual,
                        [feature.get_name(),
                        elemento.get_description()])
            
    def get_element(self, widget, path):
        
        self.textview.get_buffer().set_text(get_inspect(path))
        
    def embed_event(self, widget):
        
        print "JAMediaGstreamerInstrospector OK"
        
    def salir(self, widget):
        
        self.emit('salir')
