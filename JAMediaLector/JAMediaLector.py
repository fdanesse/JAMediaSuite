#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaLector.py por:
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

# https://github.com/mfenniak/pyPdf
# http://stackoverflow.com/questions/8942604/embed-evince-python-gi/9067463#9067463
# http://stackoverflow.com/questions/9682297/displaying-pdf-files-with-python3
# https://launchpad.net/poppler-python
# http://www.roojs.org/seed/gir-1.1-gtk-2.0/Poppler.Page.html
# http://hackage.haskell.org/packages/archive/poppler/0.12.1/doc/html/Graphics-UI-Gtk-Poppler-Page.html

import os
import sys
#import threading

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import Poppler

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir
import JAMediaObjects.JAMFileSystem as JAMF
import JAMediaObjects.JAMediaGlobales as G

from Widgets import Toolbar
from Widgets import ToolbarConfig
from Widgets import ToolbarLector
from Widgets import ToolbarTry
from Widgets import Drawing
from Widgets import ToolbarPaginas
from Widgets import PreviewContainer
from Widgets import Selector_de_Archivos
from Widgets import TextView

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class JAMediaLector(Gtk.Plug):
    """JAMediaLector:
        Lector pdf y de archivos de texto.
            
        Implementado sobre:
            python 2.7.3 y Gtk 3
        
        Es un Gtk.Plug para embeber en cualquier contenedor
        dentro de otra aplicacion.
        
    Para ello, es necesario crear en la aplicacion donde
    será enbebido JAMediaLector, un socket:
        
    import JAMediaLector
    from JAMediaLector.JAMediaLector import JAMediaLector
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamedialector = JAMediaLector()
        socket.add_id(self.jamedialector.get_id()
        
    y luego proceder de la siguiente forma:
        
            GObject.idle_add(self.setup_init)
        
        def setup_init(self):
            self.jamedialector.setup_init()
            # self.jamediaplayer.pack_standar()
            # Esta última linea no debe ir cuando se embebe
            
    NOTA: Tambien se puede ejecutar JAMediaLector directamente
    mediante python JAMediaLector.py
    """
    
    __gsignals__ = {"salir":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """JAMediaLector: Gtk.Plug para embeber en otra aplicación."""
        
        Gtk.Plug.__init__(self, 0L)
        
        self.toolbar = None
        self.toolbar_config = None
        self.toolballector = None
        self.toolbartray = None
        self.visor = None
        self.previewcontainer = None
        self.toolbarpaginas = None
        self.textview = None
        self.toolbar_salir = None
        
        self.controlespdf = None
        self.controlestexto = None
        self.controles_dinamicos = None
        
        self.documento = None
        self.npaginas = None
        self.indexpaginaactiva = None
        self.pagina = None
        
        self.show_all()
        
        self.connect("embedded", self.embed_event)
        
    def setup_init(self):
        """Se crea la interfaz grafica, se setea todo y
        se empaqueta todo."""
        
        basebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        hpanel = Gtk.HPaned()
        self.toolbar = Toolbar()
        self.toolbar_salir = ToolbarSalir()
        self.toolbar_config = ToolbarConfig()
        self.toolbarlector = ToolbarLector()
        self.toolbartry = ToolbarTry()
        self.visor = Drawing()
        self.previewcontainer = PreviewContainer()
        self.toolbarpaginas = ToolbarPaginas()
        self.textview = TextView()
        
        # Izquierda
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport (self.visor)
        vbox.pack_start(self.toolbarlector, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)
        
        self.controlespdf = [self.toolbarlector, scroll]
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport (self.textview)
        vbox.pack_start(scroll, True, True, 0)
        
        self.controlestexto = [scroll]
        
        hpanel.pack1(vbox, resize = True, shrink = True)
        
        # Derecha
        ev_box = Gtk.EventBox() # Para poder pintarlo
        ev_box.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport (self.previewcontainer)
        vbox.pack_start(self.toolbarpaginas, False, False, 0)
        vbox.pack_start(scroll, True, True, 0)
        ev_box.add(vbox)
        
        self.controlespdf.append(ev_box)
        
        hpanel.pack2(ev_box, resize = False, shrink = False)
        
        basebox.pack_start(self.toolbar, False, False, 0)
        basebox.pack_start(self.toolbar_salir, False, False, 0)
        basebox.pack_start(self.toolbar_config, False, False, 0)
        basebox.pack_start(hpanel, True, True, 0)
        basebox.pack_start(self.toolbartry, False, False, 0)
        
        self.controles_dinamicos = [
            self.toolbar,
            self.toolbarlector,
            ev_box,
            self.toolbartry]
        
        self.add(basebox)
        self.show_all()
        
        self.toolbar_salir.hide()
        self.toolbar.abrir.hide() # Solo cuando no esta embebido
        self.toolbar_config.hide()
        
        self.toolbarlector.connect('original', self.visor.original)
        self.toolbarlector.connect('alejar', self.visor.alejar)
        self.toolbarlector.connect('acercar', self.visor.acercar)
        #self.toolbarlector.connect('rotar_izquierda', self.visor.acercar)
        #self.toolbarlector.connect('rotar_derecha', self.visor.acercar)
        
        self.toolbarpaginas.connect('activar', self.activar)
        
        self.previewcontainer.connect('nueva_seleccion', self.nueva_pagina)
        
        self.visor.connect("ocultar_controles", self.ocultar_controles)
        self.visor.connect("button_press_event", self.clicks_en_pantalla)
        
        self.toolbar.connect('abrir', self.show_filechooser)
        self.toolbar.connect('config', self.mostrar_config)
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar_salir.connect('salir', self.emit_salir)
        
        map(self.ocultar, self.controlestexto)
        map(self.ocultar, self.controlespdf)
        
    def pack_standar(self):
        """Para empaquetar el botón abrir."""
        
        self.toolbar.abrir.show()
        
    def mostrar_config(self, widget):
        """Muestra u oculta las opciones de
        configuracion (toolbar_config)."""
        
        if self.toolbar_config.get_visible():
            self.toolbar_config.hide()
        else:
            self.toolbar_config.show_all()
            
    def clicks_en_pantalla(self, widget, event):
        """Hace fullscreen y unfullscreen sobre la
        ventana principal cuando el usuario hace
        doble click en el visor."""
        
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w,h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            if ww == w and hh == h:
                ventana.unfullscreen()
            else:
                ventana.fullscreen()
                
    def ocultar_controles(self, widget, valor):
        """Oculta o muestra los controles."""
        
        if valor and self.toolbar_config.ocultar_controles:
            map(self.ocultar, self.controles_dinamicos)
            map(self.ocultar, [self.toolbar_config, self.toolbar_salir])
        elif not valor:
            map(self.mostrar, self.controles_dinamicos)
            
    def ocultar(self, objeto):
        """Esta funcion es llamada desde self.ocultar_controles()"""
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        """Esta funcion es llamada desde self.ocultar_controles()"""
        
        if not objeto.get_visible(): objeto.show()
        
    def show_filechooser(self, widget):
        selector = Selector_de_Archivos(self)
        selector.connect('archivos-seleccionados', self.cargar_archivo)

    def cargar_archivo(self, widget, archivo):
        """Recibe un archivo desde el filechooser
        para abrir en el lector."""
        
        self.abrir( archivo)
    
    def limpiar(self):
        self.toolbartry.label.set_text("")
        self.documento = None
        self.previewcontainer.limpiar()
        self.load_pagina(None)
        self.textview.get_buffer().set_text("")
        map(self.ocultar, self.controlestexto)
        map(self.ocultar, self.controlespdf)
        
    def abrir(self, archivo):
        """Abre un Archivo."""
        
        descripcion = JAMF.describe_uri(archivo)
        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = JAMF.describe_archivo(archivo)
                if 'pdf' in tipo:
                    self.toolbartry.label.set_text(archivo)
                    archivo = "file://%s" % (archivo)
                    
                    map(self.ocultar, self.controlestexto)
                    map(self.mostrar, self.controlespdf)
                    
                    self.documento = Poppler.Document.new_from_file(archivo, None)
                    self.npaginas = self.documento.get_n_pages()
                    #thread = threading.Thread( target=self.llenar_preview )
                    #thread.start()
                    self.previewcontainer.llenar(self.documento)
                    
                elif 'text' in tipo:
                    self.toolbartry.label.set_text(archivo)
                    
                    map(self.ocultar, self.controlespdf)
                    map(self.mostrar, self.controlestexto)
                    
                    arch = open(archivo, "r")
                    lineas = arch.readlines()
                    arch.close()
                    
                    texto = ""
                    for linea in lineas:
                        texto += linea
                    self.textview.get_buffer().set_text(texto)
                    
                else:
                    self.toolbartry.label.set_text("")
                    self.documento = None
                    self.previewcontainer.limpiar()
                    self.load_pagina(None)
                    self.textview.get_buffer().set_text("")
    
    #def llenar_preview(self):
    #    """ Thread para cargar las páginas en preview. """
    #    self.previewcontainer.llenar(self.documento)

    def nueva_pagina(self, widget, indice):
        """Cuando se selecciona una nueva pagina"""
        
        self.load_pagina(indice)
        
    def load_pagina(self, indice):
        """Carga una página del Archivo pdf abierto actualmente."""
        
        if indice != None:
            self.indexpaginaactiva = indice
            self.pagina = self.documento.get_page(self.indexpaginaactiva)
            self.visor.set_pagina(self.pagina)
            self.toolbarpaginas.set_pagina(self.indexpaginaactiva+1, self.npaginas)
        else:
            self.indexpaginaactiva = None
            self.pagina = None
            self.visor.set_pagina(None)
            self.toolbarpaginas.set_pagina(None, None)
    
    def activar(self, widget, senial):
        """Cuando se pasa de pagina."""
        
        if senial == 'atras':
            if self.indexpaginaactiva > 0:
                self.previewcontainer.seleccionar(self.indexpaginaactiva-1)
            else:
                self.previewcontainer.seleccionar(self.npaginas-1)
        elif senial == 'siguiente':
            if self.indexpaginaactiva < self.npaginas-1:
                self.previewcontainer.seleccionar(self.indexpaginaactiva+1)
            else:
                self.previewcontainer.seleccionar(0)
    
    def embed_event(self, widget):
        """No hace nada por ahora."""
        
        print "JAMediaLector => OK"
    
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        self.toolbar_salir.run("JAMediaLector")
        
    def emit_salir(self, widget = None, senial = None):
        """Emite salir para que cuando esta embebida, la
        aplicacion decida que hacer, si salir, o cerrar solo
        JAMediaLector."""
        
        self.emit('salir')
        