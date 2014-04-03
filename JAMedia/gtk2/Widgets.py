#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
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
from Globales import get_boton

BASE_PATH = os.path.dirname(__file__)


class My_FileChooser(gtk.FileChooserDialog):
    """
    Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio.
    """

    #__gtype_name__ = 'My_FileChooser'

    __gsignals__ = {
    'archivos-seleccionados': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}

    def __init__(self, parent=None, action=None,
        filter=[], title=None, path=None, mime=[]):

        gtk.FileChooserDialog.__init__(self,
            title=title,
            parent=parent,
            action=action,
            #flags=gtk.DIALOG_MODAL,
            )

        self.modify_bg(0, get_colors("window"))

        if not path:
            path = "file:///media"

        self.set_current_folder_uri(path)

        self.set_select_multiple(True)

        hbox = gtk.HBox()

        boton_abrir_directorio = gtk.Button("Abrir")
        boton_seleccionar_todo = gtk.Button("Seleccionar Todos")
        boton_salir = gtk.Button("Salir")

        boton_salir.connect("clicked", self.__salir)
        boton_abrir_directorio.connect("clicked",
            self.__abrir_directorio)
        boton_seleccionar_todo.connect("clicked",
            self.__seleccionar_todos_los_archivos)

        hbox.pack_end(boton_salir, True, True, 5)
        hbox.pack_end(boton_seleccionar_todo, True, True, 5)
        hbox.pack_end(boton_abrir_directorio, True, True, 5)

        self.set_extra_widget(hbox)

        hbox.show_all()

        if filter:
            filtro = gtk.FileFilter()
            filtro.set_name("Filtro")

            for fil in filter:
                filtro.add_pattern(fil)

            self.add_filter(filtro)

        elif mime:
            filtro = gtk.FileFilter()
            filtro.set_name("Filtro")

            for mi in mime:
                filtro.add_mime_type(mi)

            self.add_filter(filtro)

        self.add_shortcut_folder_uri("file:///media/")

        self.resize(400, 300)

        self.connect("file-activated", self.__file_activated)

    def __file_activated(self, widget):
        """
        Cuando se hace doble click sobre un archivo.
        """

        self.emit('archivos-seleccionados', self.get_filenames())

        self.__salir(None)

    def __seleccionar_todos_los_archivos(self, widget):

        self.select_all()

    def __abrir_directorio(self, widget):
        """
        Manda una señal con la lista de archivos
        seleccionados para cargarse en el reproductor.
        """

        self.emit('archivos-seleccionados', self.get_filenames())
        self.__salir(None)

    def __salir(self, widget):

        self.destroy()


class MenuList(gtk.Menu):
    """
    Menu con opciones para operar sobre el archivo o
    el streaming seleccionado en la lista de reproduccion
    al hacer click derecho sobre él.
    """

    #__gtype_name__ = 'MenuList'

    __gsignals__ = {
    'accion': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        gtk.Menu.__init__(self)

        iter = modelo.get_iter(path)
        uri = modelo.get_value(iter, 2)

        quitar = gtk.MenuItem("Quitar de la Lista")
        self.append(quitar)
        quitar.connect_object("activate", self.__set_accion,
            widget, path, "Quitar")

        from Globales import describe_acceso_uri
        from Globales import get_my_files_directory
        from Globales import get_data_directory
        from Globales import stream_en_archivo

        if describe_acceso_uri(uri):
            lectura, escritura, ejecucion = describe_acceso_uri(uri)

            if lectura and os.path.dirname(uri) != get_my_files_directory():
                copiar = gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__set_accion,
                    widget, path, "Copiar")

            if escritura and os.path.dirname(uri) != get_my_files_directory():
                mover = gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__set_accion,
                    widget, path, "Mover")

            if escritura:
                borrar = gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.__set_accion,
                    widget, path, "Borrar")

        else:
            borrar = gtk.MenuItem("Borrar Streaming")
            self.append(borrar)
            borrar.connect_object("activate", self.__set_accion,
                widget, path, "Borrar")

            listas = [
                os.path.join(get_data_directory(), "JAMediaTV.JAMedia"),
                os.path.join(get_data_directory(), "JAMediaRadio.JAMedia"),
                os.path.join(get_data_directory(), "MisRadios.JAMedia"),
                os.path.join(get_data_directory(), "MisTvs.JAMedia")
                ]

            if (stream_en_archivo(uri, listas[0]) and \
                not stream_en_archivo(uri, listas[3])) or \
                (stream_en_archivo(uri, listas[1]) and \
                not stream_en_archivo(uri, listas[2])):

                copiar = gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__set_accion,
                    widget, path, "Copiar")

                mover = gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__set_accion,
                    widget, path, "Mover")

            grabar = gtk.MenuItem("Grabar")
            self.append(grabar)
            grabar.connect_object("activate", self.__set_accion,
                widget, path, "Grabar")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __null(self):
        pass

    def __set_accion(self, widget, path, accion):
        """
        Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la lista de reproduccion.

        Recibe la lista de reproduccion, una accion a realizar
        sobre el elemento seleccionado en ella y el elemento
        seleccionado y pasa todo a toolbar_accion para pedir
        confirmacion al usuario sobre la accion a realizar.
        """

        iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, iter)


