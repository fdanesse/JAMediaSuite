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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import GLib

from Globales import get_color
from Globales import get_colors
from Globales import get_separador
from Globales import get_boton

BASE_PATH = os.path.dirname(__file__)


class My_FileChooser(Gtk.FileChooserDialog):
    """
    Selector de Archivos para poder cargar archivos
    desde cualquier dispositivo o directorio.
    """

    __gtype_name__ = 'My_FileChooser'

    __gsignals__ = {
    'archivos-seleccionados': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, parent=None, action=None,
        filter=[], title=None, path=None, mime=[]):

        Gtk.FileChooserDialog.__init__(self,
            title=title,
            parent=parent,
            action=action,
            flags=Gtk.DialogFlags.MODAL)

        self.modify_bg(0, get_colors("window"))

        if not path:
            path = "file:///media"

        self.set_current_folder_uri(path)

        self.set_select_multiple(True)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        boton_abrir_directorio = Gtk.Button("Abrir")
        boton_seleccionar_todo = Gtk.Button("Seleccionar Todos")
        boton_salir = Gtk.Button("Salir")

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
            filtro = Gtk.FileFilter()
            filtro.set_name("Filtro")

            for fil in filter:
                filtro.add_pattern(fil)

            self.add_filter(filtro)

        elif mime:
            filtro = Gtk.FileFilter()
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


class MenuList(Gtk.Menu):
    """
    Menu con opciones para operar sobre el archivo o
    el streaming seleccionado en la lista de reproduccion
    al hacer click derecho sobre él.
    """

    __gtype_name__ = 'MenuList'

    __gsignals__ = {
    'accion': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos, tiempo, path, modelo):

        Gtk.Menu.__init__(self)

        iter = modelo.get_iter(path)
        uri = modelo.get_value(iter, 2)

        quitar = Gtk.MenuItem("Quitar de la Lista")
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
                copiar = Gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__set_accion,
                    widget, path, "Copiar")

            if escritura and os.path.dirname(uri) != get_my_files_directory():
                mover = Gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__set_accion,
                    widget, path, "Mover")

            if escritura:
                borrar = Gtk.MenuItem("Borrar el Archivo")
                self.append(borrar)
                borrar.connect_object("activate", self.__set_accion,
                    widget, path, "Borrar")

        else:
            borrar = Gtk.MenuItem("Borrar Streaming")
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

                copiar = Gtk.MenuItem("Copiar a JAMedia")
                self.append(copiar)
                copiar.connect_object("activate", self.__set_accion,
                    widget, path, "Copiar")

                mover = Gtk.MenuItem("Mover a JAMedia")
                self.append(mover)
                mover.connect_object("activate", self.__set_accion,
                    widget, path, "Mover")

            grabar = Gtk.MenuItem("Grabar")
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


class JAMediaButton(Gtk.EventBox):
    """
    Un Boton a medida.
    """

    __gsignals__ = {
    "clicked": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
    "click_derecho": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

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
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK |
            Gdk.EventMask.ENTER_NOTIFY_MASK |
            Gdk.EventMask.LEAVE_NOTIFY_MASK)

        self.connect("button_press_event", self.button_press)
        self.connect("button_release_event", self.__button_release)
        self.connect("enter-notify-event", self.__enter_notify_event)
        self.connect("leave-notify-event", self.__leave_notify_event)

        self.imagen = Gtk.Image()
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

        label = Gtk.Label(texto)
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

    __gtype_name__ = 'WidgetEfecto_en_Pipe'

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


class DialogoDescarga(Gtk.Dialog):

    __gtype_name__ = 'DialogoDescarga'

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL)

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        label = Gtk.Label("*** Descargando Streamings de JAMedia ***")
        label.show()

        self.vbox.pack_start(label, True, True, 5)

        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):

        GLib.timeout_add(500, self.__descargar)

    def __descargar(self):

        # FIXME: Agregar control de conexión para evitar errores.
        from Globales import get_streaming_default
        get_streaming_default()

        self.destroy()


class Credits(Gtk.Dialog):

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        imagen = Gtk.Image()
        imagen.set_from_file(
            os.path.join(BASE_PATH,
                "Iconos", "JAMediaCredits.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class Help(Gtk.Dialog):

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_decorated(False)
        self.modify_bg(0, get_colors("window"))
        self.set_border_width(15)

        tabla1 = Gtk.Table(columns=5, rows=2, homogeneous=False)

        vbox = Gtk.HBox()
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
            help = Gtk.Image()
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


class Visor(Gtk.DrawingArea):
    """
    Visor generico para utilizar como area de
    reproduccion de videos o dibujar.
    """

    __gtype_name__ = 'Visor'

    __gsignals__ = {
    "ocultar_controles": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_BOOLEAN,))}

    def __init__(self):

        Gtk.DrawingArea.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

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

        #self.connect("touch-event", self.__touch)

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


