#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaWidgets.py por:
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

# Contiene:
#   Visor => DrawingArea para mostrar imágenes o video o dibujar sobre el.
#   Lista => TreeView con modelo ListStore asociado, para operar como lista de reproducción.
#   ToolbarReproduccion(Gtk.Box) => Controles de Reproducción: play/pausa-stop-atras-siguiente

import os
import sys

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkX11
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import cairo

import JAMFileSystem as JAMF

import JAMediaObjects.JAMediaGlobales as G

JAMediaWidgetsBASE = os.path.dirname(__file__)

class JAMediaButton(Gtk.EventBox):
    """Un Boton a medida"""
    
    __gsignals__ = {
    "clicked":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, )),
    "click_derecho":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        
        Gtk.EventBox.__init__(self)
        
        self.set_visible_window(True)
        self.modify_bg(0, G.BLANCO)
        self.set_border_width(1)
        
        self.estado_select = False
        
        self.colornormal = G.BLANCO
        self.colorselect = G.AMARILLO
        self.colorclicked = G.NARANJA
        
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
        Gdk.EventMask.BUTTON_RELEASE_MASK |
        Gdk.EventMask.POINTER_MOTION_MASK |
        Gdk.EventMask.ENTER_NOTIFY_MASK |
        Gdk.EventMask.LEAVE_NOTIFY_MASK)
            
        self.connect("button_press_event", self.button_press)
        self.connect("button_release_event", self.button_release)
        self.connect("enter-notify-event", self.enter_notify_event)
        self.connect("leave-notify-event", self.leave_notify_event)
        
        self.imagen = Gtk.Image()
        self.add(self.imagen)
            
        self.show_all()
        
    def seleccionar(self):
        """Marca como seleccionado"""
        
        self.estado_select = True
        self.colornormal = G.NARANJA
        self.colorselect = G.NARANJA
        self.colorclicked = G.NARANJA
        self.modify_bg(0, self.colornormal)
        
    def des_seleccionar(self):
        """Desmarca como seleccionado"""
        
        self.estado_select = False
        self.colornormal = G.BLANCO
        self.colorselect = G.AMARILLO
        self.colorclicked = G.NARANJA
        self.modify_bg(0, self.colornormal)
        
    def button_release(self, widget, event):
        
        self.modify_bg(0, self.colorselect)
        
    def leave_notify_event(self, widget, event):
        
        self.modify_bg(0, self.colornormal)
        
    def enter_notify_event(self, widget, event):
        
        self.modify_bg(0, self.colorselect)
        
    def button_press(self, widget, event):
        
        self.seleccionar()
        
        if event.button == 1:
            self.emit("clicked", event)
            
        elif event.button == 3:
            self.emit("click_derecho", event)
            
    def set_tooltip(self, texto):
        
        self.set_tooltip_text(texto)
        
    def set_imagen(self, archivo):
        
        self.imagen.set_from_file(archivo)
        
    def set_tamanio(self, w, h):
        
        self.set_size_request(w,h)
        
class Visor(Gtk.DrawingArea):
    """Visor generico para utilizar como area de
    reproduccion de videos o dibujar."""
    
    __gtype_name__ = 'Visor'
    
    __gsignals__ = {
    "ocultar_controles":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}
    
    def __init__(self):
        
        Gtk.DrawingArea.__init__(self)
        
        self.add_events(
            Gdk.EventMask.KEY_PRESS_MASK |
            Gdk.EventMask.KEY_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.POINTER_MOTION_HINT_MASK |
            Gdk.EventMask.BUTTON_MOTION_MASK |
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK
        )
        
        self.show_all()
        
    def do_motion_notify_event(self, event):
        """Cuando se mueve el mouse sobre el visor."""
        
        x, y = (int(event.x), int(event.y))
        rect = self.get_allocation()
        xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)
        if x in range(ww-60, ww) or y in range(yy, yy+60) \
            or y in range(hh-60, hh):
            self.emit("ocultar_controles", False)
            return
        else:
            self.emit("ocultar_controles", True)
            return
        
