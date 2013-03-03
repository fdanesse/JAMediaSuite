#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import commands

import gi
gi.require_version('Gst', '1.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Gst
from gi.repository import Vte

#from Widgets import Toolbar
from Widgets import TextView
from Widgets import Lista

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir
from JAMediaObjects.JAMediaWidgets import JAMediaTerminal

JAMediaObjectsPath = JAMediaObjects.__path__[0]

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMediaEstilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()
context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    
GObject.threads_init()
Gdk.threads_init()

Gst.init([])

registry = Gst.Registry.get()
plugins = registry.get_plugin_list()

def get_inspect(elemento):
    """Devuelve inspect de elemento."""
    
    return commands.getoutput('gst-inspect-1.0 %s' % (elemento))

class JAMediaGstreamer(Gtk.Plug):

    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Plug.__init__(self, 0L)
        
        self.toolbar = None
        self.toolbar_salir = None
        self.textview = None
        self.lista = None
        
        self.show_all()
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        #self.toolbar = Toolbar()
        #self.toolbar_salir = ToolbarSalir()
        self.lista = Lista()
        
        panel_base = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        
        # Izquierda
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add_with_viewport(self.lista)
        scroll.set_size_request(250, -1)
        
        panel_base.pack1(
            scroll,
            resize = False,
            shrink = False)
        
        # Derecha
        panel = Gtk.Paned(orientation = Gtk.Orientation.VERTICAL)
        panel_base.pack2(
            panel,
            resize = True,
            shrink = True)
        
        self.textview = TextView()
        scroll = Gtk.ScrolledWindow()
        
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        scroll.add_with_viewport(self.textview)
        panel.pack1(
            scroll,
            resize = True,
            shrink = True)
        
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_size_request(-1, 150)
        
        scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
            
        self.terminal = JAMediaTerminal()
        
        scrolled_window.add_with_viewport(self.terminal)
        
        panel.pack2(
            scrolled_window,
            resize = False,
            shrink = False)
        
        # Todo
        #vbox.pack_start(self.toolbar, False, False, 0)
        #vbox.pack_start(self.toolbar_salir, False, False, 0)
        vbox.pack_start(panel_base, True, True, 0)
        
        self.add(vbox)
        
        self.show_all()
        
        #self.toolbar_salir.hide()
        
        self.llenar_lista()
        
        self.connect("embedded", self.embed_event)
        #self.toolbar.connect('salir', self.confirmar_salir)
        #self.toolbar_salir.connect('salir', self.emit_salir)
        self.lista.connect('nueva-seleccion', self.get_element)
        
    #def emit_salir(self, widget):
        
    #    self.emit('salir')
        
    #def confirmar_salir(self, widget = None, senial = None):
        
    #    self.toolbar_salir.run("JAMediaGstreamer")
        
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
        
        print "JAMediaGstreamer OK"