class BarraProgreso(Gtk.EventBox):
    """
    Barra de progreso para mostrar estado de reproduccion.
    """

    __gsignals__ = {
    "user-set-value": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT, ))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        #self.modify_bg(0, get_color("BLANCO"))
        self.modify_bg(0, get_colors("barradeprogreso"))

        self.escala = ProgressBar(
            Gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

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
            self.escala.get_adjustment().set_value(valor)
            self.escala.queue_draw()

    def __emit_valor(self, widget, valor):
        """
        El usuario modifica la escala.
        """

        if self.valor != valor:
            self.valor = valor
            self.emit("user-set-value", valor)


class ProgressBar(Gtk.Scale):
    """
    Escala de BarraProgreso.
    """

    __gsignals__ = {
    "user-set-value": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}

    def __init__(self, ajuste):

        Gtk.Scale.__init__(self,
            orientation=Gtk.Orientation.HORIZONTAL)

        self.set_adjustment(ajuste)
        self.set_digits(0)
        self.set_draw_value(False)

        self.presed = False
        self.borde = 10

        icono = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            24, 24)
        self.pixbuf = pixbuf.rotate_simple(
            GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)

        self.show_all()

    def do_button_press_event(self, event):

        self.presed = True

    def do_button_release_event(self, event):

        self.presed = False

    def do_motion_notify_event(self, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        """

        if event.state == Gdk.ModifierType.MOD2_MASK | \
            Gdk.ModifierType.BUTTON1_MASK:

            rect = self.get_allocation()
            x, y = (self.borde, self.borde)
            w, h = (rect.width - (
                self.borde * 2), rect.height - (self.borde * 2))
            eventx, eventy = (int(event.x) - x, int(event.y) - y)

            if (eventx > int(x) and eventx < int(w)):
                valor = float(eventx * 100 / w)
                self.get_adjustment().set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

    def do_draw(self, contexto):
        """
        Dibuja el estado de la barra de progreso.
        """

        rect = self.get_allocation()
        w, h = (rect.width, rect.height)

        # Relleno de la barra
        ww = w - self.borde * 2
        hh = 10 #h - self.borde * 2
        Gdk.cairo_set_source_color(contexto, get_color("NEGRO"))
        rect = Gdk.Rectangle()
        rect.x, rect.y, rect.width, rect.height = (
            self.borde, self.borde, ww, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()

        # Relleno de la barra segun progreso
        Gdk.cairo_set_source_color(contexto, get_color("NARANJA"))
        rect = Gdk.Rectangle()
        ximage = int(self.get_adjustment().get_value() * ww / 100)
        rect.x, rect.y, rect.width, rect.height = (self.borde, self.borde,
            ximage, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()

        # borde del progreso
        Gdk.cairo_set_source_color(contexto, get_color("BLANCO"))
        rect = Gdk.Rectangle()
        rect.x, rect.y, rect.width, rect.height = (
            self.borde, self.borde, ww, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.stroke()

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        imgx = ximage
        imgy = float(self.borde + hh / 2 - imgh / 2)
        Gdk.cairo_set_source_pixbuf(contexto, self.pixbuf, imgx, imgy)
        contexto.paint()

        return True


class ControlVolumen(Gtk.VolumeButton):
    """
    Botón con escala para controlar el volúmen
    de reproducción en los reproductores.
    """

    __gsignals__ = {
    "volumen": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_FLOAT,))}

    def __init__(self):

        Gtk.VolumeButton.__init__(self)

        self.show_all()

    def do_value_changed(self, valor):
        """
        Cuando el usuario desplaza la escala
        emite el valor en float de 0.0 a 1.0.
        """

        self.emit('volumen', valor)


class MouseSpeedDetector(GObject.GObject):
    """
    Verifica posición y moviemiento del mouse.
    estado puede ser:
        fuera       (está fuera de la ventana según self.parent)
        moviendose
        detenido
    """

    __gsignals__ = {
        'estado': (GObject.SignalFlags.RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self, parent):

        GObject.GObject.__init__(self)

        self.parent = parent

        self.actualizador = False
        self.mouse_pos = (0, 0)

    def __handler(self):
        """
        Emite la señal de estado cada 60 segundos.
        """

        display, posx, posy = self.parent.get_display().get_window_at_pointer()

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
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = GLib.timeout_add(1000, self.__handler)