class JAMediaButton(gtk.EventBox):
    """
    Un Boton a medida.
    """

    __gsignals__ = {
    "clicked": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    "click_derecho": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.cn = get_color("BLANCO")
        self.cs = get_color("AMARILLO")
        self.cc = get_color("NARANJA")
        self.text_color = get_color("NEGRO")
        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.set_visible_window(True)
        self.modify_bg(0, self.colornormal)
        self.modify_fg(0, self.text_color)
        self.set_border_width(1)

        self.estado_select = False

        self.add_events(
            gdk.BUTTON_PRESS_MASK |
            gdk.BUTTON_RELEASE_MASK |
            gdk.POINTER_MOTION_MASK |
            gdk.ENTER_NOTIFY_MASK |
            gdk.LEAVE_NOTIFY_MASK)

        self.connect("button_press_event", self.button_press)
        self.connect("button_release_event", self.__button_release)
        self.connect("enter-notify-event", self.__enter_notify_event)
        self.connect("leave-notify-event", self.__leave_notify_event)

        self.imagen = gtk.Image()
        self.add(self.imagen)

        self.show_all()

    def set_colores(self, colornormal=False,
        colorselect=False, colorclicked=False):

        if colornormal:
            self.cn = colornormal

        if colorselect:
            self.cs = colorselect

        if colorclicked:
            self.cc = colorclicked

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        if self.estado_select:
            self.seleccionar()

        else:
            self.des_seleccionar()

    def seleccionar(self):
        """
        Marca como seleccionado
        """

        self.estado_select = True
        self.colornormal = self.cc
        self.colorselect = self.cc
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def des_seleccionar(self):
        """
        Desmarca como seleccionado
        """

        self.estado_select = False

        self.colornormal = self.cn
        self.colorselect = self.cs
        self.colorclicked = self.cc

        self.modify_bg(0, self.colornormal)

    def __button_release(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def __leave_notify_event(self, widget, event):

        self.modify_bg(0, self.colornormal)

    def __enter_notify_event(self, widget, event):

        self.modify_bg(0, self.colorselect)

    def button_press(self, widget, event):

        self.seleccionar()

        if event.button == 1:
            self.emit("clicked", event)

        elif event.button == 3:
            self.emit("click_derecho", event)

    def set_tooltip(self, texto):

        self.set_tooltip_text(texto)

    def set_label(self, texto):

        for child in self.get_children():
            child.destroy()

        label = gtk.Label(texto)
        label.show()
        self.add(label)

    def set_imagen(self, archivo):

        self.imagen.set_from_file(archivo)

    def set_tamanio(self, w, h):

        self.set_size_request(w, h)


class WidgetEfecto_en_Pipe(JAMediaButton):
    """
    Representa un efecto agregado al pipe de JAMediaVideo.
    Es simplemente un objeto gráfico que se agrega debajo del
    visor de video, para que el usuario tenga una referencia de
    los efectos que ha agregado y en que orden se encuentran.
    """

    #__gtype_name__ = 'WidgetEfecto_en_Pipe'

    def __init__(self):

        JAMediaButton.__init__(self)

        self.show_all()

        self.set_colores(
            colornormal=get_color("NEGRO"),
            colorselect=get_color("NEGRO"),
            colorclicked=get_color("NEGRO"))

        self.modify_bg(0, self.colornormal)

    def seleccionar(self):
        pass

    def des_seleccionar(self):
        pass


class DialogoDescarga(gtk.Dialog):

    #__gtype_name__ = 'DialogoDescarga'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            #flags=gtk.DIALOG_MODAL,
            )

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        label = gtk.Label("*** Descargando Streamings de JAMedia ***")
        label.show()

        self.vbox.pack_start(label, True, True, 5)

        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):

        gobject.timeout_add(500, self.__descargar)

    def __descargar(self):

        # FIXME: Agregar control de conexión para evitar errores.
        from Globales import get_streaming_default
        get_streaming_default()

        self.destroy()


