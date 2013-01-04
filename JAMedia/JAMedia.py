#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMedia.py por:
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
import time
import datetime

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import Visor
from JAMediaObjects.JAMediaWidgets import Lista
from JAMediaObjects.JAMediaWidgets import ToolbarReproduccion
from JAMediaObjects.JAMediaWidgets import BarraProgreso
from JAMediaObjects.JAMediaWidgets import ControlVolumen
from JAMediaObjects.JAMediaWidgets import ToolbarAccion
from JAMediaObjects.JAMediaWidgets import ToolbarSalir
from JAMediaObjects.JAMediaWidgets import WidgetsGstreamerEfectos

import JAMediaObjects.JAMFileSystem as JAMF

# HACK: La aplicación nunca debe explotar :P
if JAMF.get_programa("mplayer"):
    from JAMediaObjects.MplayerReproductor import MplayerReproductor
    from JAMediaObjects.MplayerReproductor import MplayerGrabador
    
else:
    from JAMediaObjects.PlayerNull import MplayerReproductor
    from JAMediaObjects.PlayerNull import MplayerGrabador
    
# HACK: La aplicación nunca debe explotar :P
if JAMF.verificar_Gstreamer():
    from JAMediaObjects.JAMediaReproductor import JAMediaReproductor
    from JAMediaObjects.JAMediaReproductor import JAMediaGrabador
    
else:
    from JAMediaObjects.PlayerNull import JAMediaReproductor
    from JAMediaObjects.PlayerNull import JAMediaGrabador
    
import JAMediaObjects.JAMediaGlobales as G

from Widgets import ToolbarLista
from Widgets import Toolbar
from Widgets import MenuList
from Widgets import ToolbarConfig
from Widgets import ToolbarGrabar
from Widgets import Selector_de_Archivos
from Widgets import ToolbarInfo
from Widgets import ToolbarAddStream
from Widgets import WidgetEfecto_en_Pipe

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

