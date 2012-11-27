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

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject

import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import ToolbarcontrolValores

import JAMediaObjects.JAMFileSystem as JAMF
import JAMediaObjects.JAMediaGlobales as G

JAMediaObjectsPath = JAMediaObjects.__path__[0]
   
class ToolbarGrabar(Gtk.Toolbar):
    """ Informa al usuario cuando se está grabando
    desde un streaming. """
    
    __gsignals__ = {
    "stop":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.colors = [G.BLANCO, G.NARANJA]
        self.color = self.colors[0]
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "stop.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Detener.")
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("Grabador Detenido.")
        #self.label.set_line_wrap(True)
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.show_all()
        
        boton.connect("clicked", self.emit_stop)

    def emit_stop(self, widget= None, event= None):
        """Cuando el usuario hace click en el boton stop
        para detener la grabacion en proceso."""
        
        self.stop()
        self.emit("stop")
    
    def stop(self):
        """ Setea la toolbar a "no grabando"."""
        
        self.color = self.colors[0]
        self.label.modify_fg(0, self.color)
        self.label.set_text("Grabador Detenido.")
        if self.get_visible(): self.hide()
        
    def set_info(self, datos):
        """Muestra información sobre el proceso de grabación."""
        
        self.label.set_text(datos)
        self.update()
        
    def update(self):
        """Cambia los colores de la toolbar
        mientras se esta grabando desde un streaming."""
        
        if self.color == self.colors[0]:
            self.color = self.colors[1]
            
        elif self.color == self.colors[1]:
            self.color = self.colors[0]
            
        self.label.modify_fg(0, self.color)
        if not self.get_visible(): self.show()
    
