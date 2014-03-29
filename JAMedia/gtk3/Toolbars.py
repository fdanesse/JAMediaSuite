#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Toolbars.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

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
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GLib

BASE_PATH = os.path.dirname(__file__)

#import JAMediaObjects
#from JAMediaObjects.JAMediaWidgets import JAMediaButton

from Globales import get_color
from Globales import get_separador
from Globales import get_boton


class ToolbarAccion(Gtk.Toolbar):
    """
    Toolbar para que el usuario confirme las
    acciones que se realizan sobre items que se
    seleccionan en la lista de reproduccion.
    (Borrar, mover, copiar, quitar).
    """

    __gsignals__ = {
    "Grabar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    "accion-stream": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.lista = None
        self.accion = None
        self.iter = None

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__realizar_accion)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def __realizar_accion(self, widget):
        """
        Ejecuta una accion sobre un archivo o streaming
        en la lista de reprucción cuando el usuario confirma.
        """

        from Globales import get_my_files_directory

        from JAMediaObjects.JAMFileSystem import describe_acceso_uri
        from JAMediaObjects.JAMFileSystem import copiar
        from JAMediaObjects.JAMFileSystem import borrar
        from JAMediaObjects.JAMFileSystem import mover

        uri = self.lista.modelo.get_value(self.iter, 2)

        if describe_acceso_uri(uri):
            if self.accion == "Quitar":
                self.lista.modelo.remove(self.iter)

            elif self.accion == "Copiar":
                if os.path.isfile(uri):
                    copiar(uri, get_my_files_directory())

            elif self.accion == "Borrar":
                if os.path.isfile(uri):
                    if borrar(uri):
                        self.lista.modelo.remove(self.iter)

            elif self.accion == "Mover":
                if os.path.isfile(uri):
                    if mover(uri, get_my_files_directory()):
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
        """
        Configura una accion sobre un archivo o
        streaming y muestra toolbaraccion para que
        el usuario confirme o cancele dicha accion.
        """

        self.lista = lista
        self.accion = accion
        self.iter = iter

        if self.lista and self.accion and self.iter:
            uri = self.lista.modelo.get_value(self.iter, 2)
            texto = uri

            if os.path.exists(uri):
                texto = os.path.basename(uri)

            if len(texto) > 30:
                texto = str(texto[0:30]) + " . . . "

            self.label.set_text("¿%s?: %s" % (accion, texto))
            self.show_all()

    def cancelar(self, widget=None):
        """
        Cancela la accion configurada sobre
        un archivo o streaming en la lista de
        reproduccion.
        """

        self.label.set_text("")
        self.lista = None
        self.accion = None
        self.iter = None
        self.hide()


