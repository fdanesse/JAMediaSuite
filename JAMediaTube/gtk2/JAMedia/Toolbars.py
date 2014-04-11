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

import gtk
from gtk import gdk
import gobject

from Globales import get_color
from Globales import get_colors
from Globales import get_separador
from Globales import get_boton
from Globales import get_togle_boton

BASE_PATH = os.path.dirname(__file__)


class ToolbarAccion(gtk.Toolbar):
    """
    Toolbar para que el usuario confirme las
    acciones que se realizan sobre items que se
    seleccionan en la lista de reproduccion.
    (Borrar, mover, copiar, quitar).
    """

    __gsignals__ = {
    "Grabar": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "accion-stream": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

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

        item = gtk.ToolItem()
        self.label = gtk.Label("")
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

        from Globales import describe_acceso_uri
        from Globales import copiar
        from Globales import borrar
        from Globales import mover

        uri = self.lista.get_model().get_value(self.iter, 2)

        if describe_acceso_uri(uri):
            if self.accion == "Quitar":
                path = self.lista.get_model().get_path(self.iter)
                path = (path[0] - 1, )

                self.lista.get_model().remove(self.iter)

                try:
                    self.lista.get_selection().select_iter(
                        self.lista.get_model().get_iter(path))

                except:
                    self.lista.seleccionar_primero()

            elif self.accion == "Copiar":
                if os.path.isfile(uri):
                    copiar(uri, get_my_files_directory())

            elif self.accion == "Borrar":
                if os.path.isfile(uri):
                    if borrar(uri):
                        path = self.lista.get_model().get_path(self.iter)
                        path = (path[0] - 1, )

                        self.lista.get_model().remove(self.iter)

                        try:
                            self.lista.get_selection().select_iter(
                                self.lista.get_model().get_iter(path))

                        except:
                            self.lista.seleccionar_primero()

            elif self.accion == "Mover":
                if os.path.isfile(uri):
                    if mover(uri, get_my_files_directory()):
                        path = self.lista.get_model().get_path(self.iter)
                        path = (path[0] - 1, )

                        self.lista.get_model().remove(self.iter)

                        try:
                            self.lista.get_selection().select_iter(
                                self.lista.get_model().get_iter(path))

                        except:
                            self.lista.seleccionar_primero()
        else:
            if self.accion == "Quitar":
                path = self.lista.get_model().get_path(self.iter)
                path = (path[0] - 1, )

                self.lista.get_model().remove(self.iter)

                try:
                    self.lista.get_selection().select_iter(
                        self.lista.get_model().get_iter(path))

                except:
                    self.lista.seleccionar_primero()

            elif self.accion == "Borrar":
                self.emit("accion-stream", "Borrar", uri)
                path = self.lista.get_model().get_path(self.iter)
                path = (path[0] - 1, )

                self.lista.get_model().remove(self.iter)

                try:
                    self.lista.get_selection().select_iter(
                        self.lista.get_model().get_iter(path))

                except:
                    self.lista.seleccionar_primero()

            elif self.accion == "Copiar":
                self.emit("accion-stream", "Copiar", uri)

            elif self.accion == "Mover":
                self.emit("accion-stream", "Mover", uri)
                path = self.lista.get_model().get_path(self.iter)
                path = (path[0] - 1, )

                self.lista.get_model().remove(self.iter)

                try:
                    self.lista.get_selection().select_iter(
                        self.lista.get_model().get_iter(path))

                except:
                    self.lista.seleccionar_primero()

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
            uri = self.lista.get_model().get_value(self.iter, 2)
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


class ToolbarGrabar(gtk.EventBox):
    """
    Informa al usuario cuando se está grabando
    desde un streaming.
    """

    #__gtype_name__ = 'ToolbarGrabar'

    __gsignals__ = {
    "stop": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.colors = [get_color("BLANCO"), get_color("NARANJA")]
        self.color = self.colors[0]

        self.toolbar = gtk.Toolbar()
        self.toolbar.modify_bg(0, get_colors("drawingplayer"))

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "stop.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Detener")
        self.toolbar.insert(boton, -1)

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("Grabador Detenido.")
        self.label.show()
        item.add(self.label)
        self.toolbar.insert(item, -1)

        self.add(self.toolbar)

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


class ToolbarLista(gtk.Toolbar):
    """
    Toolbar de la lista de reproduccion, que contiene
    un menu con las listas standar de JAMedia:
    Radios, Tv, etc . . .
    """

    #__gtype_name__ = 'ToolbarLista'

    __gsignals__ = {
    "cargar_lista": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "add_stream": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, []),
    "menu_activo": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("barradeprogreso"))

        archivo = os.path.join(BASE_PATH,
            "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Selecciona una Lista")
        boton.connect("clicked", self.__get_menu)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("")
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

        menu = gtk.Menu()

        item = gtk.MenuItem("JAMedia Radio")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 0)

        item = gtk.MenuItem("JAMedia TV")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 1)

        item = gtk.MenuItem("Mis Emisoras")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 2)

        item = gtk.MenuItem("Mis Canales")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 3)

        item = gtk.MenuItem("Web Cams")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 4)

        item = gtk.MenuItem("Mis Archivos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 5)

        item = gtk.MenuItem("JAMediaTube")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 6)

        item = gtk.MenuItem("Audio-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 7)

        item = gtk.MenuItem("Video-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 8)

        item = gtk.MenuItem("Archivos Externos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 9)

        menu.show_all()
        menu.attach_to_widget(widget, self.__null)
        gtk.Menu.popup(menu, None, None, None, 1, 0)

    def __null(self):
        pass

    def __emit_load_list(self, indice):
        self.emit("cargar_lista", indice)

    def __emit_add_stream(self, widget):
        self.emit("add_stream")


class Toolbar(gtk.Toolbar):
    """
    Toolbar principal de JAMedia.
    """

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, []),
    'config': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("barradeprogreso"))

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "JAMedia.svg")
        boton = get_boton(archivo, flip=False,
            pixels=35)
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

    def __show_credits(self, widget):

        from Widgets import Credits
        dialog = Credits(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __show_help(self, widget):

        from Widgets import Help
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


class ToolbarInfo(gtk.Toolbar):
    """
    Informa al usuario sobre el reproductor
    que se esta utilizando.
    Permite Rotar el Video.
    Permite configurar ocultar controles automáticamente.
    """

    #__gtype_name__ = 'ToolbarInfo'

    __gsignals__ = {
    'rotar': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'actualizar_streamings': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("barradeprogreso"))

        self.ocultar_controles = False

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

        item = gtk.ToolItem()
        label = gtk.Label("Ocultar Controles:")
        label.show()
        item.add(label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        switch = gtk.CheckButton()
        item = gtk.ToolItem()
        item.set_expand(False)
        item.add(switch)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        self.descarga = get_boton(archivo, flip=False,
            rotacion=gdk.PIXBUF_ROTATE_CLOCKWISE,
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


class ToolbarConfig(gtk.Table):
    """
    Toolbar para intercambiar reproductores (mplayer gst) y
    modificar valores de balance en video.
    """

    #__gtype_name__ = 'ToolbarConfig'

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_CLEANUP, gobject.TYPE_NONE,
        (gobject.TYPE_FLOAT, gobject.TYPE_STRING))}

    def __init__(self):

        gtk.Table.__init__(self, rows=5, columns=1, homogeneous=True)

        self.modify_bg(0, get_colors("window"))

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


class ToolbarcontrolValores(gtk.Toolbar):
    """
    Toolbar con escala para modificar
    valores de balance en video, utilizada
    por ToolbarBalanceConfig.
    """

    __gsignals__ = {
    'valor': (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self, label):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.titulo = label

        self.escala = SlicerBalance()

        item = gtk.ToolItem()
        item.set_expand(True)

        self.frame = gtk.Frame()
        self.frame.set_border_width(4)
        self.frame.set_label(self.titulo)
        self.frame.set_label_align(0.5, 1.0)
        event = gtk.EventBox()
        event.set_border_width(4)
        event.add(self.escala)
        self.frame.add(event)
        self.frame.show_all()
        item.add(self.frame)
        self.insert(item, -1)

        self.show_all()

        self.escala.connect("user-set-value", self.__user_set_value)

    def __user_set_value(self, widget=None, valor=None):
        """
        Recibe la posicion en la barra de
        progreso (en % float), y re emite los valores.
        """

        self.emit('valor', valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))

    def set_progress(self, valor):
        """
        Establece valores en la escala.
        """

        self.escala.set_progress(valor)
        self.frame.set_label("%s: %s%s" % (self.titulo, int(valor), "%"))


class SlicerBalance(gtk.EventBox):
    """
    Barra deslizable para cambiar valores de Balance en Video.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.escala = BalanceBar(gtk.Adjustment(0.0, 0.0,
            101.0, 0.1, 1.0, 1.0))

        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)

    def set_progress(self, valor=0.0):
        """
        El reproductor modifica la escala.
        """

        self.escala.ajuste.set_value(valor)
        self.escala.queue_draw()

    def __emit_valor(self, widget, valor):
        """
        El usuario modifica la escala.
        Y se emite la señal con el valor (% float).
        """

        self.emit("user-set-value", valor)


class BalanceBar(gtk.HScale):
    """
    Escala de SlicerBalance.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.ancho, self.borde = (7, 10)

        icono = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        pixbuf = gdk.pixbuf_new_from_file_at_size(icono,
            16, 16)
        self.pixbuf = pixbuf.rotate_simple(
            gdk.PIXBUF_ROTATE_CLOCKWISE)

        self.connect("expose_event", self.__expose)

        self.show_all()

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """

        if event.state == gdk.MOD2_MASK | \
            gdk.BUTTON1_MASK:

            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)
            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

    def __expose(self, widget, event):
        """
        Dibuja el estado de la barra de progreso.
        """

        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        gc.set_rgb_fg_color(gdk.color_parse("#ffffff"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        gc.set_rgb_fg_color(gdk.Color(0, 0, 0))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(gdk.Color(65000, 26000, 0))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True


class ToolbarAddStream(gtk.Toolbar):
    """
    Toolbar para agregar streamings.
    """

    #__gtype_name__ = 'ToolbarAddStream'

    __gsignals__ = {
    "add-stream": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_STRING))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

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

        frame = gtk.Frame()
        frame.set_label('Nombre')
        self.nombre = gtk.Entry()
        event = gtk.EventBox()
        event.modify_bg(0, get_colors("window"))
        event.set_border_width(4)
        event.add(self.nombre)
        frame.add(event)
        frame.show_all()
        item = gtk.ToolItem()
        item.add(frame)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        frame = gtk.Frame()
        frame.set_label('URL')
        self.url = gtk.Entry()
        event = gtk.EventBox()
        event.modify_bg(0, get_colors("window"))
        event.set_border_width(4)
        event.add(self.url)
        frame.add(event)
        frame.show_all()
        item = gtk.ToolItem()
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


class ToolbarSalir(gtk.Toolbar):
    """
    Toolbar para confirmar salir de la aplicación.
    """

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_CLEANUP,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

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

        item = gtk.ToolItem()
        self.label = gtk.Label("")
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