class Credits(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            #flags=gtk.DIALOG_MODAL,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        imagen = gtk.Image()
        imagen.set_from_file(
            os.path.join(BASE_PATH,
                "Iconos", "JAMediaCredits.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class Help(gtk.Dialog):

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            #flags=gtk.DIALOG_MODAL,
            buttons=("Cerrar", gtk.RESPONSE_ACCEPT))

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        tabla1 = gtk.Table(columns=5, rows=2, homogeneous=False)

        vbox = gtk.HBox()
        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.anterior = get_boton(
            archivo, flip=True,
            pixels=24,
            tooltip_text="Anterior")
        self.anterior.connect("clicked", self.__switch)
        self.anterior.show()
        vbox.pack_start(self.anterior, False, False, 0)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.siguiente = get_boton(
            archivo,
            pixels=24,
            tooltip_text="Siguiente")
        self.siguiente.connect("clicked", self.__switch)
        self.siguiente.show()
        vbox.pack_end(self.siguiente, False, False, 0)

        tabla1.attach_defaults(vbox, 0, 5, 0, 1)

        self.helps = []

        for x in range(1, 5):
            help = gtk.Image()
            help.set_from_file(
                os.path.join(BASE_PATH,
                    "Iconos", "JAMedia-help%s.png" % x))
            tabla1.attach_defaults(help, 0, 5, 1, 2)

            self.helps.append(help)

        self.vbox.pack_start(tabla1, True, True, 0)
        self.vbox.show_all()

        self.__switch(None)

    def __ocultar(self, objeto):

        if objeto.get_visible():
            objeto.hide()

    def __switch(self, widget):

        if not widget:
            map(self.__ocultar, self.helps[1:])
            self.anterior.hide()
            self.helps[0].show()

        else:
            index = self.__get_index_visible()
            helps = list(self.helps)
            new_index = index

            if widget == self.siguiente:
                if index < len(self.helps) - 1:
                    new_index += 1

            elif widget == self.anterior:
                if index > 0:
                    new_index -= 1

            helps.remove(helps[new_index])
            map(self.__ocultar, helps)
            self.helps[new_index].show()

            if new_index > 0:
                self.anterior.show()

            else:
                self.anterior.hide()

            if new_index < self.helps.index(self.helps[-1]):
                self.siguiente.show()

            else:
                self.siguiente.hide()

    def __get_index_visible(self):

        for help in self.helps:
            if help.get_visible():
                return self.helps.index(help)


class Visor(gtk.DrawingArea):
    """
    Visor generico para utilizar como area de
    reproduccion de videos o dibujar.
    """

    #__gtype_name__ = 'Visor'

    __gsignals__ = {
    "ocultar_controles": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.add_events(
            gdk.KEY_PRESS_MASK |
            gdk.KEY_RELEASE_MASK |
            gdk.POINTER_MOTION_MASK |
            gdk.POINTER_MOTION_HINT_MASK |
            gdk.BUTTON_MOTION_MASK |
            gdk.BUTTON_PRESS_MASK |
            gdk.BUTTON_RELEASE_MASK
        )

        self.show_all()

    def do_motion_notify_event(self, event):
        """
        Cuando se mueve el mouse sobre el visor.
        """

        x, y = (int(event.x), int(event.y))
        rect = self.get_allocation()
        xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)

        if x in range(ww - 60, ww) or y in range(yy, yy + 60) \
            or y in range(hh - 60, hh):

            self.emit("ocultar_controles", False)
            return

        else:
            self.emit("ocultar_controles", True)
            return


class BarraProgreso(gtk.EventBox):
    """
    Barra de progreso para mostrar estado de reproduccion.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("barradeprogreso"))

        self.escala = ProgressBar(
            gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0

        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)
        self.set_size_request(-1, 24)

    def set_progress(self, valor=0):
        """
        El reproductor modifica la escala.
        """

        if self.escala.presed:
            return

        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()

    def __emit_valor(self, widget, valor):
        """
        El usuario modifica la escala.
        """

        if self.valor != valor:
            self.valor = valor
            self.emit("user-set-value", valor)


class ProgressBar(gtk.HScale):
    """
    Escala de SlicerBalance.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(0, get_colors("barradeprogreso"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        # FIXME: Verificar
        self.presed = False
        self.ancho, self.borde = (10, 10)

        icono = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        pixbuf = gdk.pixbuf_new_from_file_at_size(icono,
            24, 24)
        self.pixbuf = pixbuf.rotate_simple(
            gdk.PIXBUF_ROTATE_CLOCKWISE)

        self.connect("button-press-event", self.__button_press_event)
        self.connect("button-release-event", self.__button_release_event)
        self.connect("motion-notify-event", self.__motion_notify_event)
        self.connect("expose_event", self.__expose)

        self.show_all()

    def __button_press_event(self, widget, event):

        self.presed = True

    def __button_release_event(self, widget, event):

        self.presed = False

    def __motion_notify_event(self, widget, event):
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

        # todo el widget
        gc.set_rgb_fg_color(get_colors("barradeprogreso"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        # vacio
        gc.set_rgb_fg_color(gdk.Color(0, 0, 0))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        # progreso
        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(gdk.Color(65000, 26000, 0))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # borde de progreso
        gc.set_rgb_fg_color(get_colors("window"))
        self.window.draw_rectangle(gc, False, xx, yy, ww, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True


class ControlVolumen(gtk.VolumeButton):
    """
    Botón con escala para controlar el volúmen
    de reproducción en los reproductores.
    """

    __gsignals__ = {
    "volumen": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.VolumeButton.__init__(self)

        self.connect("value-changed", self.__value_changed)
        self.show_all()

    def __value_changed(self, widget, valor):
        """
        Cuando el usuario desplaza la escala
        emite el valor en float de 0.0 a 1.0.
        """

        self.emit('volumen', valor)


class MouseSpeedDetector(gobject.GObject):
    """
    Verifica posición y moviemiento del mouse.
    estado puede ser:
        fuera       (está fuera de la ventana según self.parent)
        moviendose
        detenido
    """

    __gsignals__ = {
        'estado': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self, parent):

        gobject.GObject.__init__(self)

        self.parent = parent

        self.actualizador = False
        self.mouse_pos = (0, 0)

    def __handler(self):
        """
        Emite la señal de estado cada 60 segundos.
        """

        try:
            display, posx, posy = gdk.display_get_default(
                ).get_window_at_pointer()

        except:
            return True

        if posx > 0 and posy > 0:
            if posx != self.mouse_pos[0] or posy != self.mouse_pos[1]:
                self.mouse_pos = (posx, posy)
                self.emit("estado", "moviendose")

            else:
                self.emit("estado", "detenido")

        else:
            self.emit("estado", "fuera")

        return True

    def new_handler(self, reset):
        """
        Resetea el controlador o lo termina según reset.
        """

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = gobject.timeout_add(1000, self.__handler)