class JAMediaPlayer(Gtk.Plug):
    """JAMedia:
        Interfaz grafica de:
            JAMediaReproductor y MplayerReproductor.
            
        Implementado sobre:
            python 2.7.3 y Gtk 3
        
        Es un Gtk.Plug para embeber todo el reproductor
        en cualquier contenedor dentro de otra aplicacion.
        
    Para ello, es necesario crear en la aplicacion donde
    sera enbebida JAMedia, un socket:
        
    import JAMedia
    from JAMedia.JAMedia import JAMediaPlayer
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaplayer = JAMediaPlayer()
        socket.add_id(self.jamediaplayer.get_id()
        
    y luego proceder de la siguiente forma:
        
    GObject.idle_add(self.setup_init)
        
    def setup_init(self):
        self.jamediaplayer.setup_init()
        # Empaqueta las listas standar de JAMedia
        # self.jamediaplayer.pack_standar()
        # self.jamediaplayer.pack_efectos()
        
    NOTA: Tambien se puede ejecutar JAMedia directamente
    mediante python JAMedia.py
    """
        
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """JAMedia: Gtk.Plug para embeber en otra aplicacion."""
        
        Gtk.Plug.__init__(self, 0L)
        
        self.mplayerreproductor = None
        self.jamediareproductor = None
        self.mplayergrabador = None
        self.jamediagrabador = None
        self.player = None
        self.grabador = None
        
        self.toolbar = None
        self.toolbar_accion = None
        self.pantalla = None
        self.barradeprogreso = None
        self.volumen = None
        self.toolbar_list = None
        self.scroll_config = None
        self.toolbar_config = None
        self.widget_efectos = None
        self.toolbar_grabar = None
        self.toolbar_info = None
        self.lista_de_reproduccion = None
        self.evnt_box_lista_reproduccion = None
        self.controlesrepro = None
        self.toolbaraddstream = None
        self.toolbar_salir = None
        self.hbox_efectos_en_pipe = None
        
        self.controles_dinamicos = None
        
        self.vbox_lista_reproduccion = None
        
        self.show_all()
        
        self.connect("embedded", self.embed_event)
        
    def setup_init(self):
        """Se crea la interfaz grafica,
        se setea y se empaqueta todo."""
        
        self.pantalla = Visor()
        self.barradeprogreso = BarraProgreso()
        self.volumen = ControlVolumen()
        self.lista_de_reproduccion = Lista()
        self.controlesrepro = ToolbarReproduccion()
        self.toolbar = Toolbar()
        self.toolbar_config = ToolbarConfig()
        self.widget_efectos = WidgetsGstreamerEfectos()
        self.toolbar_accion = ToolbarAccion()
        self.toolbar_grabar = ToolbarGrabar()
        self.toolbar_info = ToolbarInfo()
        self.toolbaraddstream = ToolbarAddStream()
        self.toolbar_salir = ToolbarSalir()
        
        basebox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        hpanel = Gtk.HPaned()
        basebox.pack_start(self.toolbar, False, False, 0)
        basebox.pack_start(self.toolbar_salir, False, False, 0)
        basebox.pack_start(self.toolbar_accion, False, False, 0)
        basebox.pack_start(self.toolbaraddstream, False, False, 0)
        basebox.pack_start(hpanel, True, True, 0)
        
        # Area Izquierda del Panel
        eventbox = Gtk.EventBox()
        eventbox.modify_bg(0, G.NEGRO)
        
        self.hbox_efectos_en_pipe = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.hbox_efectos_en_pipe.set_size_request(-1, G.get_pixels(0.5))
        
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        scroll.add_with_viewport(eventbox)
        
        eventbox.add(self.hbox_efectos_en_pipe)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        vbox.pack_start(self.toolbar_grabar, False, False, 0)
        vbox.pack_start(self.pantalla, True, True, 0)
        
        vbox.pack_start(scroll, False, False, 0)
        
        vbox.pack_start(self.toolbar_info, False, False, 0)
        ev_box = Gtk.EventBox() # Para poder pintarlo
        ev_box.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        vbox.pack_start(ev_box, False, True, 0)
        hbox_barra_progreso = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        hbox_barra_progreso.pack_start(self.barradeprogreso, True, True, 0)
        hbox_barra_progreso.pack_start(self.volumen, False, False, 0)
        ev_box.add(hbox_barra_progreso)
        hpanel.pack1(vbox, resize = True, shrink = True)
        
        # Area Derecha del Panel
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.vbox_config = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.scroll_config = Gtk.ScrolledWindow()
        self.scroll_config.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scroll_config.add_with_viewport (self.vbox_config)
        
        self.vbox_config.pack_start(self.toolbar_config, False, False, 0)
        #self.vbox_config.pack_start(self.widget_efectos, False, False, 0)
        
        vbox.pack_start(self.scroll_config, True, True, 0)
        
        # Lista de Reproduccion
        self.evnt_box_lista_reproduccion = Gtk.EventBox() # Para poder pintarlo
        #ev_box.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        vbox.pack_start(self.evnt_box_lista_reproduccion, True, True, 0)
        
        self.vbox_lista_reproduccion = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        self.scroll_list = Gtk.ScrolledWindow()
        self.scroll_list.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scroll_list.add_with_viewport (self.lista_de_reproduccion)
        
        self.pack_vbox_lista_reproduccion()
        
        self.evnt_box_lista_reproduccion.add(self.vbox_lista_reproduccion)
        hpanel.pack2(vbox, resize = False, shrink = True)
        
        self.controles_dinamicos = [
            hbox_barra_progreso,
            self.evnt_box_lista_reproduccion,
            self.toolbar,
            self.toolbar_info,
            self.hbox_efectos_en_pipe]
        
        basebox.show_all()
        #self.controlesrepro.botonpausa.hide()
        self.toolbar_salir.hide()
        self.scroll_config.hide()
        self.toolbar_accion.hide()
        self.toolbar_grabar.hide()
        self.toolbaraddstream.hide()
        self.toolbar_info.descarga.hide()
        self.add(basebox)
        
        xid = self.pantalla.get_property('window').get_xid()
        
        # HACK: La aplicación nunca debe explotar :P
        if JAMF.get_programa("mplayer"):
            self.mplayerreproductor = MplayerReproductor(xid)
            
        else:
            self.mplayerreproductor = MplayerReproductor(self.pantalla)
            
        # HACK: La aplicación nunca debe explotar :P
        if JAMF.verificar_Gstreamer():
            self.jamediareproductor = JAMediaReproductor(xid)
            
        else:
            self.jamediareproductor = JAMediaReproductor(self.pantalla)
            
        self.switch_reproductor(None, "JAMediaReproductor") # default Gst.
        
        self.mplayerreproductor.connect("endfile", self.endfile)
        self.mplayerreproductor.connect("estado", self.cambioestadoreproductor)
        self.mplayerreproductor.connect("newposicion", self.update_progress)
        self.mplayerreproductor.connect("volumen", self.get_volumen)
        self.mplayerreproductor.connect("video", self.set_video)
        
        self.jamediareproductor.connect("endfile", self.endfile)
        self.jamediareproductor.connect("estado", self.cambioestadoreproductor)
        self.jamediareproductor.connect("newposicion", self.update_progress)
        self.jamediareproductor.connect("volumen", self.get_volumen)
        self.jamediareproductor.connect("video", self.set_video)
        
        self.lista_de_reproduccion.connect("nueva-seleccion", self.cargar_reproducir)
        self.lista_de_reproduccion.connect("button-press-event", self.click_derecho_en_lista)
        
        self.controlesrepro.connect("activar", self.activar)
        self.barradeprogreso.connect("user-set-value", self.user_set_value)
        self.pantalla.connect("ocultar_controles", self.ocultar_controles)
        self.pantalla.connect("button_press_event", self.clicks_en_pantalla)
        #self.pantalla.connect('expose-event', self.paint_pantalla)
        
        self.toolbar.connect('salir', self.confirmar_salir)
        #self.toolbar.connect('capturar', self.fotografiar)
        self.toolbar.connect('config', self.mostrar_config)
        
        self.toolbar_salir.connect('salir', self.emit_salir)
        self.toolbar_config.connect('reproductor', self.switch_reproductor)
        self.toolbar_config.connect('valor', self.set_balance)
        self.toolbar_info.connect('rotar', self.set_rotacion)
        self.toolbar_info.connect('actualizar_streamings', self.actualizar_streamings)
        self.toolbar_accion.connect("Grabar", self.grabar_streaming)
        self.toolbar_accion.connect("accion-stream", self.accion_stream)
        self.toolbar_grabar.connect("stop", self.detener_grabacion)
        self.volumen.connect("volumen", self.set_volumen)
        self.toolbaraddstream.connect("add-stream", self.ejecutar_add_stream)
        
        self.widget_efectos.connect("click_efecto", self.click_efecto)
        self.widget_efectos.connect('configurar_efecto', self.configurar_efecto)
        
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos", "jamedia_cursor.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        jamedia_cursor = Gdk.Cursor.new_from_pixbuf(
            Gdk.Display.get_default(), pixbuf, 0, 0)
        self.get_parent_window().set_cursor(jamedia_cursor)
        
        #GObject.idle_add(self.cargar_efectos, list(G.JAMedia_VIDEOEFECTOS))
        
    #def fotografiar(self, widget):
    #    """Captura una imagen desde el video en reproduccion."""
        
    #    self.player.fotografiar()
        
    def configurar_efecto(self, widget, nombre_efecto, propiedad, valor):
        """Configura un efecto en el pipe, si no está en eĺ, lo agrega."""

        # Si el efecto no está agregado al pipe, lo agrega
        if self.player.efectos:
            if not nombre_efecto in self.player.efectos:
                self.click_efecto(None, nombre_efecto)
                self.widget_efectos.seleccionar_efecto(nombre_efecto)
                
        else:
            self.click_efecto(None, nombre_efecto)
            self.widget_efectos.seleccionar_efecto(nombre_efecto)

        # Setea el efecto
        self.player.configurar_efecto(nombre_efecto, propiedad, valor)
        
    def click_efecto(self, widget, nombre_efecto):
        """Recibe el nombre del efecto sobre el que
        se ha hecho click y decide si debe agregarse
        al pipe de JAMedia."""
        
        agregar = False
        
        if self.player.efectos:
            if not nombre_efecto in self.player.efectos:
                agregar = True
            
        else:
            agregar = True
            
        if agregar:
            self.player.agregar_efecto( nombre_efecto )
            
            # Agrega un widget a self.hbox_efectos_en_pipe
            botonefecto = WidgetEfecto_en_Pipe()
            botonefecto.set_tooltip(nombre_efecto)
            botonefecto.connect('clicked', self.clicked_mini_efecto)
            lado = G.get_pixels(0.5)
            botonefecto.set_tamanio(lado, lado)
            
            archivo = os.path.join(JAMediaObjectsPath, "Iconos", 'configurar.png')
            
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(archivo, lado, lado)
            botonefecto.imagen.set_from_pixbuf(pixbuf)
            
            self.hbox_efectos_en_pipe.pack_start(botonefecto, False, False, 0)
            
        else:
            self.player.quitar_efecto(nombre_efecto)
            
            self.widget_efectos.des_seleccionar_efecto(nombre_efecto)
            
            # Quitar el widget de self.hbox_efectos_en_pipe
            for efecto in self.hbox_efectos_en_pipe.get_children():
                if efecto.get_tooltip_text() == nombre_efecto:
                    efecto.destroy()
                    break
        
    def clicked_mini_efecto(self, widget, void = None):
        """Cuando se hace click en el mini objeto en pantalla
        para efecto agregado, este se quita del pipe de la cámara."""
        
        nombre_efecto = widget.get_tooltip_text()
        self.player.quitar_efecto(nombre_efecto)
        self.widget_efectos.des_seleccionar_efecto(nombre_efecto)
        widget.destroy()
        
    def cargar_efectos(self, efectos):
        """Agrega los widgets con efectos a la paleta de configuración."""
        
        self.widget_efectos.cargar_efectos(efectos)
        
    def actualizar_streamings(self, widget):
        """Actualiza los streamings de jamedia,
        descargandolos desde su web."""
        
        G.get_streaming_default()
        
    def accion_stream(self, widget, accion, url):
        """Ejecuta una acción sobre un streaming.
        borrar de la lista, eliminar streaming,
        copiar a jamedia, mover a jamedia."""
        
        lista = self.toolbar_list.label.get_text()
        
        if accion == "Borrar":
            G.eliminar_streaming(url, lista)
            
        elif accion == "Copiar":
            modelo, iter = self.lista_de_reproduccion.treeselection.get_selected()
            nombre = modelo.get_value(iter, 1)
            url = modelo.get_value(iter, 2)
            tipo = self.toolbar_list.label.get_text()
            G.add_stream(tipo, [nombre, url])
            
        elif accion == "Mover":
            modelo, iter = self.lista_de_reproduccion.treeselection.get_selected()
            nombre = modelo.get_value(iter, 1)
            url = modelo.get_value(iter, 2)
            tipo = self.toolbar_list.label.get_text()
            G.add_stream(tipo, [nombre, url])
            G.eliminar_streaming(url, lista)
            
        else:
            print "accion_stream desconocido:", accion
            
    def ejecutar_add_stream(self, widget, tipo, nombre, url):
        """Ejecuta agregar stream, de acuerdo a los datos
        que pasa toolbaraddstream en add-stream."""
        
        G.add_stream(tipo, [nombre, url])
        
        if "Tv" in tipo or "TV" in tipo:
            indice = 3
            
        elif "Radio" in tipo:
            indice = 2
            
        else:
            return
        
        self.cargar_lista(None, indice)
        
    def set_rotacion(self, widget, valor):
        """ Recibe la señal de rotacion de la toolbar y
        envia la rotacion al Reproductor. """
        
        self.player.rotar(valor)
        
    def set_balance(self, widget, valor, tipo):
        """ Setea valores en Balance de Video, pasando
        los valores que recibe de la toolbar (% float)."""
        
        if tipo == "saturacion": self.player.set_balance(saturacion = valor)
        if tipo == "contraste": self.player.set_balance(contraste = valor)
        if tipo == "brillo": self.player.set_balance(brillo = valor)
        if tipo == "hue": self.player.set_balance(hue = valor)
        if tipo == "gamma": self.player.set_balance(gamma = valor)
        
    def pack_vbox_lista_reproduccion(self):
        """Empaqueta la lista de reproduccion.
        Se hace a parte porque la toolbar de la lista no debe
        empaquetarse cuando JAMedia es embebida en otra aplicacion."""
        
        self.vbox_lista_reproduccion.pack_start(self.scroll_list,
            True, True, 0)
        self.vbox_lista_reproduccion.pack_end(self.controlesrepro,
            False, True, 0)
            
    def clicks_en_pantalla(self, widget, event):
        """Hace fullscreen y unfullscreen sobre la
        ventana principal donde JAMedia está embebida
        cuando el usuario hace doble click en el visor."""
        
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w,h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            
            if ww == w and hh == h:
                ventana.unfullscreen()
                ventana.set_border_width(2)
                
            else:
                ventana.fullscreen()
                ventana.set_border_width(0)
                
    def mostrar_config(self, widget):
        """Muestra u oculta las opciones de
        configuracion (toolbar_config y widget_efectos)."""
        
        map(self.ocultar, [
            self.toolbar_accion,
            self.toolbaraddstream,
            self.toolbar_salir])
            
        if self.scroll_config.get_visible():
            self.scroll_config.hide()
            self.evnt_box_lista_reproduccion.show()
            
        else:
            rect = self.evnt_box_lista_reproduccion.get_allocation()
            self.scroll_config.set_size_request(rect.width, -1)
            self.evnt_box_lista_reproduccion.hide()
            self.scroll_config.show()
            GObject.idle_add(self.update_balance_toolbars)
            
    def switch_reproductor(self, widget, nombre):
        """Recibe la señal "reproductor" desde toolbar_config y
        cambia el reproductor que se utiliza, entre mplayer y
        jamediareproductor (Gst 1.0)."""
        
        reproductor = self.player
        
        # HACK: JAMediaReproductor no funciona con Tv.
        if reproductor == self.mplayerreproductor and \
            ("TV" in self.toolbar_list.label.get_text() or \
            "Tv" in self.toolbar_list.label.get_text()):
                self.toolbar_config.mplayer_boton.set_active(True)
                self.toolbar_config.jamedia_boton.set_active(False)
                return
            
        if nombre == "MplayerReproductor":
            if JAMF.get_programa('mplayer'):
                reproductor = self.mplayerreproductor
                self.toolbar_info.set_reproductor("MplayerReproductor")
                self.toolbar_config.mplayer_boton.set_active(True)
                
            else:
                reproductor = self.jamediareproductor
                self.toolbar_info.set_reproductor("JAMediaReproductor")
                self.toolbar_config.jamedia_boton.set_active(True)
                
        elif nombre == "JAMediaReproductor":
            reproductor = self.jamediareproductor
            self.toolbar_info.set_reproductor("JAMediaReproductor")
            self.toolbar_config.jamedia_boton.set_active(True)
            
        if self.player != reproductor:
            try:
                self.player.stop()
                
            except:
                pass
            
            self.player = reproductor
            print "Reproduciendo con:", self.player.name
            
            try:
                model, iter = self.lista_de_reproduccion.treeselection.get_selected()
                valor = model.get_value(iter, 2)
                self.player.load(valor)
                
            except:
                pass

    def embed_event(self, widget):
        """No hace nada por ahora."""
        
        print "JAMediaPlayer => OK"
        
    def ocultar_controles(self, widget, valor):
        """Oculta o muestra los controles."""
        
        zona, ocultar = (valor, self.toolbar_info.ocultar_controles)
        
        if zona and ocultar:
            map(self.ocultar, [
                self.scroll_config,
                self.toolbar_accion,
                self.toolbaraddstream,
                self.toolbar_salir])
                
            map(self.ocultar, self.controles_dinamicos)
            
        elif zona and not ocultar:
            pass
        
        elif not zona and ocultar:
            self.scroll_config.hide()
            map(self.mostrar, self.controles_dinamicos)
            
        elif not zona and not ocultar:
            pass
        
    def ocultar(self, objeto):
        """Esta funcion es llamada desde self.ocultar_controles()"""
        
        if objeto.get_visible(): objeto.hide()
        
    def mostrar(self, objeto):
        """Esta funcion es llamada desde self.ocultar_controles()"""
        
        if not objeto.get_visible(): objeto.show()
        
    def activar(self, widget= None, senial= None):
        """
        Recibe:
            "atras", "siguiente", "stop" o "pause-play"
            
        desde la toolbar de reproduccion y ejecuta:
            atras o siguiente sobre la lista de reproduccion y
            stop o pause-play sobre el reproductor.
        """
        
        if not self.lista_de_reproduccion.modelo.get_iter_first():
            return
        
        if senial == "atras":
            self.lista_de_reproduccion.seleccionar_anterior()
            
        elif senial == "siguiente":
            self.lista_de_reproduccion.seleccionar_siguiente()
            
        elif senial == "stop":
            self.player.stop()
            
        elif senial == "pausa-play":
            self.player.pause_play()
        
    def endfile(self, widget = None, senial = None):
        """Recibe la señal de fin de archivo desde el reproductor
        y llama a seleccionar_siguiente en la lista de reproduccion."""
        
        self.controlesrepro.set_paused()
        GObject.idle_add(self.lista_de_reproduccion.seleccionar_siguiente)
        
    def cambioestadoreproductor(self, widget = None, valor = None):
        """Recibe los cambios de estado del reproductor (paused y playing)
        y actualiza la imagen del boton play en la toolbar de reproduccion."""
        
        if "playing" in valor:
            self.controlesrepro.set_playing()
            
        elif "paused" in valor or "None" in valor:
            self.controlesrepro.set_paused()
            
        else:
            print "Estado del Reproductor desconocido:", valor
            
        GObject.idle_add(self.update_balance_toolbars)
        
    def update_balance_toolbars(self):
        """Actualiza las toolbars de balance en video."""
        
        config = self.player.get_balance()
        
        self.toolbar_config.set_balance(
            brillo = config['brillo'],
            contraste = config['contraste'],
            saturacion = config['saturacion'],
            hue = config['hue'],
            gamma = config['gamma'])
            
    def update_progress(self, objetoemisor, valor):
        """Recibe el progreso de la reproduccion desde el reproductor
        y actualiza la barra de progreso."""
        
        self.barradeprogreso.set_progress(float(valor))
    
    def user_set_value(self, widget= None, valor= None):
        """Recibe la posicion en la barra de progreso cuando
        el usuario la desplaza y hace "seek" sobre el reproductor."""
        
        self.player.set_position(valor)
        
    def pack_standar(self):
        """Re empaqueta algunos controles de JAMedia.
        Cuando JAMedia no está embebido, tiene su toolbar_list"""
        
        G.set_listas_default()
        
        self.toolbar_list = ToolbarLista()
        self.toolbar_list.connect("cargar_lista", self.cargar_lista)
        self.toolbar_list.connect("add_stream", self.add_stream)
        self.toolbar_list.show_all()
        self.toolbar_list.boton_agregar.hide()
        self.toolbar_info.descarga.show()
        
        for child in self.vbox_lista_reproduccion.get_children():
            self.vbox_lista_reproduccion.remove(child)
            
        self.vbox_lista_reproduccion.pack_start (self.toolbar_list,
            False, False, 0)
        self.pack_vbox_lista_reproduccion()
        
    def pack_efectos(self):
        
        self.vbox_config.pack_start(self.widget_efectos, False, False, 0)
        GObject.idle_add(self.cargar_efectos, list(G.JAMedia_VIDEOEFECTOS))
        
    def add_stream(self, widget):
        """Recibe la señal add_stream desde toolbarlist
        y abre la toolbar que permite agregar un stream."""
        
        map(self.ocultar, [
            self.scroll_config,
            self.toolbar_accion])
            
        if not self.toolbaraddstream.get_visible():
            accion = widget.label.get_text()
            self.toolbaraddstream.set_accion(accion)
            self.toolbaraddstream.show()
            
        else:
            self.toolbaraddstream.hide()
            
    def set_nueva_lista(self, lista):
        """Carga una lista de archivos directamente, sin
        utilizar la toolbarlist, esto es porque: cuando
        jamedia está embebido, no tiene la toolbar_list"""
        
        if not lista: return
        self.player.stop()
        self.lista_de_reproduccion.limpiar()
        self.lista_de_reproduccion.agregar_items(lista)
        if self.toolbar_list: self.toolbar_list.label.set_text("")

    def cargar_reproducir(self, widget, path):
        """Recibe lo que se selecciona en la lista de
        reproduccion y lo manda al reproductor."""
        
        # HACK: Cuando cambia de pista se deben
        # reestablecer los valores de balance para
        # que no cuelgue la aplicación, por lo tanto,
        # el usuario no puede estar modificando estos
        # valores en el momento en que cambia la pista
        # en el reproductor.
        
        visible = self.scroll_config.get_visible()
        if visible: self.scroll_config.hide()
        
        self.player.load(path)
        
        if visible: self.scroll_config.show()
        
    def confirmar_salir(self, widget = None, senial = None):
        """Recibe salir y lo pasa a la toolbar de confirmación."""
        
        map(self.ocultar, [self.toolbaraddstream])
            
        self.toolbar_salir.run("JAMedia")
        
    def emit_salir(self, widget):
        """Emite salir para que cuando esta embebida, la
        aplicacion decida que hacer, si salir, o cerrar solo
        JAMedia."""
        
        if self.grabador != None:
            self.grabador.stop()
        self.lista_de_reproduccion.limpiar()
        self.player.stop()
        
        self.emit('salir')
        
    def cargar_lista(self, widget, indice):
        """Recibe el indice seleccionado en el menu de toolbarlist y
        carga la lista correspondiente.
        
        Esto es solo para JAMedia no embebido ya que cuando JAMedia
        esta embebida, no posee la toolbarlist."""
        
        model, iter = self.lista_de_reproduccion.treeselection.get_selected()
        ultimopath = False
        
        if model and iter:
            valor = model.get_value(iter, 2)
            
            if valor:
                descripcion = JAMF.describe_uri(valor)
                
                if descripcion:
                    if descripcion[2]:
                        ultimopath = valor
                
        map(self.ocultar, [
            self.toolbar_accion,
            self.toolbaraddstream])
            
        self.toolbar_list.boton_agregar.hide()
        
        self.lista_de_reproduccion.limpiar()
        self.player.stop()
        
        if indice == 0:
            archivo = os.path.join(G.DIRECTORIO_DATOS, 'JAMediaRadio.JAMedia')
            self.seleccionar_lista_de_stream(archivo, "JAM-Radio")
            
        elif indice == 1:
            # HACK: Tv no funciona con JAMediaReproductor.
            if self.player == self.jamediareproductor:
                self.switch_reproductor(None, "MplayerReproductor")
                
            archivo = os.path.join(G.DIRECTORIO_DATOS, 'JAMediaTV.JAMedia')
            self.seleccionar_lista_de_stream(archivo, "JAM-TV")
            
        elif indice == 2:
            archivo = os.path.join(G.DIRECTORIO_DATOS, 'MisRadios.JAMedia')
            self.seleccionar_lista_de_stream(archivo, "Radios")
            self.toolbar_list.boton_agregar.show()
            
        elif indice == 3:
            # HACK: Tv no funciona con JAMediaReproductor.
            if self.player == self.jamediareproductor:
                self.switch_reproductor(None, "MplayerReproductor")
                
            archivo = os.path.join(G.DIRECTORIO_DATOS, 'MisTvs.JAMedia')
            self.seleccionar_lista_de_stream(archivo, "TVs")
            self.toolbar_list.boton_agregar.show()
            
        elif indice == 4:
            self.seleccionar_lista_de_archivos(G.DIRECTORIO_MIS_ARCHIVOS,
                "Archivos")
                
        elif indice == 5:
            self.seleccionar_lista_de_archivos(G.DIRECTORIO_YOUTUBE,
                "JAM-Tube")
                
        elif indice == 6:
            self.seleccionar_lista_de_archivos(G.AUDIO_JAMEDIA_VIDEO,
                "JAM-Audio")
                
        elif indice == 7:
            self.seleccionar_lista_de_archivos(G.VIDEO_JAMEDIA_VIDEO,
                "JAM-Video")
                
        elif indice == 8:
            selector = Selector_de_Archivos(self)
            
            if ultimopath:
                directorio = "file://%s" % os.path.dirname(ultimopath)
                selector.set_current_folder_uri(directorio)
                
            selector.connect('archivos-seleccionados', self.cargar_directorio)
            
    def cargar_directorio(self, widget, archivos):
        """Recibe una lista de archivos y setea la lista
        de reproduccion con ellos."""
        
        if not archivos: return
        items = []
        
        for archivo in archivos:
            path = archivo
            archivo = os.path.basename(path)
            items.append( [archivo,path] )
            
        self.set_nueva_lista(items)
        
    def seleccionar_lista_de_archivos(self, directorio, titulo):
        """Responde a la seleccion en el menu de la toolbarlist.
        
        Recibe un directorio para generar una lista de archivos
        y setear la lista de reproduccion con ellos y recibe un titulo
        para la lista cargada.
        
        Esto es solo para las listas standar de JAMedia no embebido."""
        
        archivos = sorted(os.listdir(directorio))
        lista = []
        
        for texto in archivos:
            url = os.path.join(directorio, texto)
            elemento = [texto, url]
            lista.append(elemento)
            
        self.lista_de_reproduccion.agregar_items(lista)
        self.toolbar_list.label.set_text(titulo)

    def seleccionar_lista_de_stream(self, archivo, titulo):
        """Responde a la seleccion en el menu de la toolbarlist.
        
        Recibe un archivo desde donde cargar una lista de
        streamings, carga los streamings y los pasa a la lista de
        reproduccion, y recibe un titulo para la nueva lista.
        
        Esto es solo para las listas standar de JAMedia no embebido."""
        
        items = G.get_streamings(archivo)
        
        self.lista_de_reproduccion.agregar_items(items)
        self.toolbar_list.label.set_text(titulo)
        
    def click_derecho_en_lista(self, widget, event):
        """Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista de reproduccion, permitiendo copiar, mover y
        borrar el archivo o streaming o simplemente quitarlo
        de la lista."""
        
        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)
        
        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(int(pos[0]), int(pos[1]))
            
        except:
            return
        
        # TreeView.get_path_at_pos(event.x, event.y) devuelve:
        # * La ruta de acceso en el punto especificado (x, y), en relación con las coordenadas widget
        # * El gtk.TreeViewColumn en ese punto
        # * La coordenada X en relación con el fondo de la celda
        # * La coordenada Y en relación con el fondo de la celda
        
        if boton == 1:
            return
        
        elif boton == 3:
            menu = MenuList(widget, boton, pos, tiempo, path, widget.modelo)
            menu.connect('accion', self.set_accion)
            menu.popup(None, None, None, None, boton, tiempo)
            
        elif boton == 2:
            return
        
    def set_accion(self, widget, lista, accion, iter):
        """Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.
        
        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar."""
        
        self.toolbar_accion.set_accion(lista, accion, iter)
        
    def grabar_streaming(self, widget, uri):
        """Se ha confirmado grabar desde un streaming en
        la toolbar_accion."""
        
        self.detener_grabacion()
        
        extension = ""
        if "TV" in self.toolbar_list.label.get_text() or \
            "Tv" in self.toolbar_list.label.get_text():
                extension = ".avi"
                
        else:
            extension = ".mp3"
            
        hora = time.strftime("%H-%M-%S")
        fecha = str(datetime.date.today())
        
        archivo = "%s-%s-%s" % (fecha, hora, extension)
        archivo = os.path.join(G.DIRECTORIO_MIS_ARCHIVOS, archivo)
        
        if self.player == self.jamediareproductor:
            self.grabador = JAMediaGrabador(uri, archivo)
            
        elif self.player == self.mplayerreproductor:
            self.grabador = MplayerGrabador(uri, archivo)
            
        self.grabador.connect('update', self.update_grabador)
    
    def update_grabador(self, widget, datos):
        """Actualiza informacion de Grabacion en proceso."""
        
        self.toolbar_grabar.set_info(datos)
    
    def detener_grabacion(self, widget= None):
        """Detiene la Grabación en Proceso."""
        
        if self.grabador != None:
            self.grabador.stop()
            
        self.toolbar_grabar.stop()
        
    def set_volumen(self, widget, valor):
        """Cuando el usuario cambia el volumen."""
        
        valor = valor * 100
        self.player.set_volumen(valor)
        
    def get_volumen(self, widget, valor):
        """El volumen con el que se reproduce actualmente."""
        
        self.volumen.set_value(valor)
        
    def set_video(self, widget, valor):
        """Si hay video o no en la fuente . . ."""
        
        print "Video en la Fuente:", valor
        #if not valor: self.player.link_visualizador()
        