# >> -------------------- LISTA GENERICA --------------------- #
class Lista(Gtk.TreeView):
    """Lista generica."""
    
    __gsignals__ = {
    "nueva-seleccion":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}
    
    def __init__(self):
        
        Gtk.TreeView.__init__(self)
        
        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.valor_select = None
        self.modelo = Gtk.ListStore(GdkPixbuf.Pixbuf,
        GObject.TYPE_STRING, GObject.TYPE_STRING)
        self.setear_columnas()
        
        self.treeselection = self.get_selection()
        self.treeselection.set_select_function(self.selecciones, self.modelo)
        
        self.set_model(self.modelo)
        self.show_all()
    
    '''
    def keypress(self, widget, event):
        # derecha 114 izquierda 113 suprimir 119 backspace 22 (en xo no existe suprimir)
        tecla = event.get_keycode()[1]
        model, iter = self.treeselection.get_selected()
        valor = self.modelo.get_value(iter, 2)
        path = self.modelo.get_path(iter)
        if tecla == 22:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 113:
            if self.row_expanded(path):
                self.collapse_row(path)
        elif tecla == 114:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        elif tecla == 119:
            # suprimir
            print valor, path
        else:
            pass
        return False'''
    
    def selecciones(self, treeselection, model, path, is_selected, listore):
        """Cuando se selecciona un item en la lista."""
        
        # model y listore son ==
        iter = model.get_iter(path)
        valor =  model.get_value(iter, 2)
        if not is_selected and self.valor_select != valor:
            self.valor_select = valor
            self.emit('nueva-seleccion', self.valor_select)
        return True
    
    def setear_columnas(self):
        
        self.append_column(self.construir_columa_icono('', 0, True))
        self.append_column(self.construir_columa('Nombre', 1, True))
        self.append_column(self.construir_columa('', 2, False))
        
    def construir_columa(self, text, index, visible):
        
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna
    
    def construir_columa_icono(self, text, index, visible):
        
        render = Gtk.CellRendererPixbuf()
        columna = Gtk.TreeViewColumn(text, render,pixbuf=index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna
    
    def limpiar(self):
        
        self.modelo.clear()
        
    def agregar_items(self, elementos):
        """ Recibe lista de: [texto para mostrar, path oculto] y
        Agrega un item a la lista segun esos datos."""
        
        for item in elementos:
            texto, path = item
            descripcion = JAMF.describe_uri(path)
            
            icono = None
            if descripcion:
                if descripcion[2]:
                    # Es un Archivo
                    tipo = JAMF.describe_archivo(path)
                    
                    if 'video' in tipo:
                        icono = os.path.join(JAMediaWidgetsBASE,
                            "Iconos", "video.png")
                            
                    elif 'audio' in tipo:
                        icono = os.path.join(JAMediaWidgetsBASE,
                            "Iconos", "sonido.png")
                            
                    elif 'image' in tipo:
                        icono = os.path.join(path) # exige rendimiento
                        #icono = os.path.join(JAMediaWidgetsBASE,
                        #    "Iconos", "imagen.png")
                        
                    elif 'pdf' in tipo:
                        icono = os.path.join(JAMediaWidgetsBASE,
                            "Iconos", "pdf.png")
                            
                    elif 'zip' in tipo or 'rar' in tipo:
                        icono = os.path.join(JAMediaWidgetsBASE,
                            "Iconos", "zip.png")
                            
                    else:
                        icono = os.path.join(JAMediaWidgetsBASE,
                            "Iconos", "archivo.png")
            else:
                icono = os.path.join(JAMediaWidgetsBASE,
                    "Iconos", "archivo.png")
                
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
                    G.get_pixels(0.8), -1)
                self.modelo.append([ pixbuf, texto, path])
                
            except:
                pass
            
    def seleccionar_siguiente(self, widget = None):
        
        modelo, iter = self.treeselection.get_selected()
        
        try:
            self.treeselection.select_iter(modelo.iter_next(iter))
        except:
            self.seleccionar_primero()
    
    def seleccionar_anterior(self, widget = None):
        
        modelo, iter = self.treeselection.get_selected()
        
        try:
            self.treeselection.select_iter(modelo.iter_previous(iter))
        except:
            #self.seleccionar_ultimo()
            pass
    
    def seleccionar_primero(self, widget = None):
        
        self.treeselection.select_path(0)
    
    def seleccionar_ultimo(self, widget = None):
        pass