class ToolbarLista(Gtk.Toolbar):
    """Toolbar de la lista de reproduccion, que contiene
    un menu con las listas standar de JAMedia:
    Radios, Tv, etc . . ."""
    
    __gsignals__ = {
    "cargar_lista":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,)),
    "add_stream":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "lista.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Selecciona una Lista.")
        boton.connect("clicked", self.get_menu)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "agregar.png")
        self.boton_agregar = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        self.boton_agregar.set_tooltip_text("Agregar Streaming.")
        self.boton_agregar.connect("clicked", self.emit_add_stream)
        self.insert(self.boton_agregar, -1)
        
        self.show_all()
    
    def get_menu(self, widget):
        """El menu con las listas standar de JAMedia."""
        
        menu = Gtk.Menu()
        
        item = Gtk.MenuItem("JAMedia Radio")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 0)
        
        item = Gtk.MenuItem("JAMedia TV")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 1)
        
        item = Gtk.MenuItem("Mis Emisoras")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 2)
        
        item = Gtk.MenuItem("Mis Canales")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 3)
        
        item = Gtk.MenuItem("Mis Archivos")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 4)
        
        item = Gtk.MenuItem("JAMediaTube")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 5)
        
        item = Gtk.MenuItem("Audio-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 6)
        
        item = Gtk.MenuItem("Video-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 7)
        
        item = Gtk.MenuItem("Archivos Externos")
        menu.append(item)
        item.connect_object("activate", self.emit_load_list, 8)
        
        menu.show_all()
        menu.attach_to_widget(widget, self.null)
        menu.popup(None, None, None, None, 1, 0)
        
    def null(self):
        pass
    
    def emit_load_list(self, indice):
        self.emit("cargar_lista", indice)
        
    def emit_add_stream(self, widget):
        self.emit("add_stream")
        
class Toolbar(Gtk.Toolbar):
    """Toolbar principal de JAMedia."""
    
    __gsignals__ = {
    'salir':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'config':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "configurar.png")
        self.configurar = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(1))
        self.configurar.set_tooltip_text("Configuraciones.")
        self.configurar.connect("clicked", self.emit_config)
        self.insert(self.configurar, -1)
        
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
    
    def emit_config(self, widget):
        """Cuando se hace click en el boton configurar
        de la toolbar principal de JAMedia."""
        
        self.emit('config')
        
    def salir(self, widget):
        """Cuando se hace click en el boton salir
        de la toolbar principal de JAMedia."""
        
        self.emit('salir')
        
class Selector_de_Archivos (Gtk.FileChooserDialog):
    """Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio."""
    
    __gsignals__ = {
    'archivos-seleccionados':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self, jamedia):
        
        Gtk.FileChooserDialog.__init__(self,
            title = "Abrir Archivos de Audio o Video",
            parent = jamedia, action = Gtk.FileChooserAction.OPEN)
            
        self.set_default_size( 640, 480 )
        self.set_current_folder_uri("file:///media")
        self.set_select_multiple(True)
        
        # extras
        hbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        boton_abrir_directorio = Gtk.Button("Abrir")
        boton_seleccionar_todo = Gtk.Button("Seleccionar Todos")
        boton_salir = Gtk.Button("Salir")
        hbox.pack_end(boton_salir, True, True, 5)
        hbox.pack_end(boton_seleccionar_todo, True, True, 5)
        hbox.pack_end(boton_abrir_directorio, True, True, 5)
        self.set_extra_widget(hbox)
        
        filter = Gtk.FileFilter()
        filter.set_name("Música")
        filter.add_mime_type("audio/*")
        self.add_filter(filter)
        
        filter = Gtk.FileFilter()
        filter.set_name("Videos")
        filter.add_mime_type("video/*")
        self.add_filter(filter)
        
        self.add_shortcut_folder_uri("file:///media/")
        
        # Callbacks
        boton_salir.connect("clicked", self.salir)
        boton_abrir_directorio.connect("clicked",
            self.abrir_directorio)
        boton_seleccionar_todo.connect("clicked",
            self.seleccionar_todos_los_archivos)
        
        self.show_all()
        self.resize( 640, 480 )
        
    def seleccionar_todos_los_archivos(self, widget):
        
        self.select_all()
        
    def abrir_directorio(self, widget):
        """Manda una señal con la lista de archivos
        seleccionados para cargarse en el reproductor."""
        
        self.emit('archivos-seleccionados', self.get_filenames())
        self.salir(None)
        
    def salir(self, widget):
        self.destroy()
        
class MenuList(Gtk.Menu):
    """Menu con opciones para operar sobre el archivo o
    el streaming seleccionado en la lista de reproduccion
    al hacer click derecho sobre él."""
    
    __gsignals__ = {
    'accion':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}
    
    def __init__(self, widget, boton, pos, tiempo, path, modelo):
        
        Gtk.Menu.__init__(self)
        
        iter = modelo.get_iter(path)
        uri = modelo.get_value(iter, 2)
        
        quitar = Gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.set_accion,
            widget, path, "Quitar")
        
        if JAMF.describe_acceso_uri(uri):
            lectura, escritura, ejecucion = JAMF.describe_acceso_uri(uri)
            
            if lectura and os.path.dirname(uri) != G.DIRECTORIO_MIS_ARCHIVOS:
                copiar = Gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.set_accion,
                    widget, path, "Copiar")
                
            if escritura and os.path.dirname(uri) != G.DIRECTORIO_MIS_ARCHIVOS:
                mover = Gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.set_accion,
                    widget, path, "Mover")
                
            if escritura:
                borrar = Gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.set_accion,
                    widget, path, "Borrar")
                
        else:
            borrar = Gtk.MenuItem("Borrar Streaming")
            self.append(borrar)
            borrar.connect_object("activate", self.set_accion,
                widget, path, "Borrar")
                
            listas = [
                os.path.join(G.DIRECTORIO_DATOS, "JAMediaTV.JAMedia"),
                os.path.join(G.DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"),
                os.path.join(G.DIRECTORIO_DATOS, "MisRadios.JAMedia"),
                os.path.join(G.DIRECTORIO_DATOS, "MisTvs.JAMedia")
                ]
            
            if (G.stream_en_archivo(uri, listas[0]) and \
                not G.stream_en_archivo(uri, listas[3])) or \
                (G.stream_en_archivo(uri, listas[1]) and \
                not G.stream_en_archivo(uri, listas[2])):
                    
                copiar = Gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.set_accion,
                    widget, path, "Copiar")
                    
                mover = Gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.set_accion,
                    widget, path, "Mover")
                
            grabar = Gtk.MenuItem("Grabar")
            self.append(grabar)
            grabar.connect_object("activate", self.set_accion,
                widget, path, "Grabar")
                
        self.show_all()
        self.attach_to_widget(widget, self.null)
        
    def null(self):
        pass
    
    def set_accion(self, widget, path, accion):
        """Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.
        
        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar."""
        
        iter = widget.modelo.get_iter(path)
        self.emit('accion', widget, accion, iter)
        
