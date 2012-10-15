#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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
import time
import commands
import urllib

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import JAMediaButton
from JAMediaObjects.JAMediaYoutube import JAMediaYoutube

import JAMedia
from JAMedia.JAMedia import JAMediaPlayer

#import JAMediaObjects.JAMFileSystem as JAMF
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]

class Tube_Player(JAMediaPlayer):
    """JAMedia con pequeñas adaptaciones."""
    
    def __init__(self):
        
        JAMediaPlayer.__init__(self)
        
        self.show_all()
        
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        map(self.ocultar, [
            self.toolbar_config,
            self.toolbaraddstream])
            
        # Salteandose confirmación para salir
        # y maneteniendose activa la reproducción y
        # grabación de JAMedia.
        # self.toolbar_salir.run("JAMedia")
        
        self.emit('salir')
        
class Toolbar(Gtk.Toolbar):
    """Toolbar principal de JAMediaTube."""
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'switch':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","JAMediaTube.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.png")
        self.jamedia = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(1))
        self.jamedia.set_tooltip_text("Cambiar a JAMedia.")
        self.jamedia.connect("clicked", self.emit_switch)
        self.insert(self.jamedia, -1)
        
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
        
    def emit_switch(self, widget):
        """Cambia de JAMediaTube a JAMedia."""
        
        self.emit('switch')
        
    def salir(self, widget):
        """Cuando se hace click en el boton salir."""
        
        self.emit('salir')
        