# << -------------------- LISTA GENERICA --------------------- #

# >> -------------------- Controles de Reproducción ---------- #
class ToolbarReproduccion(Gtk.Box):
    """Controles de reproduccion: play/pausa, stop, siguiente, atras."""
    
    __gsignals__ = {
    "activar":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)
        
        self.botonatras = G.get_boton(os.path.join(JAMediaWidgetsBASE,
            "Iconos", "siguiente.png"), True, pixels = G.get_pixels(0.8))
        self.botonatras.set_tooltip_text("Anterior")
        self.botonatras.connect("clicked", self.clickenatras)
        self.pack_start(self.botonatras, False, True, 0)
        
        self.botonplay = G.get_boton(os.path.join(JAMediaWidgetsBASE,
            "Iconos", "play.png"), pixels = G.get_pixels(0.8))
        self.botonplay.set_tooltip_text("Reproducir")
        self.botonplay.connect("clicked", self.clickenplay_pausa)
        self.pack_start(self.botonplay, False, True, 0)
        
        #self.botonpausa = G.get_boton(os.path.join(JAMediaWidgetsBASE,
        #    "Iconos", "pausa.png"), pixels = G.get_pixels(0.8))
        #self.botonpausa.set_tooltip_text("Pausar")
        #self.botonpausa.connect("clicked", self.clickenplay_pausa)
        #self.pack_start(self.botonpausa, False, True, 0)
        
        self.botonsiguiente = G.get_boton(os.path.join(JAMediaWidgetsBASE,
            "Iconos", "siguiente.png"), pixels = G.get_pixels(0.8))
        self.botonsiguiente.set_tooltip_text("Siguiente")
        self.botonsiguiente.connect("clicked", self.clickensiguiente)
        self.pack_start(self.botonsiguiente, False, True, 0)
        
        self.botonstop = G.get_boton(os.path.join(JAMediaWidgetsBASE,
            "Iconos", "stop.png"), pixels = G.get_pixels(0.8))
        self.botonstop.set_tooltip_text("Detener Reproducción")
        self.botonstop.connect("clicked", self.clickenstop)
        self.pack_start(self.botonstop, False, True, 0)
        
        self.show_all()
        
        #self.botonpausa.hide()
        
    def set_paused(self):
        
        #self.botonplay.show()
        #self.botonpausa.hide()
        pass
        
    def set_playing(self):
        
        #self.botonpausa.show()
        #self.botonplay.hide()
        pass
        
    def clickenstop(self, widget = None, event = None):
        
        self.emit("activar", "stop")
        
    def clickenplay_pausa(self, widget = None, event = None):
        
        self.emit("activar", "pausa-play")
        
    def clickenatras(self, widget= None, event= None):
        
        self.emit("activar", "atras")
        
    def clickensiguiente(self, widget= None, event= None):
        
        self.emit("activar", "siguiente")
# << -------------------- Controles de Reproducción ---------- #

# >> -------------------- Barra de Progreso ------------------ #
class BarraProgreso(Gtk.EventBox):
    """Barra de progreso para mostrar estado de reproduccion."""
    
    __gsignals__ = {
    "user-set-value":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}
    
    def __init__(self):
        
        Gtk.EventBox.__init__(self)
        
        self.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        self.escala = ProgressBar(Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))
        
        self.valor = 0
        
        self.add(self.escala)
        self.show_all()
        
        self.escala.connect('user-set-value', self.emit_valor)
        self.set_size_request(-1, G.get_pixels(1.2))
        
    def set_progress(self, valor = 0):
        """El reproductor modifica la escala."""
        
        if self.escala.presed: return
        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()
        
    def emit_valor(self, widget, valor):
        """El usuario modifica la escala."""
        
        if self.valor != valor:
            self.valor = valor
            self.emit("user-set-value", valor)
        
