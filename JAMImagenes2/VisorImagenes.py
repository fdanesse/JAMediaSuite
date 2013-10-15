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
from gi.repository import GLib

from Widgets import ToolbarImagen
from Widgets import ToolbarTry
from Widgets import ToolbarConfig

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaObjects.JAMFileSystem import describe_archivo

class VisorImagenes (Gtk.EventBox):
    
    __gtype_name__ = 'JAMediaImagenesVisorImagenes'
    
    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'switch_to': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
        
    def __init__(self, path):
        
        Gtk.EventBox.__init__(self)
        
        self.path = path # Directorio
        
        base_box = Gtk.VBox()
        
        self.imagenes = []
        self.active_index_imagen = 0
        self.intervalo = False
        self.actualizador = False
        
        self.toolbar = ToolbarImagen(path)
        self.visor = Visor()
        self.toolbar_config = ToolbarConfig()
        self.toolbartry = ToolbarTry()
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.visor)
        
        base_box.pack_start(self.toolbar, False, False, 0)
        base_box.pack_start(self.toolbar_config, False, False, 0)
        base_box.pack_start(scroll, True, True, 0)
        base_box.pack_end(self.toolbartry, False, False, 0)
        
        self.add(base_box)
        
        self.show_all()
    
        self.toolbar.connect('switch_to', self.__emit_switch)
        self.toolbar.connect('activar', self.__set_accion)
        self.toolbar.connect('salir', self.__salir)
        self.toolbar_config.connect('run', self.__set_presentacion)
        self.visor.connect('changed', self.__set_change_image)
        self.visor.connect('info', self.__set_info)
        
        self.toolbar_config.hide()
        self.toolbar.set_modo("nochanged")
        self.toolbar.set_modo("edit")
        
        self.connect("motion-notify-event",
            self.__do_motion_notify_event)
            
        self.visor.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK
        )
        
        self.visor.connect("button_press_event", self.__clicks_en_pantalla)
        
    def __clicks_en_pantalla(self, widget, event):
        
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            
            self.get_toplevel().set_sensitive(False)
            
            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w,h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            
            if ww == w and hh == h:
                GLib.idle_add(ventana.unfullscreen)
                
            else:
                GLib.idle_add(ventana.fullscreen)
                
            self.get_toplevel().set_sensitive(True)
            
    def __do_motion_notify_event(self, widget, event):
        """
        Cuando se mueve el mouse sobre la ventana.
        """
        
        if self.toolbar_config.get_visible():
            return
        
        rect = self.toolbar.get_allocation()
        arriba = range(0, rect.height)
        
        root_rect = self.get_toplevel().get_allocation()
        rect = self.toolbartry.get_allocation()
        abajo = range(root_rect.height - rect.height, root_rect.height)
        x, y = self.get_toplevel().get_pointer()
        
        if y in arriba or y in abajo:
            if not self.toolbar.get_visible(): self.toolbar.show()
            if not self.toolbartry.get_visible(): self.toolbartry.show()
            return
        
        else:
            if self.toolbar.get_visible(): self.toolbar.hide()
            if self.toolbartry.get_visible(): self.toolbartry.hide()
            return
        
    def __set_presentacion(self, widget = None, intervalo = False):
        """
        Lanza el modo diapositivas.
        """
        
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
            
        if intervalo:
            self.intervalo = intervalo
            self.toolbar.set_modo("player")
            
        self.toolbar.set_playing()
        self.actualizador = GLib.timeout_add(
            self.intervalo, self.__handle_presentacion)
        
    def __stop_presentacion(self):
        
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
            
        self.toolbar.set_paused()
        
    def __handle_presentacion(self):
        """
        Cuando está en modo Diapositivas.
        """
        
        if self.active_index_imagen < len(self.imagenes)-1:
            self.active_index_imagen += 1
            
        else:
            self.active_index_imagen = 0
            
        self.__show_imagen(self.imagenes[self.active_index_imagen])
        
        return True
    
    def __set_accion(self, widget, accion):
        
        self.get_toplevel().set_sensitive(False)
        
        if accion == "Configurar Presentación":
            
            self.__stop_presentacion()
            
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            else:
                self.toolbar_config.show()
            
        elif accion == "Reproducir":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            if self.actualizador:
                self.__stop_presentacion()
                
            else:
                self.__set_presentacion()
            
        elif accion == "Anterior":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.__stop_presentacion()

            if self.active_index_imagen > 0:
                self.active_index_imagen -= 1
                
            else:
                self.active_index_imagen = self.imagenes.index(self.imagenes[-1])
                
            self.__show_imagen(self.imagenes[self.active_index_imagen])
        
        elif accion == "Siguiente":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.__stop_presentacion()

            if self.active_index_imagen < len(self.imagenes)-1:
                self.active_index_imagen += 1
                
            else:
                self.active_index_imagen = 0
                
            self.__show_imagen(self.imagenes[self.active_index_imagen])
            
        elif accion == "Detener":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.__stop_presentacion()
        
        elif accion == "Rotar Izquierda":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.visor.rotar(-1)
            
        elif accion == "Rotar Derecha":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.visor.rotar(1)
            
        elif accion == "Acercar":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.visor.zoom(1)
            
        elif accion == "Alejar":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.visor.zoom(-1)
            
        elif accion == "Centrar en Pantalla":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
                
            self.visor.center_image()
        
        elif accion == "Navegar Imágenes":
            if self.toolbar_config.get_visible():
                self.toolbar_config.hide()
            
            self.__stop_presentacion()

            if self.toolbar.modo != "edit":
                self.toolbar.set_modo("edit")
                
            elif self.toolbar.modo == "edit":
                self.toolbar.set_modo("player")
            
        elif accion == "Guardar":
            self.visor.guardar()
            
        self.get_toplevel().set_sensitive(True)
        
    def __set_change_image(self, widget, valor):
        """
        Cuando el usuario rota la imagen, puede guardarla.
        """
        
        if valor:
            self.toolbar.set_modo("changed")
            
        else:
            self.toolbar.set_modo("nochanged")
        
    def __emit_switch(self, widget, path):
        
        self.__stop_presentacion()
        self.emit("switch_to", path)
        
    def __salir(self, widget):
        
        self.__stop_presentacion()
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
            if len(self.imagenes) == 1:
                self.toolbar.set_modo("noconfig")
                
            self.__show_imagen(self.imagenes[0])
            
    def __show_imagen(self, imagen):
        
        self.visor.load(imagen)

        '''
        while Gtk.events_pending():
            Gtk.main_iteration()
        '''
        self.queue_draw()
        
    def __set_info(self, widget, info):
        
        self.toolbartry.set_info(info)
        
