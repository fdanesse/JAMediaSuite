#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VisorImagenes.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       CeibalJAM - Uruguay
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

import os
import cairo

from collections import OrderedDict

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GdkX11

from Widgets import ToolbarImagen
from Widgets import ToolbarTry

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaObjects.JAMFileSystem import describe_archivo

class VisorImagenes (Gtk.VBox):
    
    __gtype_name__ = 'JAMediaImagenesVisorImagenes'
    
    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'switch_to': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self, path):
        
        Gtk.VBox.__init__(self)
        
        self.path = path
        
        self.imagenes = []
        
        self.toolbar = ToolbarImagen(path)
        self.visor = Visor()
        # toolbar - Controles de reproducción.
        # toolbar [][][][] previews
        self.toolbartry = ToolbarTry()
        
        self.pack_start(self.toolbar, False, False, 0)
        self.pack_start(self.visor, True, True, 0)
        self.pack_end(self.toolbartry, False, False, 0)
        
        self.show_all()
    
        self.toolbar.connect('switch_to', self.__emit_switch)
        self.toolbar.connect('activar', self.__set_accion)
        self.toolbar.connect('salir', self.__salir)
        
    def __set_accion(self, widget, accion):
        
        print accion
        '''
        Original
        Alejar
        Acercar
        Izquierda
        Derecha
        Configurar
        Anterior
        Reproducir
        Siguiente
        Detener
        '''
        
    def __emit_switch(self, widget, path):
        
        self.emit("switch_to", path)
        
    def __salir(self, widget):
        
        self.emit("salir")
        
    def run(self):
        
        self.imagenes = []
        for arch in os.listdir(self.path):
            path = os.path.join(self.path, arch)
            
            if os.path.isfile(path):
                descripcion = describe_archivo(path)
                
                if 'image' in descripcion and not 'iso' in descripcion:
                    self.imagenes.append(path)
                    
        if self.imagenes:
            self.visor.load(self.imagenes[0])
            self.toolbartry.set_info(
                self.imagenes[0],
                (self.visor.imagen_original.get_width(),
                self.visor.imagen_original.get_height()))
        
class Visor(Gtk.DrawingArea):
    """
    Visor de Imágenes.
    """
    
    __gtype_name__ = 'JAMediaImagenesVisor'
    
    def __init__(self):
        
        Gtk.DrawingArea.__init__(self)
        
        #self.touch_events = OrderedDict()
        self.imagen_original = None
        self.image_path = None
        
        self.show_all()
        
        #self.add_events(Gdk.EventMask.TOUCH_MASK)
        
        self.connect("draw", self.__do_draw)
        #self.connect("touch-event", self.__touch_event)
        
    '''
    def __touch_event(self, widget, event):
        """
        Gestiona Gdk.EventTouch
        """
        
        touch_event = str(event.touch.sequence)
        
        if event.type == Gdk.EventType.TOUCH_BEGIN:
            
            self.touch_events[touch_event] = (
                event.touch.x, event.touch.y,
                event.touch.x_root, event.touch.y_root,
                event.touch.axes, event.touch.state)
            
        if event.type == Gdk.EventType.TOUCH_UPDATE:

            self.touch_events[touch_event] = (
                event.touch.x, event.touch.y,
                event.touch.x_root, event.touch.y_root,
                event.touch.axes, event.touch.state)
                
            self.__gestione_touch()
            
        if event.type == Gdk.EventType.TOUCH_CANCEL:
            del(self.touch_events[touch_event])
            
        if event.type == Gdk.EventType.TOUCH_END:
            del(self.touch_events[touch_event])
        '''
    '''
    def __gestione_touch(self):
        #for touch in self.touch_events.keys():
        #    print self.touch_events[touch][0:2]
        
        keys = self.touch_events.keys()
        
        if len(keys) == 2:
            event_0 = self.touch_events[keys[0]]
            event_1 = self.touch_events[keys[1]]
            
            x_0, y_0 = (event_0[0], event_0[1])
            x_1, y_1 = (event_1[0], event_1[1])
            
            ### Horizontal
            if x_1 > x_0:
                pass
            
            ### Vertical
            if y_1 > y_0:
                pass
            
        elif len(keys) == 1:
            pass
        '''
    
    def load(self, path):
        """
        Carga una imagen.
        """
        
        if path:
            if os.path.exists(path):
                self.image_path = path
                self.imagen_original = GdkPixbuf.Pixbuf.new_from_file(path)
                
    def __do_draw(self, widget, context):
        """
        Pinta la imagen lo más grande posible y
        centrada en la pantalla.
        """
        
        if not self.image_path: return
    
        rect = self.get_allocation()
        
        src = self.imagen_original.copy()
        dst = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.image_path, rect.width, rect.height)
        
        GdkPixbuf.Pixbuf.scale(
            src, dst, 0, 0, 100, 100,
            0, 0, 1.5, 1.5,
            GdkPixbuf.InterpType.BILINEAR)
            
        x = rect.width/2 - dst.get_width()/2
        y = rect.height/2 - dst.get_height()/2
        
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
            dst.get_width(), dst.get_height())
            
        Gdk.cairo_set_source_pixbuf(context, dst, x, y)
        context.paint()
        