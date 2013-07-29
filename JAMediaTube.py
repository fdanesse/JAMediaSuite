#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTube.py por:
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
import sys

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarSalir

JAMediaObjectsPath = JAMediaObjects.__path__[0]

#base_path = os.path.dirname(__file__)
#commands.getoutput('PATH=%s:$PATH' % (base_path))

import JAMediaObjects.JAMediaYoutube as YT
import JAMediaObjects.JAMediaGlobales as G
import JAMediaObjects.JAMFileSystem as JAMF

import JAMediaTube
from JAMediaTube.Widgets import Toolbar
from JAMediaTube.Widgets import Toolbar_Busqueda
from JAMediaTube.Widgets import Toolbar_Descarga
from JAMediaTube.Widgets import Alerta_Busqueda
from JAMediaTube.Widgets import WidgetVideoItem
from JAMediaTube.Widgets import Tube_Player

from JAMediaTube.PanelTube import PanelTube

'''
screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMediaEstilo.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()
context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)'''
    
TipDescargas = "Arrastra Hacia La Izquierda para Quitarlo de Descargas."
TipEncontrados = "Arrastra Hacia La Derecha para Agregarlo a Descargas"

GObject.threads_init()
Gdk.threads_init()

class Ventana(Gtk.Window):
    """
    JAMediaTube.
    """
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMediaTube")
        self.set_icon_from_file(os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMediaTube.png"))
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.box_tube = None
        
        self.toolbar = None
        self.toolbar_busqueda = None
        self.toolbar_descarga = None
        self.toolbar_salir = None
        self.alerta_busqueda = None
        self.paneltube = None
        
        self.socketjamedia = Gtk.Socket()
        self.jamedia = None
        
        self.pistas = []
        
        self.videos_temp = []
        
        self.setup_init()
        
    def setup_init(self):
        """
        Crea y Empaqueta todo.
        """
        
        boxbase = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.box_tube = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbar = Toolbar()
        self.toolbar_busqueda = Toolbar_Busqueda()
        self.toolbar_descarga = Toolbar_Descarga()
        self.toolbar_salir = ToolbarSalir()
        self.alerta_busqueda = Alerta_Busqueda()
        self.paneltube = PanelTube()
        
        self.box_tube.pack_start(self.toolbar, False, False, 0)
        self.box_tube.pack_start(self.toolbar_salir, False, False, 0)
        self.box_tube.pack_start(self.toolbar_busqueda, False, False, 0)
        self.box_tube.pack_start(self.toolbar_descarga, False, False, 0)
        self.box_tube.pack_start(self.alerta_busqueda, False, False, 0)
        self.box_tube.pack_start(self.paneltube, True, True, 0)
        
        boxbase.pack_start(self.box_tube, True, True, 0)
        
        boxbase.pack_start(self.socketjamedia, True, True, 0)
        
        self.add(boxbase)
        
        self.jamedia = Tube_Player()
        self.socketjamedia.add_id(self.jamedia.get_id())
        
        self.show_all()
        self.realize()
        
        self.paneltube.set_vista_inicial() # oculta las toolbarsaccion
        
        GObject.idle_add(self.setup_init2)
    
    def setup_init2(self):
        """
        Inicializa la aplicación a su estado fundamental.
        """
        
        self.jamedia.setup_init()
        self.jamedia.pack_standar()
        self.jamedia.switch_reproductor(None, "JAMediaReproductor")
        
        map(self.ocultar,[
            self.toolbar_descarga,
            self.toolbar_salir,
            self.alerta_busqueda,
            self.paneltube.toolbar_guardar_encontrados,
            self.paneltube.toolbar_guardar_descargar])
        
        if self.pistas:
            self.jamedia.set_nueva_lista(self.pistas)
            self.switch(None, 'jamedia')
            
        else:
            self.switch(None, 'jamediatube')
        
        self.paneltube.encontrados.drag_dest_set(
            Gtk.DestDefaults.ALL,
            target,
            Gdk.DragAction.MOVE)
            
        self.paneltube.encontrados.connect("drag-drop", self.drag_drop)
        self.paneltube.encontrados.drag_dest_add_uri_targets()
        
        self.paneltube.descargar.drag_dest_set(
            Gtk.DestDefaults.ALL,
            target,
            Gdk.DragAction.MOVE)
            
        self.paneltube.descargar.connect("drag-drop", self.drag_drop)
        self.paneltube.descargar.drag_dest_add_uri_targets()
        
        self.connect("destroy", self.salir)
        self.toolbar.connect('salir', self.confirmar_salir)
        self.toolbar_salir.connect('salir', self.salir)
        self.toolbar.connect('switch', self.switch, 'jamedia')
        self.jamedia.connect('salir', self.switch, 'jamediatube')
        self.toolbar_busqueda.connect("comenzar_busqueda", self.comenzar_busqueda)
        self.paneltube.connect('download', self.run_download)
        self.paneltube.connect('open_shelve_list', self.open_shelve_list)
        self.toolbar_descarga.connect('end', self.run_download)
        
    def open_shelve_list(self, widget, shelve_list, toolbarwidget):
        """
        Carga una lista de videos almacenada en un
        archivo shelve en el area del panel correspondiente
        según que toolbarwidget haya lanzado la señal.
        """
        
        destino = False
        
        if toolbarwidget == self.paneltube.toolbar_encontrados:
            destino = self.paneltube.encontrados
            
        elif toolbarwidget == self.paneltube.toolbar_descargar:
            destino = self.paneltube.descargar
            
        videos = []
        for video in shelve_list:
            videos.append(video)
        
        GObject.idle_add(self.add_videos, videos, destino)
        
    def run_download(self, widget):
        """
        Comienza descarga de un video.
        """
        
        if self.toolbar_descarga.estado:
            return
    
        videos = self.paneltube.descargar.get_children()
        
        if videos:
            videos[0].get_parent().remove(videos[0])
            self.toolbar_descarga.download(videos[0])
        else:
            self.toolbar_descarga.hide()
            
    def drag_drop(self, destino, drag_context, x, y, n):
        """
        Ejecuta drop sobre un destino.
        """
        
        videoitem = Gtk.drag_get_source_widget(drag_context)
        
        if videoitem.get_parent() == destino:
            return
        
        else:
            # E try siguiente es para evitar problemas cuando:
            # El drag termina luego de que el origen se ha
            # comenzado a descargar y por lo tanto, no tiene padre.
            try:
                videoitem.get_parent().remove(videoitem)
                destino.pack_start(videoitem, False, False, 1)
                
            except:
                return
            
            if destino == self.paneltube.descargar:
                text = TipDescargas
                
            elif destino == self.paneltube.encontrados:
                text = TipEncontrados
                
            videoitem.set_tooltip_text(text)
        
    def comenzar_busqueda(self, widget, palabras):
        """
        Muestra la alerta de busqueda y lanza
        secuencia de busqueda y agregado de videos al panel.
        """
        
        map(self.mostrar,[self.alerta_busqueda])
        self.alerta_busqueda.label.set_text("Buscando: %s" % (palabras))
        
        GObject.timeout_add(300, self.lanzar_busqueda, palabras)
        
    def lanzar_busqueda(self, palabras):
        """
        Lanza la Búsqueda y comienza secuencia
        que agrega los videos al panel.
        """
        
        for video in YT.Buscar(palabras):
            self.videos_temp.append(video)
        
        GObject.idle_add(self.add_videos, self.videos_temp, self.paneltube.encontrados)
        return False
    
    def add_videos(self, videos, destino):
        """
        Se crean los video_widgets de videos y
        se agregan al panel, segun destino.
        """
        
        if len(self.videos_temp) < 1:
            # self.videos_temp contiene solo los videos
            # encontrados en las búsquedas, no los que se cargan
            # desde un archivo.
            map(self.ocultar,[self.alerta_busqueda])
        
        if videos:
            video = videos[0]
            
            videowidget = WidgetVideoItem(video)
            text = TipEncontrados
            
            if destino == self.paneltube.encontrados:
                text = TipEncontrados
                
            elif destino == self.paneltube.descargar:
                text = TipDescargas
                
            videowidget.set_tooltip_text(text)
            videowidget.show_all()
            
            videowidget.drag_source_set(
                Gdk.ModifierType.BUTTON1_MASK,
                target,
                Gdk.DragAction.MOVE)
            
            # FIXME: Enlentece la aplicación ya que exige procesamiento.
            #archivo = "/tmp/preview%d" % time.time()
            #fileimage, headers = urllib.urlretrieve(video["previews"][0][0], archivo)
            #pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(fileimage,
            #    50, 50)
            #videowidget.drag_source_set_icon_pixbuf(pixbuf)
            #commands.getoutput('rm %s' % (archivo))
            
            videos.remove(video)
            destino.pack_start(videowidget, False, False, 1)
            self.alerta_busqueda.label.set_text("Encontrado: %s" % (video["titulo"]))
            self.get_property('window').invalidate_rect(self.get_allocation(), True)
            self.get_property('window').process_updates(True)
            
            GObject.idle_add(self.add_videos, videos, destino)
        
    def set_pistas(self, pistas):
        """
        Cuando se ejecuta pasandole un archivo.
        """
        
        self.pistas = pistas
        
    def switch(self, widget, valor):
        """
        Cambia entre la vista de descargas y
        la de reproduccion.
        """
        
        if valor == 'jamediatube':
            map(self.ocultar,[self.socketjamedia])
            map(self.mostrar, [self.box_tube])
            
        elif valor == 'jamedia':
            map(self.ocultar,[self.box_tube])
            map(self.mostrar, [self.socketjamedia])
        
    def ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
    def confirmar_salir(self, widget = None, senial = None):
        """
        Recibe salir y lo pasa a la toolbar de confirmación.
        """
        
        self.toolbar_salir.run("JAMediaTube")
        
    def salir(self, widget = None, senial = None):
        
        # FIXME: Hay que Mejorar esta forma de salir.
        import commands
        commands.getoutput('killall mplayer')
        sys.exit(0)

target = [Gtk.TargetEntry.new('Mover', Gtk.TargetFlags.SAME_APP, 0)]

def get_item_list(path):
    
    if os.path.exists(path):
        if os.path.isfile(path):
            archivo = os.path.basename(path)
            
            if 'audio' in JAMF.describe_archivo(path) or \
                'video' in JAMF.describe_archivo(path):
                    return [archivo, path]
        
    return False

if __name__ == "__main__":
    
    items = []
    
    if len(sys.argv) > 1:
        
        for campo in sys.argv[1:]:
            path = os.path.join(campo)
            
            if os.path.isfile(path):
                item = get_item_list(path)
                
                if item:
                    items.append( item )
                    
            elif os.path.isdir(path):
                
                for arch in os.listdir(path):
                    newpath = os.path.join(path, arch)
                    
                    if os.path.isfile(newpath):
                        item = get_item_list(newpath)
                        
                        if item:
                            items.append( item )
                            
        if items:
            jamediatube = Ventana()
            jamediatube.set_pistas(items)
            
        else:
            jamediatube = Ventana()
        
    else:
        jamediatube = Ventana()
        
    Gtk.main()
    