class Toolbar_Videos_Izquierda(Gtk.Toolbar):
    """toolbar inferior izquierda para videos encontrados."""
    
    __gsignals__ = {
    "borrar":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    "mover_videos":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
            
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Borrar Lista.")
        boton.connect("clicked", self.emit_borrar)
        self.insert(boton, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "iconplay.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Enviar a Descargas.")
        boton.connect("clicked", self.emit_adescargas)
        self.insert(boton, -1)
        
        self.show_all()
        
    def emit_adescargas(self, widget):
        """Para pasar los videos encontrados a la
        lista de descargas."""
        
        self.emit('mover_videos')
        
    def emit_borrar(self, widget):
        """Para borrar todos los videos de la lista."""
        
        self.emit('borrar')
        
class Toolbar_Videos_Derecha(Gtk.Toolbar):
    """toolbar inferior derecha para videos en descarga."""
    
    __gsignals__ = {
    "borrar":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    "mover_videos":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'comenzar_descarga':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
        
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "iconplay.png")
        boton = G.get_boton(archivo, flip = True,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Quitar de Descargas.")
        boton.connect("clicked", self.emit_aencontrados)
        self.insert(boton, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Borrar Lista.")
        boton.connect("clicked", self.emit_borrar)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
            
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "iconplay.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8),
            rotacion = GdkPixbuf.PixbufRotation.CLOCKWISE)
        boton.set_tooltip_text("Descargar.")
        boton.connect("clicked", self.emit_comenzar_descarga)
        self.insert(boton, -1)
        
        self.show_all()
        
    def emit_comenzar_descarga(self, widget):
        """Emite la señal para comenzar a descargar
        los videos en la lista de descargas."""
        
        self.emit('comenzar_descarga')
    
    def emit_aencontrados(self, widget):
        """Para pasar los videos en descarga a la
        lista de encontrados."""
        
        self.emit('mover_videos')
        
    def emit_borrar(self, widget):
        """Para borrar todos los videos de la lista."""
        
        self.emit('borrar')
        
class Mini_Toolbar(Gtk.Toolbar):
    """Mini toolbars izquierda y derecha."""
    
    def __init__(self, text):
        
        Gtk.Toolbar.__init__(self)
        
        self.label = None
        self.texto = text
        self.numero = 0
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("%s: %s" % (text, self.numero) )
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.show_all()
        
    def set_info(self, valor):
        """Recibe un entero y actualiza la información."""
        
        if valor != self.numero:
            self.numero = valor
            text = "%s: %s" % (self.texto, str(self.numero))
            self.label.set_text(text)
        
class Toolbar_Busqueda(Gtk.Toolbar):
    """Toolbar con widgets de busqueda."""
    
    __gsignals__ = {
    "comenzar_busqueda":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        item = Gtk.ToolItem()
        label = Gtk.Label("Buscar por: ")
        label.show()
        item.add(label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        item = Gtk.ToolItem()
        self.entrytext = Gtk.Entry()
        self.entrytext.set_size_request(400, -1)
        self.entrytext.set_max_length(50)
        self.entrytext.set_tooltip_text("Escribe lo que Buscas.")
        self.entrytext.show()
        self.entrytext.connect('activate', self.activate_entrytext)
        item.add(self.entrytext)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "iconplay.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8),
            rotacion = GdkPixbuf.PixbufRotation.CLOCKWISE)
        boton.set_tooltip_text("Comenzar Búsqueda")
        boton.connect("clicked", self.emit_buscar)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)

        self.show_all()
        
        boton.connect("clicked", self.emit_buscar)
        
    def emit_buscar(self, widget = None):
        
        texto = self.entrytext.get_text()
        if texto: self.emit("comenzar_busqueda", texto)
        self.entrytext.set_text("")
        
    def activate_entrytext(self, widget):
        """Cuando se da enter en el entrytext."""
        
        self.emit_buscar()
        
class Alerta_Busqueda(Gtk.Toolbar):
    """Para informa que se está buscando con JAMediaTube."""
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.label = None
        
        self.set_layout()
        self.show_all()
        
    def set_layout(self):
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","yt_videos_black.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
            
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("")
        self.label.set_justify(Gtk.Justification.LEFT)
        #self.label.set_line_wrap(True)
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
class WidgetVideoItem(JAMediaButton):
    
    def __init__(self, videodict):
        
        JAMediaButton.__init__(self)
        
        self.set_border_width(2)
        
        self.videodict = videodict
        
        self.imagen.destroy()
        
        self.layout()
        self.show_all()
    
    def button_press(self, widget, event):
        pass
    
    def button_release(self, widget, event):
        pass
    
    def set_imagen(self, archivo):
        pass
    
    def layout(self):
        
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        keys = self.videodict.keys()
        
        if "previews" in keys:
            imagen = Gtk.Image()
            url = self.videodict["previews"][0][0]
            archivo = "/tmp/preview%d" % time.time()
            fileimage, headers = urllib.urlretrieve(url, archivo)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(fileimage, 200, 200)
            imagen.set_from_pixbuf(pixbuf)
            hbox.pack_start(imagen, False, False, 3)
            commands.getoutput('rm %s' % (archivo))
            
        vbox.pack_start(Gtk.Label("%s: %s" % ("id",
            self.videodict["id"])), True, True, 0)
            
        vbox.pack_start(Gtk.Label("%s: %s" % ("Título",
            self.videodict["titulo"])), True, True, 0)
            
        vbox.pack_start(Gtk.Label("%s: %s" % ("Categoría",
            self.videodict["categoria"])), True, True, 0)
            
        #vbox.pack_start(gtk.Label("%s: %s" % ("Etiquetas",
        #    self.videodict["etiquetas"])), True, True, 0)
        
        #vbox.pack_start(gtk.Label("%s: %s" % ("Descripción",
        #   self.videodict["descripcion"])), True, True, 0)
        
        vbox.pack_start(Gtk.Label("%s: %s %s" % ("Duración",
            int(float(self.videodict["duracion"])/60.0), "Minutos")),
            True, True, 0)
            
        #vbox.pack_start(gtk.Label("%s: %s" % ("Reproducción en la Web",
        #   self.videodict["flash player"])), True, True, 0)
        
        vbox.pack_start(Gtk.Label("%s: %s" % ("url",
            self.videodict["url"])), True, True, 0)
        
        for label in vbox.get_children():
            
            label.set_justify(Gtk.Justification.LEFT)
            
        hbox.pack_start(vbox, False, False, 0)
        self.add(hbox)
        
class ToolbarAccionListasVideos(Gtk.Toolbar):
    """Toolbar para que el usuario confirme "borrar"
    lista de video de JAMediaTube."""
    
    __gsignals__ = {
    "ok":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        #self.modify_bg(0, Gdk.Color(65000,65000,65000))
        
        self.objetos = None
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        item = Gtk.ToolItem()
        #item.set_expand(True)
        self.label = Gtk.Label("")
        #self.label.set_line_wrap(True)
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
            
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "acercar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.realizar_accion)
        self.insert(boton, -1)

        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.show_all()
    
    def realizar_accion(self, widget):
        """Confirma borrar."""
        
        self.emit('ok', self.objetos)
        self.objetos = None
        self.label.set_text("")
        self.hide()
        
    def set_accion(self, objetos):
        """Configura borrar."""
        
        self.objetos = objetos
        self.label.set_text("¿Eliminar?")
        self.show_all()
        
    def cancelar(self, widget = None):
        """Cancela borrar."""
        
        self.objetos = None
        self.label.set_text("")
        self.hide()
        
class Toolbar_Descarga(Gtk.Box):
    
    __gsignals__ = {
    'end':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbar = Gtk.Toolbar()
        
        self.label_titulo = None
        self.label_progreso = None
        self.progress = 0.0
        self.barra_progreso = None
        self.estado = False
        
        self.actualizador = False
        
        self.datostemporales = None
        self.ultimosdatos = None
        self.contadortestigo = 0
        
        self.video_item = None
        self.url = None
        self.titulo = None
        
        self.jamediayoutube = JAMediaYoutube()
        
        self.set_layout()
        
        self.show_all()
        
        self.jamediayoutube.connect("progress_download", self.progress_download)
        
    def set_layout(self):
        
        self.toolbar.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        #item.set_expand(True)
        self.label_titulo = Gtk.Label("")
        #self.label_titulo.set_line_wrap(True)
        self.label_titulo.show()
        item.add(self.label_titulo)
        self.toolbar.insert(item, -1)

        self.toolbar.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)

        item = Gtk.ToolItem()
        #item.set_expand(True)
        self.label_progreso = Gtk.Label("")
        #self.label_progreso.set_line_wrap(True)
        self.label_progreso.show()
        item.add(self.label_progreso)
        self.toolbar.insert(item, -1)
        
        #self.toolbar.insert(G.get_separador(draw = False,
        #    ancho = 0, expand = True), -1)
            
        # FIXME: BUG. Las descargas no se cancelan.
        #archivo = os.path.join(JAMediaObjectsPath,
        #    "Iconos","stop.png")
        #boton = G.get_boton(archivo, flip = False,
        #    pixels = G.get_pixels(1))
        #boton.set_tooltip_text("Cancelar")
        #boton.connect("clicked", self.cancel_download)
        #self.toolbar.insert(boton, -1)
        
        #self.toolbar.insert(G.get_separador(draw = False,
        #    ancho = 3, expand = False), -1)
        
        self.barra_progreso = Progreso_Descarga()
        self.barra_progreso.show()
        
        self.pack_start(self.toolbar, False, False, 0)
        self.pack_start(self.barra_progreso, False, False, 0)
        
    def download(self, video_item):
        """Comienza a descargar un video-item."""
        
        self.estado = True
        self.progress = 0.0
        self.datostemporales = None
        self.ultimosdatos = None
        self.contadortestigo = 0
        
        self.video_item = video_item
        self.url = video_item.videodict["url"]
        self.titulo = video_item.videodict["titulo"]
        
        self.label_titulo.set_text(self.titulo)
        self.jamediayoutube.download(self.url, self.titulo)
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            
        self.actualizador = GObject.timeout_add(1000, self.handle)
        
        self.show_all()
        
    def handle(self):
        """Verifica que se esté descargando el archivo."""
        
        if self.ultimosdatos != self.datostemporales:
            self.ultimosdatos = self.datostemporales
            self.contadortestigo = 0
            
        else:
            self.contadortestigo += 1
            
        if self.contadortestigo > 10:
            self.cancel_download()
            print "No se pudo controlar la descarga de:"
            print self.titulo, self.url
            return False
        
        return True
    
    def progress_download(self, widget, progress):
        """Muestra el progreso de la descarga."""
        
        self.datostemporales = progress
        datos = progress.split(" ")
        
        if datos[0] == '[youtube]':
            dat = progress.split('[youtube]')[1]
            if self.label_progreso.get_text() != dat:
                self.label_progreso.set_text( dat )
                
        elif datos[0] == '[download]':
            dat = progress.split('[download]')[1]
            if self.label_progreso.get_text() != dat:
                self.label_progreso.set_text( dat )
                
        elif datos[0] == '\r[download]':
            porciento = 0.0
            
            if "%" in datos[2]:
                porciento = datos[2].split("%")[0]
                
            elif "%" in datos[3]:
                porciento = datos[3].split("%")[0]
                
            porciento = float(porciento)
            self.barra_progreso.set_progress(valor = int(porciento))
                
            if porciento >= 100.0: # nunca llega
                self.cancel_download()
                return False
            
            else:
                dat = progress.split("[download]")[1]
                if self.label_progreso.get_text() != dat:
                    self.label_progreso.set_text( dat )
                    
        if "100.0%" in progress.split(" "):
            self.cancel_download()
            return False
        
        if not self.get_visible(): self.show()
        
        return True
    
    def cancel_download(self, button = None, event = None):
        """Cancela la descarga actual."""
        
        # No funciona correctamente, la descarga continúa.
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = False
            
        try:
            self.jamediayoutube.end()
        except:
            pass
        
        try:
            self.video_item.destroy()
        except:
            pass
        
        self.estado = False
        self.emit("end")
        
        return False
    
class Progreso_Descarga(Gtk.EventBox):
    """Barra de progreso para mostrar estado de descarga."""
    
    def __init__(self):
        
        Gtk.EventBox.__init__(self)
        
        #self.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        self.escala = ProgressBar(Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))
        
        self.valor = 0
        
        self.add(self.escala)
        self.show_all()
        
        self.set_size_request(-1, G.get_pixels(1.2))
        self.set_progress(0)
        
    def set_progress(self, valor = 0):
        """El reproductor modifica la escala."""
        
        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()
            
class ProgressBar(Gtk.Scale):
    """Escala de Progreso_Descarga."""
    
    def __init__(self, ajuste):
        
        Gtk.Scale.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)
        
        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)
        
        self.borde = G.get_pixels(0.5)
        
        self.show_all()
        
    def do_draw(self, contexto):
        """Dibuja el estado de la barra de progreso."""
        
        rect = self.get_allocation()
        w, h = (rect.width, rect.height)
        
        # Fondo
        #Gdk.cairo_set_source_color(contexto, G.BLANCO)
        #contexto.paint()

        # Relleno de la barra
        ww = w - self.borde*2
        hh = h - self.borde*2
        Gdk.cairo_set_source_color(contexto, G.NEGRO)
        rect = Gdk.Rectangle()
        rect.x, rect.y, rect.width, rect.height = (self.borde, self.borde, ww, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()
        
        # Relleno de la barra segun progreso
        Gdk.cairo_set_source_color(contexto, G.NARANJA)
        rect = Gdk.Rectangle()
        
        ximage = int(self.ajuste.get_value() * ww / 100)
        rect.x, rect.y, rect.width, rect.height = (self.borde, self.borde,
            ximage, hh)
        
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()
        
        return True
