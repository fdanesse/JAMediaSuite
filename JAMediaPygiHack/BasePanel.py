#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BasePanel.py por:
#       Flavio Danesse <fdanesse@gmail.com>, <fdanesse@activitycentral.com>
#       CeibalJAM - Uruguay - Activity Central

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
from gi.repository import WebKit

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaObjects.JAMediaTerminal import JAMediaTerminal

import JAMediaGstreamer
from JAMediaGstreamer.JAMediaGstreamer import JAMediaGstreamer

from Widgets import ToolbarTry
from ApiWidget import ApiWidget

from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_pixels

BASEPATH = os.path.dirname(__file__)

class BasePanel(Gtk.Paned):

    __gtype_name__ = 'PygiHackBasePanel'
    
    __gsignals__ = {
    "update":(GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self):

        Gtk.Paned.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.base_notebook = BaseNotebook()
        self.jamedia_gstreamer = JAMediaGstreamer()
        
        vbox.pack_start(self.base_notebook, True, True, 0)
        vbox.pack_end(self.jamedia_gstreamer, True, True, 0)
        
        self.pack1(vbox, resize = True, shrink = False)
        
        self.terminal = JAMediaTerminal()
        self.terminal.set_size_request(-1, 200)
        self.pack2(self.terminal, resize = False, shrink = False)
        
        self.show_all()
        
        self.connect("realize", self.__do_realize)
        
    def __do_realize(self, widget):
        
        self.set_accion("ver", "Terminal", True)
        self.set_accion("ver", "Apis PyGiHack", True)
        self.base_notebook.import_modulo("python-gi", "Gtk")
        
    def set_accion(self, menu, wid_lab, valor):
        
        if menu == "ver":
            if wid_lab == "Terminal":
                if valor == True:
                    self.terminal.show()
                elif valor == False:
                    self.terminal.hide()
                    
            elif wid_lab == "Gstreamer - Inspect 1.0":
                self.base_notebook.hide()
                self.jamedia_gstreamer.show()
                
            elif wid_lab == "Apis PyGiHack":
                self.jamedia_gstreamer.hide()
                self.base_notebook.show()
                
            self.emit("update", wid_lab)
            
    def import_modulo(self, paquete, modulo):
        
        self.base_notebook.import_modulo(paquete, modulo)
        
class BaseNotebook(Gtk.Notebook):

    __gtype_name__ = 'PygiHackBaseNotebook'
    
    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)
        
        self.show_all()

        #self.connect('switch_page', self.__switch_page)
        
    def import_modulo(self, paquete, modulo):
        """
        Crea una lengüeta para el módulo que se cargará.
        """
        
        if paquete == "python-gi" or paquete == "python":
            hbox = Gtk.HBox()
            label = Gtk.Label(modulo)
            
            boton = get_boton(
                os.path.join(JAMediaObjectsPath,
                "Iconos", "button-cancel.svg"),
                pixels = get_pixels(0.5),
                tooltip_text = "Cerrar")
            
            hbox.pack_start(label, False, False, 0)
            hbox.pack_start(boton, False, False, 0)

            introspectionwidget = IntrospectionWidget(paquete, modulo)
            self.append_page(introspectionwidget, hbox)
            
            label.show()
            boton.show()
            self.show_all()
            
            boton.connect("clicked", self.__cerrar)
            
            self.set_current_page(-1)
        
    def __cerrar(self, widget):
        """
        Elimina la Lengüeta.
        """
        
        paginas = self.get_n_pages()
        
        for indice in range(paginas):
            boton = self.get_tab_label(self.get_children()[indice]).get_children()[1]
            
            if boton == widget:
                self.remove_page(indice)
                return
            
class IntrospectionWidget(Gtk.Box):
    
    __gtype_name__ = 'PygiHackIntrospectionWidget'
    
    def __init__(self, paquete, modulo):
        
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        
        self.introspection_panel = IntrospectionPanel(paquete, modulo)
        self.toolbartray = ToolbarTry()
        
        self.pack_start(self.introspection_panel, True, True, 0)
        self.pack_end(self.toolbartray, False, False, 0)
        
        self.show_all()
        
        self.introspection_panel.connect('info-try', self.__set_info_tray)
        
    def __set_info_tray(self, widget, info):
        
        self.toolbartray.set_info(info)
    
