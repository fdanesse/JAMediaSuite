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
import gobject

from Globales import get_colors
from Globales import get_separador
from Globales import get_boton

BASE_PATH = os.path.dirname(__file__)


class Toolbar(gtk.Toolbar):
    """
    Toolbar principal de JAMediaTube.
    """

    __gsignals__ = {
    'salir': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'switch': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("drawingplayer"))

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "JAMediaTube.svg")
        boton = get_boton(archivo, flip=False, pixels=35)
        boton.set_tooltip_text("Autor")
        boton.connect("clicked", self.__show_credits)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "JAMedia.svg")
        self.jamedia = get_boton(archivo, flip=False, pixels=35)
        self.jamedia.set_tooltip_text("Cambiar a JAMedia")
        self.jamedia.connect("clicked", self.__emit_switch)
        self.insert(self.jamedia, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "JAMedia-help.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Ayuda")
        boton.connect("clicked", self.__show_help)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        self.show_all()

    def __show_credits(self, widget):
        dialog = Credits(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __show_help(self, widget):
        dialog = Help(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __emit_switch(self, widget):
        """
        Cambia de JAMediaTube a JAMedia.
        """
        self.emit('switch')

    def __salir(self, widget):
        self.emit('salir')


class Toolbar_Busqueda(gtk.Toolbar):
    """
    Toolbar con widgets de busqueda.
    """

    __gsignals__ = {
    "comenzar_busqueda": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        item = gtk.ToolItem()
        label = gtk.Label("Buscar por: ")
        label.show()
        item.add(label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.entrytext = gtk.Entry()
        self.entrytext.set_size_request(400, -1)
        self.entrytext.set_max_length(50)
        self.entrytext.set_tooltip_text("Escribe lo que Buscas")
        self.entrytext.show()
        self.entrytext.connect('activate', self.__activate_entrytext)
        item.add(self.entrytext)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Comenzar Búsqueda")
        boton.connect("clicked", self.__emit_buscar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.show_all()

    def __emit_buscar(self, widget=None):
        texto = self.entrytext.get_text()
        self.entrytext.set_text("")
        if texto:
            self.emit("comenzar_busqueda", texto)

    def __activate_entrytext(self, widget):
        """
        Cuando se da enter en el entrytext.
        """
        self.__emit_buscar()


class Alerta_Busqueda(gtk.Toolbar):
    """
    Para informar que se está buscando con JAMediaTube.
    """

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(0, get_colors("window"))

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(BASE_PATH, "Iconos", "yt_videos_black.png")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 24)
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        self.label = gtk.Label("")
        self.label.set_justify(gtk.JUSTIFY_LEFT)
        #self.label.set_line_wrap(True)
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.show_all()


class WidgetVideoItem(gtk.EventBox):

    __gsignals__ = {
    #"clicked": (gobject.SIGNAL_RUN_FIRST,
    #    gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
    "click_derecho": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}

    def __init__(self, videodict):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("widgetvideoitem"))
        self.set_border_width(2)

        self.videodict = videodict

        hbox = gtk.HBox()
        vbox = gtk.VBox()

        keys = self.videodict.keys()
        if "previews" in keys:
            imagen = gtk.Image()
            hbox.pack_start(imagen, False, False, 3)

            if type(self.videodict["previews"]) == list:
                # siempre hay 4 previews.
                url = self.videodict["previews"][0][0]
                import time
                archivo = "/dev/shm/preview%d" % time.time()

                try:
                    # FIXME: Porque Falla si no hay Conexión.
                    import urllib
                    fileimage, headers = urllib.urlretrieve(url, archivo)
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                        fileimage, 200, 150)
                    imagen.set_from_pixbuf(pixbuf)

                    # Convertir imagen a string por si se quiere guardar.
                    import base64
                    pixbuf_file = open(fileimage, 'rb')
                    image_string = base64.b64encode(pixbuf_file.read())
                    pixbuf_file.close()
                    self.videodict["previews"] = image_string
                except:
                    print "No hay Conexión a Internet."

                if os.path.exists(archivo):
                    os.remove(archivo)

            else:
                import base64
                loader = gtk.gdk.PixbufLoader()
                loader.set_size(200, 150)
                image_string = base64.b64decode(self.videodict["previews"])
                loader.write(image_string)
                loader.close()

                pixbuf = loader.get_pixbuf()
                imagen.set_from_pixbuf(pixbuf)

        vbox.pack_start(gtk.Label("%s: %s" % ("id",
            self.videodict["id"])), True, True, 0)
        vbox.pack_start(gtk.Label("%s: %s" % ("Título",
            self.videodict["titulo"])), True, True, 0)
        vbox.pack_start(gtk.Label("%s: %s" % ("Categoría",
            self.videodict["categoria"])), True, True, 0)
        #vbox.pack_start(gtk.Label("%s: %s" % ("Etiquetas",
        #    self.videodict["etiquetas"])), True, True, 0)
        #vbox.pack_start(gtk.Label("%s: %s" % ("Descripción",
        #   self.videodict["descripcion"])), True, True, 0)
        vbox.pack_start(gtk.Label("%s: %s %s" % ("Duración",
            int(float(self.videodict["duracion"]) / 60.0), "Minutos")),
            True, True, 0)
        #vbox.pack_start(gtk.Label("%s: %s" % ("Reproducción en la Web",
        #   self.videodict["flash player"])), True, True, 0)
        vbox.pack_start(gtk.Label("%s: %s" % ("url",
            self.videodict["url"])), True, True, 0)

        for label in vbox.get_children():
            label.set_alignment(0.0, 0.5)

        hbox.pack_start(vbox, False, False, 5)
        self.add(hbox)

        self.show_all()

        self.connect("button_press_event", self.__button_press)

    def __button_press(self, widget, event):
    #    self.modify_bg(0, self.colorclicked)
    #    if event.button == 1:
    #        self.emit("clicked", event)
    #    elif event.button == 3:
            self.emit("click_derecho", event)


class Toolbar_Descarga(gtk.VBox):

    __gsignals__ = {
    'end': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.VBox.__init__(self)

        self.toolbar = gtk.Toolbar()
        self.toolbar.modify_bg(0, get_colors("download"))

        self.label_titulo = None
        self.label_progreso = None
        self.progress = 0.0
        self.barra_progreso = None
        self.estado = False

        self.actualizador = False

        self.datostemporales = None
        self.ultimosdatos = None
        self.contadortestigo = 0

        self.video_item = None
        self.url = None
        self.titulo = None

        from JAMediaYoutube import JAMediaYoutube
        self.jamediayoutube = JAMediaYoutube()

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label_titulo = gtk.Label("")
        self.label_titulo.show()
        item.add(self.label_titulo)
        self.toolbar.insert(item, -1)

        self.toolbar.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label_progreso = gtk.Label("")
        self.label_progreso.show()
        item.add(self.label_progreso)
        self.toolbar.insert(item, -1)

        #self.toolbar.insert(G.get_separador(draw = False,
        #    ancho = 0, expand = True), -1)

        # FIXME: BUG. Las descargas no se cancelan.
        #archivo = os.path.join(BASE_PATH, "Iconos","stop.png")
        #boton = G.get_boton(archivo, flip = False,
        #    pixels = G.get_pixels(1))
        #boton.set_tooltip_text("Cancelar")
        #boton.connect("clicked", self.cancel_download)
        #self.toolbar.insert(boton, -1)

        #self.toolbar.insert(G.get_separador(draw = False,
        #    ancho = 3, expand = False), -1)

        self.barra_progreso = Progreso_Descarga()
        self.barra_progreso.show()

        self.pack_start(self.toolbar, False, False, 0)
        self.pack_start(self.barra_progreso, False, False, 0)

        self.show_all()

        self.jamediayoutube.connect("progress_download",
            self.__progress_download)

    def download(self, video_item):
        """
        Comienza a descargar un video-item.
        """
        self.estado = True
        self.progress = 0.0
        self.datostemporales = None
        self.ultimosdatos = None
        self.contadortestigo = 0

        self.video_item = video_item
        self.url = video_item.videodict["url"]
        self.titulo = video_item.videodict["titulo"]

        texto = self.titulo
        if len(self.titulo) > 30:
            texto = str(self.titulo[0:30]) + " . . . "

        self.label_titulo.set_text(texto)
        self.jamediayoutube.download(self.url, self.titulo)

        if self.actualizador:
            gobject.source_remove(self.actualizador)

        self.actualizador = gobject.timeout_add(1000, self.__handle)

        self.show_all()

    def __handle(self):
        """
        Verifica que se esté descargando el archivo.
        """
        if self.ultimosdatos != self.datostemporales:
            self.ultimosdatos = self.datostemporales
            self.contadortestigo = 0
        else:
            self.contadortestigo += 1

        if self.contadortestigo > 15:
            print "\nNo se pudo controlar la descarga de:"
            print ("%s %s\n") % (self.titulo, self.url)
            self.__cancel_download()
            return False

        return True

    def __progress_download(self, widget, progress):
        """
        Muestra el progreso de la descarga.
        """
        self.datostemporales = progress
        datos = progress.split(" ")

        if datos[0] == '[youtube]':
            dat = progress.split('[youtube]')[1]
            if self.label_progreso.get_text() != dat:
                self.label_progreso.set_text(dat)

        elif datos[0] == '[download]':
            dat = progress.split('[download]')[1]
            if self.label_progreso.get_text() != dat:
                self.label_progreso.set_text(dat)

        elif datos[0] == '\r[download]':
            porciento = 0.0

            if "%" in datos[2]:
                porciento = datos[2].split("%")[0]
            elif "%" in datos[3]:
                porciento = datos[3].split("%")[0]

            porciento = float(porciento)
            self.barra_progreso.set_progress(valor=int(porciento))

            if porciento >= 100.0:  # nunca llega
                self.__cancel_download()
                return False
            else:
                dat = progress.split("[download]")[1]
                if self.label_progreso.get_text() != dat:
                    self.label_progreso.set_text(dat)

        if "100.0%" in progress.split(" "):
            self.__cancel_download()
            return False

        if not self.get_visible():
            self.show()

        return True

    def __cancel_download(self, button=None, event=None):
        """
        Cancela la descarga actual.
        """
        # FIXME: No funciona correctamente, la descarga continúa.
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False
        try:
            self.jamediayoutube.reset()

        except:
            pass

        try:
            self.video_item.destroy()
        except:
            pass

        self.estado = False
        self.emit("end")
        return False


class Progreso_Descarga(gtk.EventBox):
    """
    Barra de progreso para mostrar estado de descarga.
    """

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, get_colors("download"))

        self.escala = ProgressBar(
            gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0

        self.add(self.escala)
        self.show_all()

        self.set_size_request(-1, 28)
        self.set_progress(0)

    def set_progress(self, valor=0):
        """
        El reproductor modifica la escala.
        """
        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()


class ProgressBar(gtk.HScale):

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self, ajuste)

        self.modify_bg(0, get_colors("widgetvideoitem"))

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)
        self.borde, self.ancho = (15, 10)

        self.connect("expose_event", self.expose)

    def expose(self, widget, event):
        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        # todo el widget
        gc.set_rgb_fg_color(get_colors("window"))
        self.window.draw_rectangle(gc, True, x, y, w, h)

        # vacio
        gc.set_rgb_fg_color(gtk.gdk.Color(0, 0, 0))
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        # progreso
        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(gtk.gdk.Color(65000, 26000, 0))
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # borde de progreso
        gc.set_rgb_fg_color(get_colors("drawingplayer"))
        self.window.draw_rectangle(gc, False, xx, yy, ww, hh)

        return True


class Credits(gtk.Dialog):

    __gtype_name__ = 'TubeCredits'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self, parent=parent, title="",
            buttons=("Cerrar", gtk.RESPONSE_OK))

        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_border_width(15)

        imagen = gtk.Image()
        imagen.set_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMediaTubeCredits.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class Help(gtk.Dialog):

    __gtype_name__ = 'TubeHelp'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self, parent=parent, title="",
            buttons=("Cerrar", gtk.RESPONSE_OK))

        self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
        self.set_border_width(15)

        tabla1 = gtk.Table(columns=5, rows=2, homogeneous=False)

        vbox = gtk.HBox()
        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")
        self.anterior = get_boton(archivo, flip=True, pixels=24,
            tooltip_text="Anterior")
        self.anterior.connect("clicked", self.__switch)
        self.anterior.show()
        vbox.pack_start(self.anterior, False, False, 0)

        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")
        self.siguiente = get_boton(archivo, pixels=24,
            tooltip_text="Siguiente")
        self.siguiente.connect("clicked", self.__switch)
        self.siguiente.show()
        vbox.pack_end(self.siguiente, False, False, 0)

        tabla1.attach_defaults(vbox, 0, 5, 0, 1)

        self.helps = []
        for x in range(1, 3):
            help = gtk.Image()
            help.set_from_file(os.path.join(BASE_PATH,
                "Iconos", "help-%s.svg" % x))
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


class ToolbarSalir(gtk.Toolbar):
    """
    Toolbar para confirmar salir de la aplicación.
    """

    __gtype_name__ = 'ToolbarSalir'

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("download"))

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.show_all()

    def run(self, nombre_aplicacion):
        """
        La toolbar se muestra y espera confirmación.
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