class ProgressBar(Gtk.Scale):
    """Escala de BarraProgreso."""
    
    __gsignals__ = {
    "user-set-value":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}
    
    def __init__(self, ajuste):
        
        Gtk.Scale.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)
        
        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)
        
        self.presed = False
        self.borde = G.get_pixels(0.5)
        
        icono = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "iconplay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            G.get_pixels(0.8), G.get_pixels(0.8))
        self.pixbuf = pixbuf.rotate_simple(GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)
        
        self.show_all()
        
    def do_button_press_event(self, event):
        
        self.presed = True
        
    def do_button_release_event(self, event):
        
        self.presed = False
        
    def do_motion_notify_event(self, event):
        """Cuando el usuario se desplaza por la barra de progreso."""
        
        if event.state == Gdk.ModifierType.MOD2_MASK | Gdk.ModifierType.BUTTON1_MASK:
            rect = self.get_allocation()
            x, y = (self.borde, self.borde)
            w, h = (rect.width-(self.borde*2), rect.height-(self.borde*2))
            eventx, eventy = ( int(event.x)-x, int(event.y)-y )
            if (eventx > int(x) and eventx < int(w)):
                valor = float(eventx * 100 / w)
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)
                    
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
         
        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        imgx = ximage
        imgy = float(self.borde+hh/2 - imgh/2)
        Gdk.cairo_set_source_pixbuf(contexto, self.pixbuf, imgx, imgy)
        contexto.paint()
        
        return True
# << -------------------- Barra de Progreso ------------------ #

class ControlVolumen(Gtk.VolumeButton):
    """Botón con escala para controlar el volúmen
    de reproducción en los reproductores."""
    
    __gsignals__ = {
    "volumen":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}
    
    def __init__(self):
        
        Gtk.VolumeButton.__init__(self)
        
        self.show_all()
        
    def do_value_changed(self, valor):
        """Cuando el usuario desplaza la escala
        emite el valor en float de 0.0 a 1.0."""
        
        self.emit('volumen', valor)
        
