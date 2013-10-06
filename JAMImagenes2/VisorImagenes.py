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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class VisorImagenes(Gtk.DrawingArea):
    """
    Visor de Imágenes.
    """
    
    __gtype_name__ = 'VisorImagenes'
    
    __gsignals__ = {
    'switch_to': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}
        
    def __init__(self, path):
        
        Gtk.DrawingArea.__init__(self)
        
        from collections import OrderedDict
        
        self.touch_events = OrderedDict()
        self.imagen_original = None
        self.image_path = None
        
        self.show_all()
        
        self.add_events(Gdk.EventMask.TOUCH_MASK)
        
        self.connect("draw", self.__do_draw)
        self.connect("touch-event", self.__touch_event)
        
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
            
    def __gestione_touch(self):
        #for touch in self.touch_events.keys():
        #    print self.touch_events[touch][0:2]
        """
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
        """
        pass
    
    def load_previews(self, basepath):
        """
        Carga una imagen.
        """
        
        if basepath:
            if os.path.exists(basepath):
                self.image_path = basepath
                self.imagen_original = GdkPixbuf.Pixbuf.new_from_file(basepath)
                
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
        