class Visor(Gtk.DrawingArea):
    """
    Visor de Imágenes.
    """
    
    __gtype_name__ = 'JAMediaImagenesVisor'
    
    __gsignals__ = {
        'changed': (GObject.SIGNAL_RUN_LAST,
            GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,)),
        'info': (GObject.SIGNAL_RUN_LAST,
            GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):
        
        Gtk.DrawingArea.__init__(self)
        
        #self.touch_events = OrderedDict()
        self.imagen_original = None
        self.image_path = None
        self.angulo = 0
        self.rotacion = GdkPixbuf.PixbufRotation.NONE
        self.zoom_valor = 0
        self.imagen = False
        self.temp_path = "/dev/shm/img.png"
        
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
                self.angulo = 0
                self.rotacion = GdkPixbuf.PixbufRotation.NONE
                self.zoom_valor = 0
                self.image_path = path
                self.imagen_original = GdkPixbuf.Pixbuf.new_from_file(path)
                self.imagen = self.imagen_original.copy()
                self.imagen.savev(self.temp_path, "png", [], [])
                
                self.set_size_request(-1, -1)
                self.emit("info",
                    "Archivo: %s   Tamaño: %s x %s Pixeles" % (path,
                        self.imagen_original.get_width(),
                        self.imagen_original.get_height()))
                        
                self.emit("changed", False)
                
    def guardar(self):
        
        ext = self.image_path.split(".")[-1]
        if ext.lower() != "png":
            return
    
        try:
            self.imagen.savev(self.image_path, ext, [], [])
            self.load(self.image_path)
            
        except:
            pass
        
    def __do_draw(self, widget, context):
        
        if not self.image_path: return
        
        rect = self.get_allocation()
        
        src = self.imagen
        dst = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.temp_path, rect.width, rect.height)
        
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
            
    def rotar(self, angulo):
        
        if not self.imagen_original: return

        if angulo > 0: self.angulo += 90
        if angulo < 0: self.angulo -= 90
        
        if self.angulo == 0:
            self.rotacion = GdkPixbuf.PixbufRotation.NONE
            
        elif self.angulo == 90:
            self.rotacion = GdkPixbuf.PixbufRotation.CLOCKWISE
            
        elif self.angulo == 180:
            self.rotacion = GdkPixbuf.PixbufRotation.UPSIDEDOWN
            
        elif self.angulo == 270:
            self.rotacion = GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE
            
        elif self.angulo == 360:
            self.rotacion = GdkPixbuf.PixbufRotation.NONE
            
        elif self.angulo == -90:
            self.rotacion = GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE
            
        elif self.angulo == -180:
            self.rotacion = GdkPixbuf.PixbufRotation.UPSIDEDOWN
            
        elif self.angulo == -270:
            self.rotacion = GdkPixbuf.PixbufRotation.CLOCKWISE
            
        elif self.angulo == -360:
            self.rotacion = GdkPixbuf.PixbufRotation.NONE
        
        if self.angulo >= 360 or self.angulo <= -360:
            self.angulo = 0
            self.rotacion = GdkPixbuf.PixbufRotation.NONE
            
        self.imagen = self.imagen_original.copy().rotate_simple(self.rotacion)
        self.imagen.savev(self.temp_path, "png", [], [])
        
        # FIXME: Solo guardar cambios en imagenes png.
        ext = self.image_path.split(".")[-1]
        if ext.lower() == "png":
            if self.rotacion != GdkPixbuf.PixbufRotation.NONE:
                self.emit("changed", True)
                
            else:
                self.emit("changed", False)
            
        self.queue_draw()
        
    def zoom(self, zoom):
        """
        zoom es 1 o -1
        self.zoom_valor va desde 0 a 10
        """
        
        if not self.imagen_original: return

        if self.zoom_valor + zoom < 0:
            self.zoom_valor = 0
            return
        
        elif self.zoom_valor + zoom > 10:
            self.zoom_valor = 10
            return
        
        else:
            self.zoom_valor += zoom
        
        if zoom == 1:
            rect = self.get_allocation()
            width = int(rect.width * 1.1)
            height = int(rect.height * 1.1)
            good = width > rect.width or height > rect.height
            
            while not good:
                return self.zoom(1)
            
            self.set_size_request(width, height)
            self.rotar(0)
        
        elif zoom == -1:
            rect = self.get_allocation()
            width = rect.width - (int(rect.width * 1.1) - rect.width)
            height = rect.height - (int(rect.height * 1.1) - rect.height)
            good = width < rect.width or height < rect.height
            
            while not good:
                return self.zoom(-1)
            
            self.set_size_request(width, height)
            self.rotar(0)
        
    def center_image(self):
        
        self.zoom_valor = 0
        self.set_size_request(-1, -1)
        