class IntrospectionPanel(Gtk.Paned):

    __gtype_name__ = 'PygiHackIntrospectionPanel'

    __gsignals__ = {
    "info-try":(GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self, paquete, modulo):

        Gtk.Paned.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        
        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)

        apiwidget = ApiWidget(paquete, modulo)
        scroll.add(apiwidget)
        scroll.set_size_request(250, -1)
        self.pack1(scroll, resize = False, shrink = True)
        
        panel2 = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)

        self.infonotebook = InfoNotebook()
        self.pack2(self.infonotebook, resize = True, shrink = True)
        
        self.show_all()
        
        apiwidget.connect('update', self.__update)
    
    def __update(self, widget, tupla):
        
        if tupla:
            webdoc = ''
            objeto, gdoc, doc, _type, modulo_path, tipo = tupla
            doc = str(doc).replace("[", "").replace("]", "").replace(",", "\n").replace("u'", "").replace("'", "")
            
        else:
            self.infonotebook.set_gdoc('')
            self.infonotebook.set_doc('')
            self.infonotebook.set_webdoc('')
            
            self.emit("info-try", '')
            return
        
        self.infonotebook.set_gdoc(gdoc)
        self.infonotebook.set_doc(doc)
        
        clase = objeto.split(".")[-1]
        modulo = objeto.replace(".%s" % objeto.split(".")[-1], '')
        
        for f in os.listdir('/dev/shm'):
            if f.split(".")[-1] == 'html':
                os.remove(os.path.join('/dev/shm', f))
        
        import commands
        
        if tipo == "python-gi":
            arch0 = os.path.join(BASEPATH, "SpyderHack", "Make_gi_doc.py")
            commands.getoutput('cp %s %s' % (arch0, '/dev/shm'))
            arch = os.path.join('/dev/shm', "Make_gi_doc.py")
            
        elif tipo == "python":
            arch0 = os.path.join(BASEPATH, "SpyderHack", "Make_doc.py")
            commands.getoutput('cp %s %s' % (arch0, '/dev/shm'))
            arch = os.path.join('/dev/shm', "Make_doc.py")
            
        commands.getoutput('python %s %s %s' % (arch, modulo, clase))
        os.remove(arch)
        
        ### Porque aveces la web no tiene este nombre.
        for file in os.listdir('/dev/shm'):
            if str(file).endswith('.html'):
                archivo = os.path.realpath(os.path.join('/dev/shm', file))
                arch = open(archivo, "r")
                text = arch.read()
                arch.close()
                if text: webdoc = archivo
                
        self.infonotebook.set_webdoc(webdoc)
        
        self.emit("info-try", "%s %s %s %s" % (objeto, _type, modulo_path, tipo))
        
class InfoNotebook(Gtk.Notebook):

    __gtype_name__ = 'PygiHackInfoNotebook'
    
    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.set_tab_pos(Gtk.PositionType.RIGHT)
        
        self.set_scrollable(True)
        
        label = Gtk.Label("Web Doc")
        label.set_angle(-90)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        self.webview = WebKit.WebView()
        self.webview.set_settings(WebKit.WebSettings())
        self.webview.set_zoom_level(0.8)
        #buffer.set_text("%s-%s" % (paquete, modulo))
        scroll.add(self.webview)
        self.append_page(scroll, label)
        
        label = Gtk.Label("__gdoc__")
        label.set_angle(-90)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        self.gdoc = Gtk.TextView()
        self.gdoc.set_editable(False)
        self.gdoc.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        #buffer.set_text("%s-%s" % (paquete, modulo))
        scroll.add(self.gdoc)
        self.append_page(scroll, label)
        
        label = Gtk.Label("__doc__")
        label.set_angle(-90)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        self.doc = Gtk.TextView()
        self.doc.set_editable(False)
        self.doc.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        #buffer.set_text("%s-%s" % (paquete, modulo))
        scroll.add(self.doc)
        self.append_page(scroll, label)
        
        self.show_all()
        
    def set_webdoc(self, webdoc):
        self.webview.open(webdoc)

    def set_gdoc(self, gdoc):
        self.gdoc.get_buffer().set_text(gdoc)
    
    def set_doc(self, doc):
        self.doc.get_buffer().set_text(doc)
        