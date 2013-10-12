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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GLib

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaObjects.JAMFileSystem import get_programa
from JAMediaObjects.JAMFileSystem import verificar_Gstreamer

# HACK: La aplicación nunca debe explotar :P
if get_programa("mplayer"):
    from JAMediaObjects.MplayerReproductor import MplayerReproductor
    from JAMediaObjects.MplayerReproductor import MplayerGrabador
    
else:
    from JAMediaObjects.PlayerNull import MplayerReproductor
    from JAMediaObjects.PlayerNull import MplayerGrabador
    
# HACK: La aplicación nunca debe explotar :P
if verificar_Gstreamer():
    from JAMediaObjects.JAMediaReproductor import JAMediaReproductor
    from JAMediaObjects.JAMediaReproductor import JAMediaGrabador
    
else:
    from JAMediaObjects.PlayerNull import JAMediaReproductor
    from JAMediaObjects.PlayerNull import JAMediaGrabador
    
from JAMediaObjects.JAMediaGlobales import get_color
from JAMediaObjects.JAMediaGlobales import get_pixels

screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()
style_path = os.path.join(JAMediaObjectsPath, "JAMedia.css")
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
    
#GObject.threads_init()
#Gdk.threads_init()

class JAMediaPlayer(Gtk.Plug):
    """
    JAMedia:
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
        
    GLib.idle_add(self.setup_init)
        
    def setup_init(self):
        self.jamediaplayer.setup_init()
        # Empaqueta las listas standar de JAMedia
        # self.jamediaplayer.pack_standar()
        # self.jamediaplayer.pack_efectos()
        
    NOTA: Tambien se puede ejecutar JAMedia directamente
    mediante python JAMedia.py
    """
    
    __gtype_name__ = 'JAMediaPlayer'
    
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        """
        JAMedia: Gtk.Plug para embeber en otra aplicacion.
        """
        
        Gtk.Plug.__init__(self, 0L)
        
        self.pantalla = None                # visor para gstreamer
        self.barradeprogreso = None         # progreso de reproducción
        self.volumen = None                 # volumen de audio
        self.lista_de_reproduccion = None   # lista de reproducción
        self.controlesrepro = None          # controles de reproducción
        
        self.toolbar = None             # toolbar principal
        self.toolbar_list = None        # Para el nombre de la lista . . .
        self.toolbar_config = None      # control de balance y gamma
        self.widget_efectos = None      # efectos gráficos
        self.toolbar_accion = None      # para confirmar acciones ejem: salir
        self.toolbar_grabar = None      # informa sobre grabacion en progreso
        self.toolbar_info = None        # rotar, ocultar controles, etc
        self.toolbaraddstream = None    # agregar un stream
        self.toolbar_salir = None       # confirmar salir
        
        self.derecha_vbox = None                # Contiene todos los widgets de la derecha
        self.hbox_efectos_en_pipe = None        # informa sobre efectos que se aplican
        self.vbox_config = None                 # contiene balance y efectos
        self.scroll_config = None               # contiene self.vbox_config
        # FIXME: Quitarlo, solo mantiene el gris de fondo para los botones en controles de reproducción.
        self.evnt_box_lista_reproduccion = None # contiene self.vbox_lista_reproduccion
        self.scroll_list = None                 # contiene self.lista_de_reproduccion
        
        self.controles_dinamicos = None # controles que se ocultan o muestran segun config
        
        self.mplayerreproductor = None  # mplayer
        self.jamediareproductor = None  # Gstreamer 1.0
        self.mplayergrabador = None     # grabador mplayer
        self.jamediagrabador = None     # grabador Gstreamer 1.0
        self.player = None              # reproductor actual mplayer o Gstreamer 1.0
        self.grabador = None            # grabador actual mplayer o Gstreamer 1.0
        
        self.cursor_root = None         # cursor de aplicacion que embebe a jamedia.
        self.jamedia_cursor = None      # cursor de jamedia
        self.mouse_in_visor = False     # flag, el mouse se oculta sobre el visor
        
        self.show_all()
        
        self.connect("embedded", self.__embed_event)
        
    def setup_init(self):
        """
        Se crea la interfaz grafica,
        se setea y se empaqueta todo.
        """
        
        self.get_toplevel().set_sensitive(False)
        
        from JAMediaObjects.JAMediaWidgets import Visor
        from JAMediaObjects.JAMediaWidgets import BarraProgreso
        from JAMediaObjects.JAMediaWidgets import ControlVolumen
        from JAMediaObjects.JAMediaWidgets import Lista
        from JAMediaObjects.JAMediaWidgets import ToolbarReproduccion
        from JAMediaObjects.JAMediaWidgets import WidgetsGstreamerEfectos
        from JAMediaObjects.JAMediaWidgets import ToolbarAccion
        from JAMediaObjects.JAMediaWidgets import ToolbarSalir
        
        from Widgets import Toolbar
        from Widgets import ToolbarConfig
        from Widgets import ToolbarGrabar
        from Widgets import ToolbarInfo
        from Widgets import ToolbarAddStream
        
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
        hpanel = Gtk.Paned(orientation = Gtk.Orientation.HORIZONTAL)
        
        basebox.pack_start(self.toolbar, False, False, 0)
        basebox.pack_start(self.toolbar_salir, False, False, 0)
        basebox.pack_start(self.toolbar_accion, False, False, 0)
        basebox.pack_start(self.toolbaraddstream, False, False, 0)
        
        basebox.pack_start(hpanel, True, True, 0)
        
        ### Area Izquierda del Panel
        
        ### Efectos que se están aplicando.
        eventbox = Gtk.EventBox() # FIXME: Mantiene el fondo negro en miniefectos que se aplican
        eventbox.modify_bg(0, get_color("NEGRO"))
        self.hbox_efectos_en_pipe = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL)
        self.hbox_efectos_en_pipe.set_size_request(-1, get_pixels(0.5))
        eventbox.add(self.hbox_efectos_en_pipe)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.NEVER)
        scroll.add_with_viewport(eventbox)
        
        ### Barra de Progreso + Volúmen
        ev_box = Gtk.EventBox() # FIXME: Para poder pintar el fondo de volumen
        ev_box.modify_bg(0, get_color("BLANCO"))
        hbox_barra_progreso = Gtk.Box(
            orientation = Gtk.Orientation.HORIZONTAL)
        hbox_barra_progreso.pack_start(self.barradeprogreso, True, True, 0)
        hbox_barra_progreso.pack_start(self.volumen, False, False, 0)
        ev_box.add(hbox_barra_progreso)
        
        ### Todo
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        vbox.pack_start(self.toolbar_grabar, False, False, 0)
        vbox.pack_start(self.pantalla, True, True, 0)
        vbox.pack_start(scroll, False, False, 0)
        vbox.pack_start(self.toolbar_info, False, False, 0)
        vbox.pack_start(ev_box, False, True, 0)
        
        hpanel.pack1(vbox, resize = True, shrink = True)
        
        ### Area Derecha del Panel
        self.derecha_vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        
        ### Configuración de balanace y efectos
        self.vbox_config = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.scroll_config = Gtk.ScrolledWindow()
        self.scroll_config.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        self.scroll_config.add_with_viewport (self.vbox_config)
        self.vbox_config.pack_start(self.toolbar_config, False, False, 0)
        #self.vbox_config.pack_start(self.widget_efectos, False, False, 0)
        
        ### Lista de Reproducción
        self.evnt_box_lista_reproduccion = Gtk.EventBox() # FIXME: Para poder pintar el fondo
        self.vbox_lista_reproduccion = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.scroll_list = Gtk.ScrolledWindow()
        self.scroll_list.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC)
        self.scroll_list.add(self.lista_de_reproduccion)
        self.__pack_vbox_lista_reproduccion() # Lista + Controles de Reproducción
        self.evnt_box_lista_reproduccion.add(self.vbox_lista_reproduccion)
        
        ### Configuración + Lista de Reproducción.
        self.derecha_vbox.pack_start(self.scroll_config, True, True, 0)
        self.derecha_vbox.pack_start(self.evnt_box_lista_reproduccion, True, True, 0)
        
        hpanel.pack2(self.derecha_vbox, resize = False, shrink = True)
        
        self.controles_dinamicos = [
            hbox_barra_progreso,
            self.derecha_vbox,
            self.toolbar,
            self.toolbar_info,
            self.hbox_efectos_en_pipe]
        
        basebox.show_all()
        
        map(self.__ocultar,
            [self.toolbar_salir,
            self.scroll_config,
            self.toolbar_accion,
            self.toolbar_grabar,
            self.toolbaraddstream,
            self.toolbar_info.descarga])
            
        self.add(basebox)
        
        from gi.repository import GdkX11
        
        xid = self.pantalla.get_property('window').get_xid()
        
        # HACK: La aplicación nunca debe explotar :P
        if get_programa("mplayer"):
            self.mplayerreproductor = MplayerReproductor(xid)
            
        else:
            self.mplayerreproductor = MplayerReproductor(self.pantalla)
            
        # HACK: La aplicación nunca debe explotar :P
        if verificar_Gstreamer():
            self.jamediareproductor = JAMediaReproductor(xid)
            
        else:
            self.jamediareproductor = JAMediaReproductor(self.pantalla)
            
        self.switch_reproductor(None, "JAMediaReproductor") # default Gst.
        
        self.mplayerreproductor.connect("endfile", self.__endfile)
        self.mplayerreproductor.connect("estado", self.__cambioestadoreproductor)
        self.mplayerreproductor.connect("newposicion", self.__update_progress)
        self.mplayerreproductor.connect("volumen", self.__get_volumen)
        self.mplayerreproductor.connect("video", self.__set_video)
        
        self.jamediareproductor.connect("endfile", self.__endfile)
        self.jamediareproductor.connect("estado", self.__cambioestadoreproductor)
        self.jamediareproductor.connect("newposicion", self.__update_progress)
        self.jamediareproductor.connect("volumen", self.__get_volumen)
        self.jamediareproductor.connect("video", self.__set_video)
        
        self.lista_de_reproduccion.connect("nueva-seleccion", self.__cargar_reproducir)
        self.lista_de_reproduccion.connect("button-press-event", self.__click_derecho_en_lista)
        
        self.controlesrepro.connect("activar", self.__activar)
        self.barradeprogreso.connect("user-set-value", self.__user_set_value)
        self.pantalla.connect("ocultar_controles", self.__ocultar_controles)
        self.pantalla.connect("button_press_event", self.__clicks_en_pantalla)
        #self.pantalla.connect('expose-event', self.paint_pantalla)
        
        self.toolbar.connect('salir', self.confirmar_salir)
        #self.toolbar.connect('capturar', self.fotografiar)
        self.toolbar.connect('config', self.__mostrar_config)
        
        self.toolbar_salir.connect('salir', self.__emit_salir)
        self.toolbar_config.connect('reproductor', self.switch_reproductor)
        self.toolbar_config.connect('valor', self.__set_balance)
        self.toolbar_info.connect('rotar', self.__set_rotacion)
        self.toolbar_info.connect('actualizar_streamings', self.__actualizar_streamings)
        self.toolbar_accion.connect("Grabar", self.__grabar_streaming)
        self.toolbar_accion.connect("accion-stream", self.__accion_stream)
        self.toolbar_grabar.connect("stop", self.__detener_grabacion)
        self.volumen.connect("volumen", self.__set_volumen)
        self.toolbaraddstream.connect("add-stream", self.__ejecutar_add_stream)
        
        self.widget_efectos.connect("click_efecto", self.__click_efecto)
        self.widget_efectos.connect('configurar_efecto', self.__configurar_efecto)
        
        ### Controlador del mouse.
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos", "jamedia_cursor.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(0.8))
        self.jamedia_cursor = Gdk.Cursor.new_from_pixbuf(
            Gdk.Display.get_default(), pixbuf, 0, 0)
        
        self.cursor_root = self.get_parent_window().get_cursor()
        
        self.get_parent_window().set_cursor(self.jamedia_cursor)
        
        from JAMediaObjects.JAMediaWidgets import MouseSpeedDetector
        
        self.mouse_listener = MouseSpeedDetector(self)
        self.mouse_listener.connect("estado", self.__set_mouse)
        self.mouse_listener.new_handler(True)
        
        self.get_parent().connect("hide", self.__hide_show_parent)
        self.get_parent().connect("show", self.__hide_show_parent)
        
        self.get_toplevel().set_sensitive(True)
        
    # FIXME: La idea es utilizar gdkpixbufsink en el pipe.
    #def fotografiar(self, widget):
    #    """
    #    Captura una imagen desde el video en reproduccion.
    #    """
    
    #    self.player.fotografiar()
    
    def __hide_show_parent(self, widget):
        """
        Controlador del mouse funcionará solo si
        JAMedia es Visible.
        """
        
        self.mouse_listener.new_handler(widget.get_visible())
        
    def __set_mouse(self, widget, estado):
        """
        Muestra u oculta el mouse de jamedia
        según su posición.
        """
        
        if self.mouse_in_visor: ### Solo cuando el mouse está sobre el Visor.
            if estado == "moviendose":
                if self.get_parent_window().get_cursor() != self.jamedia_cursor:
                    self.get_parent_window().set_cursor(
                        self.jamedia_cursor)
                    return
                    
            elif estado == "detenido":
                if self.get_parent_window().get_cursor() != Gdk.CursorType.BLANK_CURSOR:
                    self.get_parent_window().set_cursor(
                        Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR))
                    return
                
            elif estado == "fuera":
                if self.get_parent_window().get_cursor() != self.cursor_root:
                    self.get_parent_window().set_cursor(
                        self.cursor_root)
                    return
            
        else:
            if estado == "moviendose" or "detenido":
                if self.get_parent_window().get_cursor() != self.jamedia_cursor:
                        self.get_parent_window().set_cursor(
                            self.jamedia_cursor)
                        return
                    
            elif estado == "fuera":
                if self.get_parent_window().get_cursor() != self.cursor_root:
                    self.get_parent_window().set_cursor(
                        self.cursor_root)
                    return
                
    def __cancel_toolbars_flotantes(self, widget = None):
        """
        Asegura un widget flotante a la vez.
        """
        
        self.toolbaraddstream.cancelar()
        self.__cancel_toolbar()
        
    def __cancel_toolbar(self, widget = None):
        """
        Asegura un widget flotante a la vez.
        """
        
        self.toolbar_accion.cancelar()
        self.toolbar_salir.cancelar()
        
    def __configurar_efecto(self, widget, nombre_efecto, propiedad, valor):
        """
        Configura un efecto en el pipe, si no está en eĺ, lo agrega.
        """

        # Si el efecto no está agregado al pipe, lo agrega
        if self.player.efectos:
            if not nombre_efecto in self.player.efectos:
                self.__click_efecto(None, nombre_efecto)
                self.widget_efectos.seleccionar_efecto(nombre_efecto)
                
        else:
            self.__click_efecto(None, nombre_efecto)
            self.widget_efectos.seleccionar_efecto(nombre_efecto)

        # Setea el efecto
        self.player.configurar_efecto(nombre_efecto, propiedad, valor)
        
    def __click_efecto(self, widget, nombre_efecto):
        """
        Recibe el nombre del efecto sobre el que
        se ha hecho click y decide si debe agregarse
        al pipe de JAMedia.
        """
        
        self.get_toplevel().set_sensitive(False)
        
        self.__cancel_toolbars_flotantes()
        
        agregar = False
        
        if self.player.efectos:
            if not nombre_efecto in self.player.efectos:
                agregar = True
            
        else:
            agregar = True
            
        if agregar:
            self.player.agregar_efecto( nombre_efecto )
            
            from Widgets import WidgetEfecto_en_Pipe
            
            # Agrega un widget a self.hbox_efectos_en_pipe
            botonefecto = WidgetEfecto_en_Pipe()
            botonefecto.set_tooltip(nombre_efecto)
            botonefecto.connect('clicked', self.__clicked_mini_efecto)
            lado = get_pixels(0.5)
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
        
        self.get_toplevel().set_sensitive(True)
        
    def __clicked_mini_efecto(self, widget, void = None):
        """
        Cuando se hace click en el mini objeto en pantalla
        para efecto agregado, este se quita del pipe de la cámara.
        """
        
        self.__cancel_toolbars_flotantes()
        
        nombre_efecto = widget.get_tooltip_text()
        self.player.quitar_efecto(nombre_efecto)
        self.widget_efectos.des_seleccionar_efecto(nombre_efecto)
        widget.destroy()
        
    def __cargar_efectos(self, efectos):
        """
        Agrega los widgets con efectos a la paleta de configuración.
        """
        
        self.widget_efectos.cargar_efectos(efectos)
        
        return False
    
    def __actualizar_streamings(self, widget):
        """
        Actualiza los streamings de jamedia,
        descargandolos desde su web.
        """
        
        self.__cancel_toolbars_flotantes()
        
        from Widgets import DialogoDescarga
        
        dialog = DialogoDescarga(parent = self.get_toplevel())
        dialog.run()
        
    def __accion_stream(self, widget, accion, url):
        """
        Ejecuta una acción sobre un streaming.
        borrar de la lista, eliminar streaming,
        copiar a jamedia, mover a jamedia.
        """
        
        lista = self.toolbar_list.label.get_text()
        
        from JAMediaObjects.JAMediaGlobales import eliminar_streaming
        from JAMediaObjects.JAMediaGlobales import add_stream
        
        if accion == "Borrar":
            eliminar_streaming(url, lista)
            print "Streaming Eliminado:", url
            
        elif accion == "Copiar":
            modelo, iter = self.lista_de_reproduccion.treeselection.get_selected()
            nombre = modelo.get_value(iter, 1)
            url = modelo.get_value(iter, 2)
            tipo = self.toolbar_list.label.get_text()
            add_stream(tipo, [nombre, url])
            
        elif accion == "Mover":
            modelo, iter = self.lista_de_reproduccion.treeselection.get_selected()
            nombre = modelo.get_value(iter, 1)
            url = modelo.get_value(iter, 2)
            tipo = self.toolbar_list.label.get_text()
            add_stream(tipo, [nombre, url])
            eliminar_streaming(url, lista)
            
        else:
            print "accion_stream desconocido:", accion
            
    def __ejecutar_add_stream(self, widget, tipo, nombre, url):
        """
        Ejecuta agregar stream, de acuerdo a los datos
        que pasa toolbaraddstream en add-stream.
        """
        
        from JAMediaObjects.JAMediaGlobales import add_stream
        add_stream(tipo, [nombre, url])
        
        if "Tv" in tipo or "TV" in tipo:
            indice = 3
            
        elif "Radio" in tipo:
            indice = 2
            
        else:
            return
        
        self.cargar_lista(None, indice)
        
    def __set_rotacion(self, widget, valor):
        """
        Recibe la señal de rotacion de la toolbar y
        envia la rotacion al Reproductor.
        """
        
        self.get_toplevel().set_sensitive(False)
        
        self.__cancel_toolbars_flotantes()
        
        self.player.rotar(valor)
        
        self.get_toplevel().set_sensitive(True)
        
    def __set_balance(self, widget, valor, tipo):
        """
        Setea valores en Balance de Video, pasando
        los valores que recibe de la toolbar (% float).
        """
        
        self.__cancel_toolbars_flotantes()
        
        if tipo == "saturacion": self.player.set_balance(saturacion = valor)
        if tipo == "contraste": self.player.set_balance(contraste = valor)
        if tipo == "brillo": self.player.set_balance(brillo = valor)
        if tipo == "hue": self.player.set_balance(hue = valor)
        if tipo == "gamma": self.player.set_balance(gamma = valor)
        
    def __pack_vbox_lista_reproduccion(self):
        """
        Empaqueta la lista de reproduccion.
        Se hace a parte porque la toolbar de la lista no debe
        empaquetarse cuando JAMedia es embebida en otra aplicacion.
        """
        
        self.vbox_lista_reproduccion.pack_start(self.scroll_list,
            True, True, 0)
        self.vbox_lista_reproduccion.pack_end(self.controlesrepro,
            False, True, 0)
            
    def __clicks_en_pantalla(self, widget, event):
        """
        Hace fullscreen y unfullscreen sobre la
        ventana principal donde JAMedia está embebida
        cuando el usuario hace doble click en el visor.
        """
        
        if event.type.value_name == "GDK_2BUTTON_PRESS":
            
            self.get_toplevel().set_sensitive(False)
            
            ventana = self.get_toplevel()
            screen = ventana.get_screen()
            w,h = ventana.get_size()
            ww, hh = (screen.get_width(), screen.get_height())
            
            self.__cancel_toolbars_flotantes()
            
            if ww == w and hh == h:
                ventana.set_border_width(2)
                GLib.idle_add(ventana.unfullscreen)
                
            else:
                ventana.set_border_width(0)
                GLib.idle_add(ventana.fullscreen)
                
            self.get_toplevel().set_sensitive(True)
            
    def __mostrar_config(self, widget):
        """
        Muestra u oculta las opciones de
        configuracion (toolbar_config y widget_efectos).
        """
        
        self.get_toplevel().set_sensitive(False)
        
        map(self.__ocultar, [
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
            self.scroll_config.show_all()
            GLib.idle_add(self.__update_balance_toolbars)
        
        self.get_toplevel().set_sensitive(True)
        
    def switch_reproductor(self, widget, nombre):
        """
        Recibe la señal "reproductor" desde toolbar_config y
        cambia el reproductor que se utiliza, entre mplayer y
        jamediareproductor (Gst 1.0).
        """
        
        self.get_toplevel().set_sensitive(False)
        
        reproductor = self.player
        
        # HACK: JAMediaReproductor no funciona con Tv.
        if reproductor == self.mplayerreproductor and \
            ("TV" in self.toolbar_list.label.get_text() or \
            "Tv" in self.toolbar_list.label.get_text()):
                self.toolbar_config.mplayer_boton.set_active(True)
                self.toolbar_config.jamedia_boton.set_active(False)
                return
            
        if nombre == "MplayerReproductor":
            if get_programa('mplayer'):
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
            
        self.get_toplevel().set_sensitive(True)
        
    def __embed_event(self, widget):
        """
        No hace nada por ahora.
        """
        
        print "JAMediaPlayer => OK"
        
    '''
    # FIXME: Nueva metodología Según JAMediaLector, esto reemplaza
    # self.pantalla.connect("ocultar_controles", self.ocultar_controles)
    def do_motion_notify_event(self, event):
        """
        Cuando se mueve el mouse sobre la ventana.
        """
        
        if self.toolbar_info.ocultar_controles:
            x, y = (int(event.x), int(event.y))
            rect = self.get_allocation()
            xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)
            
            arriba = range(0, self.toolbar.get_allocation().height)
            abajo = range(hh - self.controlesrepro.get_allocation().height, hh)
            derecha = range(ww - self.derecha_vbox.get_allocation().width, ww)
            
            ###Arriba    ###Derecha     ###Abajo
            if y in arriba or x in derecha or y in abajo:
                map(self.mostrar, self.controles_dinamicos)
                
            else:
                map(self.ocultar, [
                    #self.scroll_config,
                    self.toolbar_accion,
                    self.toolbaraddstream,
                    self.toolbar_salir])
                    
                map(self.ocultar, self.controles_dinamicos)
                
        else:
            map(self.mostrar, self.controles_dinamicos)'''

    def __ocultar_controles(self, widget, valor):
        """
        Oculta o muestra los controles.
        """
        
        self.mouse_in_visor = valor
        
        self.get_toplevel().set_sensitive(False)
        
        zona, ocultar = (valor, self.toolbar_info.ocultar_controles)
        
        if zona and ocultar:
            map(self.__ocultar, [
                #self.scroll_config,
                self.toolbar_accion,
                self.toolbaraddstream,
                self.toolbar_salir])
                
            map(self.__ocultar, self.controles_dinamicos)
            
        elif zona and not ocultar:
            pass
        
        elif not zona and ocultar:
            #self.scroll_config.hide()
            map(self.__mostrar, self.controles_dinamicos)
            
        elif not zona and not ocultar:
            pass
        
        self.get_toplevel().set_sensitive(True)
        
    def __ocultar(self, objeto):
        """
        Esta funcion es llamada desde self.ocultar_controles()
        """
        
        if objeto.get_visible(): objeto.hide()
        
    def __mostrar(self, objeto):
        """
        Esta funcion es llamada desde self.ocultar_controles()
        """
        
        if not objeto.get_visible(): objeto.show()
        
    def __activar(self, widget= None, senial= None):
        """
        Recibe:
            "atras", "siguiente", "stop" o "pause-play"
            
        desde la toolbar de reproduccion y ejecuta:
            atras o siguiente sobre la lista de reproduccion y
            stop o pause-play sobre el reproductor.
        """
        
        self.get_toplevel().set_sensitive(False)
        
        self.__cancel_toolbars_flotantes()
        
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
        
        while Gtk.events_pending():
            Gtk.main_iteration()
            
        self.get_toplevel().set_sensitive(True)

    def __endfile(self, widget = None, senial = None):
        """
        Recibe la señal de fin de archivo desde el reproductor
        y llama a seleccionar_siguiente en la lista de reproduccion.
        """
        
        self.controlesrepro.set_paused()
        GLib.idle_add(self.lista_de_reproduccion.seleccionar_siguiente)
        
    def __cambioestadoreproductor(self, widget = None, valor = None):
        """
        Recibe los cambios de estado del reproductor (paused y playing)
        y actualiza la imagen del boton play en la toolbar de reproduccion.
        """
        
        if "playing" in valor:
            self.controlesrepro.set_playing()
            
        elif "paused" in valor or "None" in valor:
            self.controlesrepro.set_paused()
            
        else:
            print "Estado del Reproductor desconocido:", valor
            
        GLib.idle_add(self.__update_balance_toolbars)
        
    def __update_balance_toolbars(self):
        """
        Actualiza las toolbars de balance en video.
        """
        
        config = self.player.get_balance()
        
        self.toolbar_config.set_balance(
            brillo = config['brillo'],
            contraste = config['contraste'],
            saturacion = config['saturacion'],
            hue = config['hue'],
            gamma = config['gamma'])
            
        return False
    
    def __update_progress(self, objetoemisor, valor):
        """
        Recibe el progreso de la reproduccion desde el reproductor
        y actualiza la barra de progreso.
        """
        
        self.barradeprogreso.set_progress(float(valor))
    
    def __user_set_value(self, widget= None, valor= None):
        """
        Recibe la posicion en la barra de progreso cuando
        el usuario la desplaza y hace "seek" sobre el reproductor.
        """
        
        self.__cancel_toolbars_flotantes()
        
        self.player.set_position(valor)
        
    def pack_standar(self):
        """
        Re empaqueta algunos controles de JAMedia.
        Cuando JAMedia no está embebido, tiene su toolbar_list
        """
        
        self.get_toplevel().set_sensitive(False)
        
        from JAMediaObjects.JAMediaGlobales import set_listas_default
        
        set_listas_default()
        
        from Widgets import ToolbarLista
        
        self.toolbar_list = ToolbarLista()
        self.toolbar_list.connect("cargar_lista", self.__cargar_lista)
        self.toolbar_list.connect("add_stream", self.__add_stream)
        self.toolbar_list.connect("menu_activo", self.__cancel_toolbars_flotantes)
        self.toolbar_list.show_all()
        self.toolbar_list.boton_agregar.hide()
        self.toolbar_info.descarga.show()
        
        for child in self.vbox_lista_reproduccion.get_children():
            self.vbox_lista_reproduccion.remove(child)
            
        self.vbox_lista_reproduccion.pack_start(self.toolbar_list,
            False, False, 0)
        self.__pack_vbox_lista_reproduccion()
        
        self.get_toplevel().set_sensitive(True)
        
    def pack_efectos(self):
        """
        Empaqueta los widgets de efectos gstreamer.
        """
        
        self.get_toplevel().set_sensitive(False)
        
        self.vbox_config.pack_start(self.widget_efectos, False, False, 0)
        
        from JAMediaObjects.JAMediaGlobales import get_jamedia_video_efectos
        
        GLib.idle_add(self.__cargar_efectos, list(get_jamedia_video_efectos()))
        
        self.get_toplevel().set_sensitive(True)
        
    def __add_stream(self, widget):
        """
        Recibe la señal add_stream desde toolbarlist
        y abre la toolbar que permite agregar un stream.
        """
        
        self.__cancel_toolbar()
        
        map(self.__ocultar, [
            self.scroll_config,
            self.toolbar_accion])
            
        if not self.toolbaraddstream.get_visible():
            accion = widget.label.get_text()
            self.toolbaraddstream.set_accion(accion)
            self.toolbaraddstream.show()
            
        else:
            self.toolbaraddstream.hide()
            
    def set_nueva_lista(self, lista):
        """
        Carga una lista de archivos directamente, sin
        utilizar la toolbarlist, esto es porque: cuando
        jamedia está embebido, no tiene la toolbar_list
        """
        
        if not lista: return
        
        self.player.stop()
        
        if self.toolbar_list: self.toolbar_list.label.set_text("")
        self.lista_de_reproduccion.limpiar()
        
        GLib.idle_add(self.lista_de_reproduccion.agregar_items, lista)
        
        return False

    def __cargar_reproducir(self, widget, path):
        """
        Recibe lo que se selecciona en la lista de
        reproduccion y lo manda al reproductor.
        """
        
        # HACK: Cuando cambia de pista se deben
        # reestablecer los valores de balance para
        # que no cuelgue la aplicación, por lo tanto,
        # el usuario no puede estar modificando estos
        # valores en el momento en que cambia la pista
        # en el reproductor.
        
        self.get_toplevel().set_sensitive(False)
        
        visible = self.scroll_config.get_visible()
        if visible: self.scroll_config.hide()
        
        self.player.load(path)
        
        if visible: self.scroll_config.show()
        
        self.get_toplevel().set_sensitive(True)
        
    def confirmar_salir(self, widget = None, senial = None):
        """
        Recibe salir y lo pasa a la toolbar de confirmación.
        
        Es pública para sobre escritura.
        """
        
        #map(self.__ocultar, [self.toolbaraddstream])
        self.__cancel_toolbars_flotantes()
        
        self.toolbar_salir.run("JAMedia")
        
    def __emit_salir(self, widget):
        """
        Emite salir para que cuando esta embebida, la
        aplicacion decida que hacer, si salir, o cerrar solo
        JAMedia.
        """
        
        if self.grabador != None:
            self.grabador.stop()
        
        self.player.stop()
        #self.lista_de_reproduccion.limpiar()
        
        while Gtk.events_pending():
            Gtk.main_iteration()
            
        self.emit('salir')
        
    def __cargar_lista(self, widget, indice):
        """
        Recibe el indice seleccionado en el menu de toolbarlist y
        carga la lista correspondiente.
        
        Esto es solo para JAMedia no embebido ya que cuando JAMedia
        esta embebida, no posee la toolbarlist.
        """
        
        model, iter = self.lista_de_reproduccion.treeselection.get_selected()
        ultimopath = False
        
        if model and iter:
            valor = model.get_value(iter, 2)
            
            if valor:
                from JAMediaObjects.JAMFileSystem import describe_uri
                
                descripcion = describe_uri(valor)
                
                if descripcion:
                    if descripcion[2]:
                        ultimopath = valor
                
        map(self.__ocultar, [
            self.toolbar_accion,
            self.toolbaraddstream])
            
        self.toolbar_list.boton_agregar.hide()
        
        from JAMediaObjects.JAMediaGlobales import get_data_directory
        from JAMediaObjects.JAMediaGlobales import get_my_files_directory
        from JAMediaObjects.JAMediaGlobales import get_tube_directory
        from JAMediaObjects.JAMediaGlobales import get_audio_directory
        from JAMediaObjects.JAMediaGlobales import get_video_directory
        
        if indice == 0:
            archivo = os.path.join(
                get_data_directory(),
                'JAMediaRadio.JAMedia')
                
            self.__seleccionar_lista_de_stream(archivo, "JAM-Radio")
            
        elif indice == 1:
            # HACK: Tv no funciona con JAMediaReproductor.
            if self.player == self.jamediareproductor:
                self.switch_reproductor(None, "MplayerReproductor")
                
            archivo = os.path.join(
                get_data_directory(),
                'JAMediaTV.JAMedia')
                
            self.__seleccionar_lista_de_stream(archivo, "JAM-TV")
            
        elif indice == 2:
            archivo = os.path.join(
                get_data_directory(),
                'MisRadios.JAMedia')
                
            self.__seleccionar_lista_de_stream(archivo, "Radios")
            self.toolbar_list.boton_agregar.show()
            
        elif indice == 3:
            # HACK: Tv no funciona con JAMediaReproductor.
            if self.player == self.jamediareproductor:
                self.switch_reproductor(None, "MplayerReproductor")
                
            archivo = os.path.join(
                get_data_directory(),
                'MisTvs.JAMedia')
                
            self.__seleccionar_lista_de_stream(archivo, "TVs")
            self.toolbar_list.boton_agregar.show()
            
        elif indice == 4:
            self.__seleccionar_lista_de_archivos(
                get_my_files_directory(),
                "Archivos")
                
        elif indice == 5:
            self.__seleccionar_lista_de_archivos(
                get_tube_directory(),
                "JAM-Tube")
                
        elif indice == 6:
            self.__seleccionar_lista_de_archivos(
                get_audio_directory(),
                "JAM-Audio")
                
        elif indice == 7:
            self.__seleccionar_lista_de_archivos(
                get_video_directory(),
                "JAM-Video")
                
        elif indice == 8:
            from Widgets import My_FileChooser
            
            directorio = None
            
            if ultimopath:
                directorio = "file://%s" % os.path.dirname(ultimopath)
                
            selector = My_FileChooser(
                parent = self.get_toplevel(),
                action = Gtk.FileChooserAction.OPEN,
                mime = ["audio/*", "video/*"],
                title = "Abrir Archivos.",
                path = directorio,
                filter = [])
            
            selector.connect('archivos-seleccionados', self.__cargar_directorio)
            
            selector.run()
            
            if selector: selector.destroy()
        
    def __cargar_directorio(self, widget, archivos):
        """
        Recibe una lista de archivos y setea la lista
        de reproduccion con ellos.
        """
        
        if not archivos: return
        
        items = []
        
        for archivo in archivos:
            path = archivo
            archivo = os.path.basename(path)
            items.append( [archivo,path] )
            
        self.set_nueva_lista(items)
        
    def __seleccionar_lista_de_archivos(self, directorio, titulo):
        """
        Responde a la seleccion en el menu de la toolbarlist.
        
        Recibe un directorio para generar una lista de archivos
        y setear la lista de reproduccion con ellos y recibe un titulo
        para la lista cargada.
        
        Esto es solo para las listas standar de JAMedia no embebido.
        """
        
        self.player.stop()
        
        archivos = sorted(os.listdir(directorio))
        
        lista = []
        
        for texto in archivos:
            url = os.path.join(directorio, texto)
            elemento = [texto, url]
            lista.append(elemento)
            
        self.toolbar_list.label.set_text(titulo)
        self.lista_de_reproduccion.limpiar()
        
        GLib.idle_add(self.lista_de_reproduccion.agregar_items, lista)

    def __seleccionar_lista_de_stream(self, archivo, titulo):
        """
        Responde a la seleccion en el menu de la toolbarlist.
        
        Recibe un archivo desde donde cargar una lista de
        streamings, carga los streamings y los pasa a la lista de
        reproduccion, y recibe un titulo para la nueva lista.
        
        Esto es solo para las listas standar de JAMedia no embebido.
        """
        
        self.player.stop()
        
        self.__cancel_toolbars_flotantes()
        
        from JAMediaObjects.JAMediaGlobales import get_streamings
        
        items = get_streamings(archivo)
        
        self.toolbar_list.label.set_text(titulo)
        self.lista_de_reproduccion.limpiar()
        
        GLib.idle_add(self.lista_de_reproduccion.agregar_items, items)
        
    def __click_derecho_en_lista(self, widget, event):
        """
        Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista de reproduccion, permitiendo copiar, mover y
        borrar el archivo o streaming o simplemente quitarlo
        de la lista.
        """
        
        self.__cancel_toolbars_flotantes()
        
        # FIXME: Desactivar __cargar_reproducir
        
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
            from Widgets import MenuList
            
            menu = MenuList(widget, boton, pos, tiempo, path, widget.modelo)
            menu.connect('accion', self.__set_accion)
            menu.popup(None, None, None, None, boton, tiempo)
            
        elif boton == 2:
            return
        
    def __set_accion(self, widget, lista, accion, iter):
        """
        Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.
        
        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar.
        """
        
        self.toolbar_accion.set_accion(lista, accion, iter)
        
    def __grabar_streaming(self, widget, uri):
        """
        Se ha confirmado grabar desde un streaming en
        la toolbar_accion.
        """
        
        self.get_toplevel().set_sensitive(False)
        
        self.__detener_grabacion()
        
        extension = ""
        if "TV" in self.toolbar_list.label.get_text() or \
            "Tv" in self.toolbar_list.label.get_text():
                extension = ".avi"
                
        else:
            extension = ".mp3"
            
        import time
        import datetime
        
        hora = time.strftime("%H-%M-%S")
        fecha = str(datetime.date.today())
        
        from JAMediaObjects.JAMediaGlobales import get_my_files_directory
        
        archivo = "%s-%s-%s" % (fecha, hora, extension)
        archivo = os.path.join(get_my_files_directory(), archivo)
        
        if self.player == self.jamediareproductor:
            self.grabador = JAMediaGrabador(uri, archivo)
            
        elif self.player == self.mplayerreproductor:
            self.grabador = MplayerGrabador(uri, archivo)
            
        self.grabador.connect('update', self.__update_grabador)
        
        self.get_toplevel().set_sensitive(True)
        
    def __update_grabador(self, widget, datos):
        """
        Actualiza informacion de Grabacion en proceso.
        """
        
        self.toolbar_grabar.set_info(datos)
    
    def __detener_grabacion(self, widget= None):
        """
        Detiene la Grabación en Proceso.
        """
        
        if self.grabador != None:
            self.grabador.stop()
            
        self.toolbar_grabar.stop()
        
    def __set_volumen(self, widget, valor):
        """
        Cuando el usuario cambia el volumen.
        """
        
        valor = valor * 100
        self.player.set_volumen(valor)
        
    def __get_volumen(self, widget, valor):
        """
        El volumen con el que se reproduce actualmente.
        """
        
        self.volumen.set_value(valor)
        
    def __set_video(self, widget, valor):
        """
        Si hay video o no en la fuente . . .
        """
        
        pass
        # FIXME: La idea es iniciar visualizador de audio.
        #print "Video en la Fuente:", valor
        #if not valor: self.player.link_visualizador()
        