class ToolbarAccion(Gtk.Toolbar):
    """Toolbar para que el usuario confirme las
    acciones que se realizan sobre items que se
    seleccionan en la lista de reproduccion.
    (Borrar, mover, copiar, quitar)."""
    
    __gsignals__ = {
    "Grabar":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "accion-stream":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        #self.modify_bg(0, Gdk.Color(65000,65000,65000))
        
        self.lista = None
        self.accion = None
        self.iter = None
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("")
        self.label.set_line_wrap(True)
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaWidgetsBASE,
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
        """Ejecuta una accion sobre un archivo o streaming
        en la lista de reprucción cuando el usuario confirma."""
        
        uri = self.lista.modelo.get_value(self.iter, 2)
        
        if JAMF.describe_acceso_uri(uri):
            if self.accion == "Quitar":
                self.lista.modelo.remove(self.iter)
                
            elif self.accion == "Copiar":
                if os.path.isfile(uri):
                    JAMF.copiar(uri, G.DIRECTORIO_MIS_ARCHIVOS)
                    
            elif self.accion == "Borrar":
                if os.path.isfile(uri):
                    if JAMF.borrar(uri):
                        self.lista.modelo.remove(self.iter)
                        
            elif self.accion == "Mover":
                if os.path.isfile(uri):
                    if JAMF.mover(uri, G.DIRECTORIO_MIS_ARCHIVOS):
                        self.lista.modelo.remove(self.iter)
        else:
            if self.accion == "Quitar":
                self.lista.modelo.remove(self.iter)
                
            elif self.accion == "Borrar":
                self.emit("accion-stream", "Borrar", uri)
                self.lista.modelo.remove(self.iter)
                
            elif self.accion == "Copiar":
                self.emit("accion-stream", "Copiar", uri)
                
            elif self.accion == "Mover":
                self.emit("accion-stream", "Mover", uri)
                self.lista.modelo.remove(self.iter)
                
            elif self.accion == "Grabar":
                self.emit("Grabar", uri)
                
        self.label.set_text("")
        self.lista = None
        self.accion = None
        self.iter = None
        self.hide()
        
    def set_accion(self, lista, accion, iter):
        """Configura una accion sobre un archivo o
        streaming y muestra toolbaraccion para que
        el usuario confirme o cancele dicha accion."""
        
        self.lista = lista
        self.accion = accion
        self.iter = iter
        if self.lista and self.accion and self.iter:
            uri = self.lista.modelo.get_value(self.iter, 2)
            texto = uri
            if os.path.exists(uri):
                texto = os.path.basename(uri)
            self.label.set_text("¿%s?: %s" % (accion, texto))
            self.show_all()

    def cancelar(self, widget= None):
        """Cancela la accion configurada sobre
        un archivo o streaming en la lista de
        reproduccion."""
        
        self.label.set_text("")
        self.lista = None
        self.accion = None
        self.iter = None
        self.hide()
        
class ToolbarBalanceConfig(Gtk.Table):
    """ Toolbar de Configuración de Balance
    en Video. (Utilizado por JAMedia). """
    
    __gsignals__ = {
    'valor':(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_FLOAT, GObject.TYPE_STRING))}
    
    def __init__(self):
        
        Gtk.Table.__init__(self, rows=2, columns=3, homogeneous=True)
        
        self.brillo = ToolbarcontrolValores("Brillo")
        self.contraste = ToolbarcontrolValores("Contraste")
        self.saturacion = ToolbarcontrolValores("Saturación")
        self.hue = ToolbarcontrolValores("Hue")
        self.gamma = ToolbarcontrolValores("Gamma")
        
        self.attach(self.brillo, 0, 1, 0, 1)
        self.attach(self.contraste, 1, 2, 0, 1)
        self.attach(self.saturacion, 2, 3, 0, 1)
        self.attach(self.hue, 0, 1, 1, 2)
        self.attach(self.gamma, 1, 2, 1, 2)
        
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
        
class ToolbarcontrolValores(Gtk.Toolbar):
    """Toolbar con escala para modificar
    valores de balance en video, utilizada
    por ToolbarBalanceConfig."""
    
    __gsignals__ = {
    'valor':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}
    
    def __init__(self, label):
        
        Gtk.Toolbar.__init__(self)
        
        #self.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        #self.modify_bg(0, Gdk.Color(0, 0, 0))
        
        self.titulo = label
        
        self.escala = SlicerBalance()
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        
        self.frame = Gtk.Frame()
        self.frame.set_label(self.titulo)
        self.frame.set_label_align(0.5, 1.0)
        self.frame.add(self.escala)
        self.frame.show()
        item.add(self.frame)
        self.insert(item, -1)
        
        self.show_all()
        
        self.escala.connect("user-set-value", self.user_set_value)
        
    def user_set_value(self, widget= None, valor= None):
        """Recibe la posicion en la barra de
        progreso (en % float), y re emite los valores."""
        
        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))
        
    def set_progress(self, valor):
        """Establece valores en la escala."""
        
        self.escala.set_progress(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))
        