class ToolbarGrabar(Gtk.Toolbar):
    """
    Informa al usuario cuando se está grabando
    desde un streaming.
    """

    __gtype_name__ = 'ToolbarGrabar'

    __gsignals__ = {
    "stop": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.colors = [get_color("BLANCO"), get_color("NARANJA")]
        self.color = self.colors[0]

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Detener")
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label("Grabador Detenido.")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.show_all()

        boton.connect("clicked", self.__emit_stop)

    def __emit_stop(self, widget=None, event=None):
        """
        Cuando el usuario hace click en el boton stop
        para detener la grabacion en proceso.
        """

        self.stop()
        self.emit("stop")

    def stop(self):
        """
        Setea la toolbar a "no grabando".
        """

        self.color = self.colors[0]
        self.label.modify_fg(0, self.color)
        self.label.set_text("Grabador Detenido.")

        if self.get_visible():
            self.hide()

    def set_info(self, datos):
        """
        Muestra información sobre el proceso de grabación.
        """

        self.label.set_text(datos)
        self.__update()

    def __update(self):
        """
        Cambia los colores de la toolbar
        mientras se esta grabando desde un streaming.
        """

        if self.color == self.colors[0]:
            self.color = self.colors[1]

        elif self.color == self.colors[1]:
            self.color = self.colors[0]

        self.label.modify_fg(0, self.color)

        if not self.get_visible():
            self.show()


class ToolbarLista(Gtk.Toolbar):
    """
    Toolbar de la lista de reproduccion, que contiene
    un menu con las listas standar de JAMedia:
    Radios, Tv, etc . . .
    """

    __gtype_name__ = 'ToolbarLista'

    __gsignals__ = {
    "cargar_lista": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,)),
    "add_stream": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    "menu_activo": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Selecciona una Lista")
        boton.connect("clicked", self.__get_menu)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "agregar.svg")
        self.boton_agregar = get_boton(archivo, flip=False,
            pixels=24)
        self.boton_agregar.set_tooltip_text("Agregar Streaming")
        self.boton_agregar.connect("clicked", self.__emit_add_stream)
        self.insert(self.boton_agregar, -1)

        self.show_all()

    def __get_menu(self, widget):
        """
        El menu con las listas standar de JAMedia.
        """

        self.emit("menu_activo")

        menu = Gtk.Menu()

        item = Gtk.MenuItem("JAMedia Radio")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 0)

        item = Gtk.MenuItem("JAMedia TV")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 1)

        item = Gtk.MenuItem("Mis Emisoras")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 2)

        item = Gtk.MenuItem("Mis Canales")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 3)

        item = Gtk.MenuItem("Web Cams")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 4)

        item = Gtk.MenuItem("Mis Archivos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 5)

        item = Gtk.MenuItem("JAMediaTube")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 6)

        item = Gtk.MenuItem("Audio-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 7)

        item = Gtk.MenuItem("Video-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 8)

        item = Gtk.MenuItem("Archivos Externos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 9)

        menu.show_all()
        menu.attach_to_widget(widget, self.__null)
        menu.popup(None, None, None, None, 1, 0)

    def __null(self):
        pass

    def __emit_load_list(self, indice):
        self.emit("cargar_lista", indice)

    def __emit_add_stream(self, widget):
        self.emit("add_stream")


class Toolbar(Gtk.Toolbar):
    """
    Toolbar principal de JAMedia.
    """

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'config': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'capturar': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "JAMedia.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Autor")
        boton.connect("clicked", self.__show_credits)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "configurar.svg")
        self.configurar = get_boton(archivo, flip=False,
            pixels=24)
        self.configurar.set_tooltip_text("Configuraciones")
        self.configurar.connect("clicked", self.__emit_config)
        self.insert(self.configurar, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "JAMedia-help.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Ayuda")
        boton.connect("clicked", self.__show_help)
        self.insert(boton, -1)

        #archivo = os.path.join(BASE_PATH,
        #    "Iconos", "foto.png")
        #boton = G.get_boton(archivo, flip = False,
        #    pixels = G.get_pixels(1))
        #boton.set_tooltip_text("Captura.")
        #boton.connect("clicked", self.emit_capturar)
        #self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.show_all()

    #def emit_capturar(self, widget):
    #    """
    #    Emite Capturar para obtener la imagen del video.
    #    """

    #    self.emit('capturar')

    def __show_credits(self, widget):

        dialog = Credits(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __show_help(self, widget):

        dialog = Help(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __emit_config(self, widget):
        """
        Cuando se hace click en el boton configurar
        de la toolbar principal de JAMedia.
        """

        self.emit('config')

    def __salir(self, widget):
        """
        Cuando se hace click en el boton salir
        de la toolbar principal de JAMedia.
        """

        self.emit('salir')


class ToolbarInfo(Gtk.Toolbar):
    """
    Informa al usuario sobre el reproductor
    que se esta utilizando.
    Permite Rotar el Video.
    Permite configurar ocultar controles automáticamente.
    """

    __gtype_name__ = 'ToolbarInfo'

    __gsignals__ = {
    'rotar': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'actualizar_streamings': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.ocultar_controles = False

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(BASE_PATH,
            "Iconos", "mplayer.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        self.mplayer = Gtk.ToolItem()
        self.mplayer.add(imagen)
        self.insert(self.mplayer, -1)

        imagen = Gtk.Image()
        icono = os.path.join(BASE_PATH,
            "Iconos", "JAMedia.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, 38)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        self.jamedia = Gtk.ToolItem()
        self.jamedia.add(imagen)
        self.insert(self.jamedia, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        self.boton_izquierda = get_boton(archivo, flip=False,
            pixels=24)
        self.boton_izquierda.set_tooltip_text("Izquierda")
        self.boton_izquierda.connect("clicked", self.__emit_rotar)
        self.insert(self.boton_izquierda, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "rotar.svg")
        self.boton_derecha = get_boton(archivo, flip=True,
            pixels=24)
        self.boton_derecha.set_tooltip_text("Derecha")
        self.boton_derecha.connect("clicked", self.__emit_rotar)
        self.insert(self.boton_derecha, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        label = Gtk.Label("Ocultar Controles:")
        label.show()
        item.add(label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        switch = Gtk.Switch()
        item = Gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        self.descarga = get_boton(archivo, flip=False,
            rotacion=GdkPixbuf.PixbufRotation.CLOCKWISE,
            pixels=24)
        self.descarga.set_tooltip_text("Actualizar Streamings")
        self.descarga.connect("clicked", self.__emit_actualizar_streamings)
        self.insert(self.descarga, -1)

        self.show_all()

        switch.connect('button-press-event', self.__set_controles_view)

    def __emit_actualizar_streamings(self, widget):
        """
        Emite señal para actualizar los
        streamings desde la web de jamedia.
        """

        self.emit('actualizar_streamings')

    def set_reproductor(self, reproductor):
        """
        Muestra el Reproductor Activo.
        """

        if reproductor == "MplayerReproductor":
            self.mplayer.show()
            self.jamedia.hide()

        elif reproductor == "JAMediaReproductor":
            self.jamedia.show()
            self.mplayer.hide()

    def __emit_rotar(self, widget):
        """
        Emite la señal rotar con su valor Izquierda o Derecha.
        """

        if widget == self.boton_derecha:
            self.emit('rotar', "Derecha")

        elif widget == self.boton_izquierda:
            self.emit('rotar', "Izquierda")

    def __set_controles_view(self, widget, senial):
        """
        Almacena el estado de "ocultar_controles".
        """

        self.ocultar_controles = not widget.get_active()


class ToolbarConfig(Gtk.Table):
    """
    Toolbar para intercambiar reproductores (mplayer gst) y
    modificar valores de balance en video.
    """

    __gtype_name__ = 'ToolbarConfig'

    __gsignals__ = {
    "reproductor": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'valor': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_FLOAT, GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.Table.__init__(self, rows=6, columns=1, homogeneous=True)

        from JAMediaObjects.JAMediaWidgets import ToolbarcontrolValores
        from JAMediaObjects.JAMediaGlobales import get_togle_boton

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

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label("Utilizar: ")
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "mplayer.png")
        self.mplayer_boton = get_togle_boton(archivo,
            flip=False,
            pixels=get_pixels(1))
        self.mplayer_boton.set_tooltip_text("MplayerReproductor")
        self.mplayer_boton.connect("toggled",
            self.__emit_reproductor, "MplayerReproductor")
        toolbar.insert(self.mplayer_boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "JAMedia.svg")
        self.jamedia_boton = get_togle_boton(archivo,
            flip=False,
            pixels=get_pixels(1))
        self.jamedia_boton.set_tooltip_text("JAMediaReproductor")
        self.jamedia_boton.connect("toggled",
            self.__emit_reproductor, "JAMediaReproductor")
        toolbar.insert(self.jamedia_boton, -1)

        toolbar.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.attach(toolbar, 0, 1, 5, 6)

        self.show_all()

        self.brillo.connect('valor', self.__emit_senial, 'brillo')
        self.contraste.connect('valor', self.__emit_senial, 'contraste')
        self.saturacion.connect('valor', self.__emit_senial, 'saturacion')
        self.hue.connect('valor', self.__emit_senial, 'hue')
        self.gamma.connect('valor', self.__emit_senial, 'gamma')

    def __emit_senial(self, widget, valor, tipo):
        """
        Emite valor, que representa un valor
        en % float y un valor tipo para:
            brillo - contraste - saturacion - hue - gamma
        """

        self.emit('valor', valor, tipo)

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        """
        Setea las barras segun valores.
        """

        if saturacion != None:
            self.saturacion.set_progress(saturacion)

        if contraste != None:
            self.contraste.set_progress(contraste)

        if brillo != None:
            self.brillo.set_progress(brillo)

        if hue != None:
            self.hue.set_progress(hue)

        if gamma != None:
            self.gamma.set_progress(gamma)

    def __emit_reproductor(self, widget, nombre):
        """
        Emite la señal que cambia de reproductor
        entre mplayer y jamediareproductor (Gst 1.0)
        """

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
    """
    Toolbar para agregar streamings.
    """

    __gtype_name__ = 'ToolbarAddStream'

    __gsignals__ = {
    "add-stream": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING, GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.tipo = None

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        frame = Gtk.Frame()
        frame.set_label('Nombre')
        self.nombre = Gtk.Entry()
        frame.add(self.nombre)
        frame.show_all()
        item = Gtk.ToolItem()
        item.add(frame)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        frame = Gtk.Frame()
        frame.set_label('URL')
        self.url = Gtk.Entry()
        frame.add(self.url)
        frame.show_all()
        item = Gtk.ToolItem()
        self.url.show()
        item.add(frame)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_add_stream)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def __emit_add_stream(self, widget):
        """
        Emite la señal para agregar el streaming.
        """

        nombre, url = (self.nombre.get_text(), self.url.get_text())

        if nombre and url:
            self.emit('add-stream', self.tipo, nombre, url)

        self.tipo = None
        self.nombre.set_text("")
        self.url.set_text("")

        self.hide()

    def set_accion(self, tipo):
        """
        Recibe Tv o Radio para luego enviar
        este dato en la señal add-stream, de modo que
        JAMedia sepa donde agregar el streaming.
        """

        self.nombre.set_text("")
        self.url.set_text("")
        self.tipo = tipo

    def cancelar(self, widget=None):
        """
        Cancela la accion.
        """

        self.tipo = None
        self.nombre.set_text("")
        self.url.set_text("")

        self.hide()


class ToolbarSalir(Gtk.Toolbar):
    """
    Toolbar para confirmar salir de la aplicación.
    """

    __gsignals__ = {
    "salir": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def run(self, nombre_aplicacion):
        """
        La toolbar se muestra y espera confirmación
        del usuario.
        """

        self.label.set_text("¿Salir de %s?" % (nombre_aplicacion))
        self.show()

    def __emit_salir(self, widget):
        """
        Confirma Salir de la aplicación.
        """

        self.cancelar()
        self.emit('salir')

    def cancelar(self, widget=None):
        """
        Cancela salir de la aplicación.
        """

        self.label.set_text("")
        self.hide()