class ToolbarInfo(Gtk.Toolbar):
    """ Informa al usuario sobre el reproductor
    que se esta utilizando.
    Permite Rotar el Video.
    Permite configurar ocultar controles automáticamente."""
    
    __gsignals__ = {
    'rotar':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'actualizar_streamings':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.ocultar_controles = False
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","mplayer.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        self.mplayer = Gtk.ToolItem()
        self.mplayer.add(imagen)
        self.insert(self.mplayer, -1)
        
        imagen = Gtk.Image()
        icono = os.path.join(JAMediaObjectsPath,
            "Iconos","JAMedia.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, G.get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        self.jamedia = Gtk.ToolItem()
        self.jamedia.add(imagen)
        self.insert(self.jamedia, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "rotar.png")
        self.boton_izquierda = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        self.boton_izquierda.set_tooltip_text("Izquierda")
        self.boton_izquierda.connect("clicked", self.emit_rotar)
        self.insert(self.boton_izquierda, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "rotar.png")
        self.boton_derecha = G.get_boton(archivo, flip = True,
            pixels = G.get_pixels(0.8))
        self.boton_derecha.set_tooltip_text("Derecha")
        self.boton_derecha.connect("clicked", self.emit_rotar)
        self.insert(self.boton_derecha, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        item = Gtk.ToolItem()
        label = Gtk.Label("Ocultar Controles:")
        label.show()
        item.add(label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        switch = Gtk.Switch()
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        self.insert(item, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "iconplay.png")
        self.descarga = G.get_boton(archivo, flip = False,
            rotacion = GdkPixbuf.PixbufRotation.CLOCKWISE,
            pixels = G.get_pixels(0.8))
        self.descarga.set_tooltip_text("Actualizar Streamings")
        self.descarga.connect("clicked", self.emit_actualizar_streamings)
        self.insert(self.descarga, -1)
        
        self.show_all()
        
        switch.connect('button-press-event', self.set_controles_view)
        
    def emit_actualizar_streamings(self, widget):
        """Emite señal para actualizar los
        streamings desde la web de jamedia."""
        
        self.emit('actualizar_streamings')
        
    def set_reproductor(self, reproductor):
        """Muestra el Reproductor Activo."""
        
        if reproductor == "MplayerReproductor":
            self.mplayer.show()
            self.jamedia.hide()
            
        elif reproductor == "JAMediaReproductor":
            self.jamedia.show()
            self.mplayer.hide()
            
    def emit_rotar(self, widget):
        """ Emite la señal rotar con su valor Izquierda o Derecha. """
        
        if widget == self.boton_derecha:
            self.emit('rotar', "Derecha")
            
        elif widget == self.boton_izquierda:
            self.emit('rotar', "Izquierda")
            
    def set_controles_view(self, widget, senial):
        """Almacena el estado de "ocultar_controles"."""
        
        self.ocultar_controles = not widget.get_active()
        
class ToolbarConfig(Gtk.Table):
    """ Toolbar para intercambiar reproductores (mplayer gst) y
    modificar valores de balance en video. """
    
    __gsignals__ = {
    "reproductor":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'valor':(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_FLOAT, GObject.TYPE_STRING))}
    
    def __init__(self):
        
        Gtk.Table.__init__(self, rows=6, columns=1, homogeneous=True)
        
        self.brillo = ToolbarcontrolValores("Brillo")
        self.contraste = ToolbarcontrolValores("Contraste")
        self.saturacion = ToolbarcontrolValores("Saturación")
        self.hue = ToolbarcontrolValores("Matíz")
        self.gamma = ToolbarcontrolValores("Gamma")
        
        self.attach(self.brillo, 0, 1, 0, 1)
        self.attach(self.contraste, 0, 1, 1, 2)
        self.attach(self.saturacion, 0, 1, 2, 3)
        self.attach(self.hue, 0, 1, 3, 4)
        self.attach(self.gamma, 0, 1, 4, 5)
        
        toolbar = Gtk.Toolbar()
        
        toolbar.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        item = Gtk.ToolItem()
        self.label = Gtk.Label("Utilizar: ")
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "mplayer.png")
        self.mplayer_boton = G.get_togle_boton(archivo,
            flip = False,
            pixels = G.get_pixels(1))
        self.mplayer_boton.set_tooltip_text("MplayerReproductor")
        self.mplayer_boton.connect("toggled",
            self.emit_reproductor, "MplayerReproductor")
        toolbar.insert(self.mplayer_boton, -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "JAMedia.png")
        self.jamedia_boton = G.get_togle_boton(archivo,
            flip = False,
            pixels = G.get_pixels(1))
        self.jamedia_boton.set_tooltip_text("JAMediaReproductor")
        self.jamedia_boton.connect("toggled",
            self.emit_reproductor, "JAMediaReproductor")
        toolbar.insert(self.jamedia_boton, -1)
        
        toolbar.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
            
        self.attach(toolbar, 0, 1, 5, 6)
        
        self.show_all()
        
        self.brillo.connect('valor', self.emit_senial, 'brillo')
        self.contraste.connect('valor', self.emit_senial, 'contraste')
        self.saturacion.connect('valor', self.emit_senial, 'saturacion')
        self.hue.connect('valor', self.emit_senial, 'hue')
        self.gamma.connect('valor', self.emit_senial, 'gamma')
        
    def emit_senial(self, widget, valor, tipo):
        """Emite valor, que representa un valor
        en % float y un valor tipo para:
            brillo - contraste - saturacion - hue - gamma"""
            
        self.emit('valor', valor, tipo)
        
    def set_balance(self, brillo = None, contraste = None,
        saturacion = None, hue = None, gamma = None):
        """Setea las barras segun valores."""
        
        if saturacion != None: self.saturacion.set_progress(saturacion)
        if contraste != None: self.contraste.set_progress(contraste)
        if brillo != None: self.brillo.set_progress(brillo)
        if hue != None: self.hue.set_progress(hue)
        if gamma != None: self.gamma.set_progress(gamma)
        
    def emit_reproductor(self, widget, nombre):
        """Emite la señal que cambia de reproductor
        entre mplayer y jamediareproductor (Gst 1.0)"""
        
        if widget.get_active():
            self.emit("reproductor", nombre)
            
            if widget == self.mplayer_boton:
                self.jamedia_boton.set_active(False)
                
            elif widget == self.jamedia_boton:
                self.mplayer_boton.set_active(False)
                
        if not self.mplayer_boton.get_active() and \
            not self.jamedia_boton.get_active():
                widget.set_active(True)
        
class ToolbarAddStream(Gtk.Toolbar):
    """Toolbar para agregar streamings."""
    
    __gsignals__ = {
    "add-stream":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_STRING))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.tipo = None
        
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
        self.nombre = Gtk.Entry()
        self.nombre.show()
        item.add(self.nombre)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        self.url = Gtk.Entry()
        self.url.show()
        item.add(self.url)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "acercar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.emit_add_stream)
        self.insert(boton, -1)

        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def emit_add_stream(self, widget):
        """Emite la señal para agregar el streaming."""
        
        nombre, url = (self.nombre.get_text(), self.url.get_text())
        
        if nombre and url:
            self.emit('add-stream', self.tipo, nombre, url)
            
        self.tipo = None
        self.nombre.set_text("")
        self.url.set_text("")
        
        self.hide()
        
    def set_accion(self, tipo):
        """Recibe Tv o Radio para luego enviar
        este dato en la señal add-stream, de modo que
        JAMedia sepa donde agregar el streaming."""
        
        self.nombre.set_text("")
        self.url.set_text("")
        self.tipo = tipo
        
    def cancelar(self, widget= None):
        """Cancela la accion."""
        
        self.tipo = None
        self.nombre.set_text("")
        self.url.set_text("")
        
        self.hide()
        