class SlicerBalance(Gtk.EventBox):
    """Barra deslizable para cambiar valores de Balance en Video."""
    
    __gsignals__ = {
    "user-set-value":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}
    
    def __init__(self):
        
        Gtk.EventBox.__init__(self)
        
        #self.modify_bg(0, Gdk.Color(65000, 65000, 65000))
        self.escala = BalanceBar(Gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))
        
        self.add(self.escala)
        self.show_all()
        
        self.escala.connect('user-set-value', self.emit_valor)
        #self.set_size_request(-1, G.get_pixels(1.2))
        
    def set_progress(self, valor = 0.0):
        """El reproductor modifica la escala."""
        
        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()
        
    def emit_valor(self, widget, valor):
        """El usuario modifica la escala.
        Y se emite la señal con el valor (% float)."""
        
        self.emit("user-set-value", valor)
        
class BalanceBar(Gtk.Scale):
    """Escala de SlicerBalance."""
    
    __gsignals__ = {
    "user-set-value":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}
    
    def __init__(self, ajuste):
        
        Gtk.Scale.__init__(self, orientation = Gtk.Orientation.HORIZONTAL)
        
        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)
        
        self.borde = G.get_pixels(0.2)
        
        icono = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "iconplay.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            G.get_pixels(0.6), G.get_pixels(0.6))
        self.pixbuf = pixbuf.rotate_simple(GdkPixbuf.PixbufRotation.CLOCKWISE)
        
        self.show_all()
        
    def do_motion_notify_event(self, event):
        """Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float)."""
        
        if event.state == Gdk.ModifierType.MOD2_MASK | \
            Gdk.ModifierType.BUTTON1_MASK:
                
            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)
            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)
            
    def do_draw(self, contexto):
        """Dibuja el estado de la barra de progreso."""
        
        rect = self.get_allocation()
        w, h = (rect.width, rect.height)
        
        # Fondo
        Gdk.cairo_set_source_color(contexto, G.BLANCO)
        contexto.paint()
        
        # Relleno de la barra
        ww = w - self.borde * 2
        hh = h/5
        
        Gdk.cairo_set_source_color(contexto, G.NEGRO)
        rect = Gdk.Rectangle()
        
        rect.x, rect.y, rect.width, rect.height = (self.borde, h/5*2, ww, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()
        
        # Relleno de la barra segun progreso
        Gdk.cairo_set_source_color(contexto, G.NARANJA)
        rect = Gdk.Rectangle()
        
        ximage = int(self.ajuste.get_value() * ww / 100)
        rect.x, rect.y, rect.width, rect.height = (self.borde, h/5*2, ximage, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()
        
        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        imgx = ximage - imgw/2
        imgy = float(self.get_allocation().height/2 - imgh/2)
        Gdk.cairo_set_source_pixbuf(contexto, self.pixbuf, imgx, imgy)
        contexto.paint()
        
        return True
    
class ItemSwitch(Gtk.Frame):
    
    __gsignals__ = {
    "switch":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}
    
    def __init__(self, text):
        
        Gtk.Frame.__init__(self)
        
        #self.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        self.set_label(text)
        self.set_label_align(0.5, 1.0)
        
        self.switch = Gtk.Switch()
        self.switch.connect('button-press-event', self.emit_switch)
        
        self.add(self.switch)
        self.show_all()
        
    def emit_switch(self, widget, senial):
        """ Emite la señal switch con el valor correspondiente. """
        
        self.emit("switch", not widget.get_active())
        
class ToolbarSalir(Gtk.Toolbar):
    """Toolbar para confirmar salir de la aplicación."""
    
    __gsignals__ = {
    "salir":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        #self.modify_bg(0, Gdk.Color(65000,65000,65000))
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "alejar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("")
        self.label.set_line_wrap(True)
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 3, expand = False), -1)
        
        archivo = os.path.join(JAMediaWidgetsBASE,
            "Iconos", "acercar.png")
        boton = G.get_boton(archivo, flip = False,
            pixels = G.get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.emit_salir)
        self.insert(boton, -1)
        
        self.insert(G.get_separador(draw = False,
            ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def run(self, nombre_aplicacion):
        """La toolbar se muestra y espera confirmación
        del usuario."""
        
        self.label.set_text("Salir de %s ?" % (nombre_aplicacion))
        self.show()
        
    def emit_salir(self, widget):
        """Confirma Salir de la aplicación."""
        
        self.hide()
        self.emit('salir')

    def cancelar(self, widget= None):
        """Cancela salir de la aplicación."""
        
        self.label.set_text("")
        self.hide()
        
'''
class ToolbarResolucion(Gtk.Toolbar):
    """Pequeña toolbar con controles para
    configurar resolución de video.
    Utilizada por JAMediaVideo."""
    
    __gsignals__ = {"resolucion":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.Toolbar.__init__(self)
        
        self.modify_bg(0, Gdk.Color(0, 0, 0))
        self.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        item = Gtk.ToolItem()
        item.set_expand(True)
        frame = Gtk.Frame()
        frame.set_label("Resolución")
        frame.set_label_align(0.5, 0.5)
        
        combo = ComboResolucion()
        combo.connect('resolucion', self.re_emit_resolucion)
        
        frame.add(combo)
        frame.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        frame.show()
        item.add(frame)
        self.insert(item, -1)
        
        #archivo = os.path.join(JAMediaObjectsPath, "Iconos", "mplayer.png")
        #self.mplayer_boton = G.get_togle_boton(archivo, flip = False,
        #    color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        #self.mplayer_boton.set_tooltip_text("MplayerReproductor")
        #self.mplayer_boton.connect("toggled", self.emit_reproductor, "MplayerReproductor")
        #toolbar.insert(self.mplayer_boton, -1)
        
        #archivo = os.path.join(JAMediaObjectsPath, "Iconos", "JAMedia.png")
        #self.jamedia_boton = G.get_togle_boton(archivo, flip = False,
        #    color = Gdk.Color(0, 0, 0), pixels = G.get_pixels(1))
        #self.jamedia_boton.set_tooltip_text("JAMediaReproductor")
        #self.jamedia_boton.connect("toggled", self.emit_reproductor, "JAMediaReproductor")
        #toolbar.insert(self.jamedia_boton, -1)
        
        self.insert(G.get_separador(draw = False, ancho = 0, expand = True), -1)
        
        self.show_all()
        
    def re_emit_resolucion(self, widget, resolucion):
        """Cuando el usuario cambia la resolución en el combo."""
        
        self.emit('resolucion', resolucion)'''
'''
class ComboResolucion(Gtk.ComboBoxText):
    """Combo con resoluciones de video.
    Utilizado por ToolbarResolucion."""
    
    __gsignals__ = {"resolucion":(GObject.SIGNAL_RUN_FIRST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self):
        
        Gtk.ComboBoxText.__init__(self)
        
        self.append_text('320 x 240')
        self.append_text('640 x 480')
        self.append_text('800 x 600')
        self.set_active(1)
        
        self.show_all()
        
    def do_changed(self):
        
        self.emit('resolucion', self.get_active_text())'''
        
'''
# En base a código de Agustin Zubiaga <aguz@sugarlabs.org>

import os
import gi
from gi.repository import GObject

# http://wiki.laptop.org/go/Accelerometer
ACELEROMETRO = '/sys/devices/platform/lis3lv02d/position'

class Acelerometro(GObject.GObject):

    def __init__(self):
        
        GObject.GObject.__init__(self)
        
        self.acelerometro = None
        
        if os.path.exists(ACELEROMETRO):
            self.acelerometro = open(ACELEROMETRO, 'r')
            self.actualizador = GObject.timeout_add(1000, self.read)
        else:
            print "El Acelerometro no está Presente."
            
    def read(self):
        if self.acelerometro != None:
            self.acelerometro.seek(0)
            print self.acelerometro.read()
            
        """
        x, y, z = self._accelerometer.read()
        if x <= -700:
            self.set_angle(270, False)
        elif x >= 700:
            self.set_angle(90, False)
        elif y <= -700:
            self.set_angle(180, False)
        else:
            self.set_angle(0, False)"""
            
        return True
    
    def close(self):
        if self.acelerometro != None:
            self.acelerometro.close()'''
            