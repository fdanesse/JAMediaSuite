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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]
    
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
        
        self.__setup_init()
        
    def __setup_init(self):
        """
        Crea y Empaqueta todo.
        """
        
        from JAMediaTube.Widgets import Toolbar
        from JAMediaTube.Widgets import Toolbar_Busqueda
        from JAMediaTube.Widgets import Toolbar_Descarga
        from JAMediaTube.Widgets import Alerta_Busqueda
        
        from JAMediaTube.PanelTube import PanelTube
        
        from JAMediaObjects.JAMediaWidgets import ToolbarSalir
        
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
        
        from JAMediaTube.Widgets import Tube_Player
        
        self.jamedia = Tube_Player()
        self.socketjamedia.add_id(self.jamedia.get_id())
        
        self.show_all()
        self.realize()
        
        self.paneltube.set_vista_inicial() # oculta las toolbarsaccion
        
        GLib.idle_add(self.__setup_init2)
    
    def __setup_init2(self):
        """
        Inicializa la aplicación a su estado fundamental.
        """
        
        self.jamedia.setup_init()
        self.jamedia.pack_standar()
        self.jamedia.switch_reproductor(None, "JAMediaReproductor")
        
        self.__cancel_toolbar()
        self.paneltube.cancel_toolbars_flotantes()
        
        map(self.__ocultar,[
            self.toolbar_descarga,
            self.alerta_busqueda])
        
        if self.pistas:
            self.jamedia.set_nueva_lista(self.pistas)
            self.__switch(None, 'jamedia')
            
        else:
            self.__switch(None, 'jamediatube')
        
        self.paneltube.encontrados.drag_dest_set(
            Gtk.DestDefaults.ALL,
            target,
            Gdk.DragAction.MOVE)
            
        self.paneltube.encontrados.connect("drag-drop", self.__drag_drop)
        self.paneltube.encontrados.drag_dest_add_uri_targets()
        
        self.paneltube.descargar.drag_dest_set(
            Gtk.DestDefaults.ALL,
            target,
            Gdk.DragAction.MOVE)
            
        self.paneltube.descargar.connect("drag-drop", self.__drag_drop)
        self.paneltube.descargar.drag_dest_add_uri_targets()
        
        self.connect("delete-event", self.__salir)
        self.toolbar.connect('salir', self.__confirmar_salir)
        self.toolbar_salir.connect('salir', self.__salir)
        self.toolbar.connect('switch', self.__switch, 'jamedia')
        self.jamedia.connect('salir', self.__switch, 'jamediatube')
        self.toolbar_busqueda.connect("comenzar_busqueda", self.__comenzar_busqueda)
        self.paneltube.connect('download', self.__run_download)
        self.paneltube.connect('open_shelve_list', self.__open_shelve_list)
        self.toolbar_descarga.connect('end', self.__run_download)
        self.paneltube.connect("cancel_toolbar", self.__cancel_toolbar)
        
    def __cancel_toolbar(self, widget = None):
        
        self.toolbar_salir.cancelar()
        
    def __open_shelve_list(self, widget, shelve_list, toolbarwidget):
        """
        Carga una lista de videos almacenada en un
        archivo shelve en el area del panel correspondiente
        según que toolbarwidget haya lanzado la señal.
        """
        
        self.paneltube.set_sensitive(False)
        self.toolbar_busqueda.set_sensitive(False)
        
        destino = False
        
        if toolbarwidget == self.paneltube.toolbar_encontrados:
            destino = self.paneltube.encontrados
            
        elif toolbarwidget == self.paneltube.toolbar_descargar:
            destino = self.paneltube.descargar
        
        objetos = destino.get_children()
        
        for objeto in objetos:
            objeto.get_parent().remove(objeto)
            objeto.destroy()
            
        GLib.idle_add(self.__add_videos, shelve_list, destino)
        
    def __run_download(self, widget):
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
            
    def __drag_drop(self, destino, drag_context, x, y, n):
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
        
    def __comenzar_busqueda(self, widget, palabras):
        """
        Muestra la alerta de busqueda y lanza
        secuencia de busqueda y agregado de videos al panel.
        """
        
        self.paneltube.set_sensitive(False)
        self.toolbar_busqueda.set_sensitive(False)
        
        self.__cancel_toolbar()
        self.paneltube.cancel_toolbars_flotantes()
        map(self.__mostrar,[self.alerta_busqueda])
        self.alerta_busqueda.label.set_text("Buscando: %s" % (palabras))
        
        objetos = self.paneltube.encontrados.get_children()
        
        for objeto in objetos:
            objeto.get_parent().remove(objeto)
            objeto.destroy()
            
        GLib.timeout_add(300, self.__lanzar_busqueda, palabras)
        
    def __lanzar_busqueda(self, palabras):
        """
        Lanza la Búsqueda y comienza secuencia
        que agrega los videos al panel.
        """
        
        import JAMediaObjects.JAMediaYoutube as YT
        
        for video in YT.Buscar(palabras):
            self.videos_temp.append(video)
        
        GLib.idle_add(self.__add_videos, self.videos_temp, self.paneltube.encontrados)
        
        return False
    
    def __add_videos(self, videos, destino):
        """
        Se crean los video_widgets de videos y
        se agregan al panel, segun destino.
        """
        
        if len(self.videos_temp) < 1:
            # self.videos_temp contiene solo los videos
            # encontrados en las búsquedas, no los que se cargan
            # desde un archivo.
            map(self.__ocultar,[self.alerta_busqueda])
        
        if not videos:
            self.paneltube.set_sensitive(True)
            self.toolbar_busqueda.set_sensitive(True)
            return False
        
        video = videos[0]
        
        from JAMediaTube.Widgets import WidgetVideoItem
        
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

        texto = "Encontrado: %s" % (video["titulo"])
        if len(texto) > 50:
            texto = str(texto[0:50]) + " . . . "
            
        self.alerta_busqueda.label.set_text(texto)
        #self.alerta_busqueda.label.set_text("Encontrado: %s" % (video["titulo"]))
        #self.get_property('window').invalidate_rect(self.get_allocation(), True)
        #self.get_property('window').process_updates(True)
        
        GLib.idle_add(self.__add_videos, videos, destino)
        
    def set_pistas(self, pistas):
        """
        Cuando se ejecuta pasandole un archivo.
        """
        
        self.pistas = pistas
        
    def __switch(self, widget, valor):
        """
        Cambia entre la vista de descargas y
        la de reproduccion.
        """
        
        if valor == 'jamediatube':
            map(self.__ocultar,[self.socketjamedia])
            map(self.__mostrar, [self.box_tube])
            
        elif valor == 'jamedia':
            map(self.__ocultar,[self.box_tube])
            map(self.__mostrar, [self.socketjamedia])
        
    def __ocultar(self, objeto):
        
        if objeto.get_visible(): objeto.hide()
        
    def __mostrar(self, objeto):
        
        if not objeto.get_visible(): objeto.show()
        
    def __confirmar_salir(self, widget = None, senial = None):
        """
        Recibe salir y lo pasa a la toolbar de confirmación.
        """
        
        self.paneltube.cancel_toolbars_flotantes()
        
        self.toolbar_salir.run("JAMediaTube")
        
    def __salir(self, widget = None, senial = None):
        
        # FIXME: Hay que Mejorar esta forma de salir.
        import commands
        import sys
        
        commands.getoutput('killall mplayer')
        sys.exit(0)

target = [Gtk.TargetEntry.new('Mover', Gtk.TargetFlags.SAME_APP, 0)]

def get_item_list(path):
    
    if os.path.exists(path):
        if os.path.isfile(path):
            archivo = os.path.basename(path)
            
            from JAMediaObjects.JAMFileSystem import describe_archivo
            
            if 'audio' in describe_archivo(path) or \
                'video' in describe_archivo(path):
                    return [archivo, path]
        
    return False

if __name__ == "__main__":
    
    import sys
    
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
    