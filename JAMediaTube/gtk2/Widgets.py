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

import gtk
from gtk import gdk
from gtk.gdk import Pixbuf
import gobject

'''
import JAMediaObjects
from JAMediaObjects.JAMediaWidgets import JAMediaButton

from JAMedia.JAMedia import JAMediaPlayer
'''
from Globales import get_separador
from Globales import get_boton
#from Globales import get_color

BASE_PATH = os.path.dirname(__file__)

'''
class Tube_Player(JAMediaPlayer):
    """
    JAMedia con pequeñas adaptaciones.
    """

    def __init__(self):

        JAMediaPlayer.__init__(self)

        self.show_all()

    def confirmar_salir(self, widget=None, senial=None):
        """
        Salteandose confirmación para salir
        y maneteniendose activa la reproducción y
        grabación de JAMedia.
        """

        map(self.__ocultar, [self.toolbaraddstream])

        self.emit('salir')

    def __ocultar(self, objeto):

        if objeto.get_visible():
            objeto.hide()
'''

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

        self.modify_bg(0, gdk.color_parse("#000000"))

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "JAMediaTube.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Autor")
        #boton.connect("clicked", self.__show_credits)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "JAMedia.svg")
        self.jamedia = get_boton(archivo, flip=False,
            pixels=24)
        self.jamedia.set_tooltip_text("Cambiar a JAMedia")
        #self.jamedia.connect("clicked", self.__emit_switch)
        self.insert(self.jamedia, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "JAMedia-help.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Ayuda")
        #boton.connect("clicked", self.__show_help)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "salir.svg")
        boton = get_boton(archivo, flip=False,
            pixels=24)
        boton.set_tooltip_text("Salir")
        #boton.connect("clicked", self.__salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

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
        """
        Cuando se hace click en el boton salir.
        """

        self.emit('salir')

'''
class Toolbar_Videos_Izquierda(gtk.Toolbar):
    """
    toolbar inferior izquierda para videos encontrados.
    """

    __gsignals__ = {
    "borrar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "mover_videos": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Borrar Lista.")
        boton.connect("clicked", self.__emit_borrar)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Enviar a Descargas.")
        boton.connect("clicked", self.__emit_adescargas)
        self.insert(boton, -1)

        self.show_all()

    def __emit_adescargas(self, widget):
        """
        Para pasar los videos encontrados a la
        lista de descargas.
        """

        self.emit('mover_videos')

    def __emit_borrar(self, widget):
        """
        Para borrar todos los videos de la lista.
        """

        self.emit('borrar')


class Toolbar_Videos_Derecha(gtk.Toolbar):
    """
    toolbar inferior derecha para videos en descarga.
    """

    __gsignals__ = {
    "borrar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "mover_videos": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'comenzar_descarga': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=True,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Quitar de Descargas.")
        boton.connect("clicked", self.__emit_aencontrados)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Borrar Lista.")
        boton.connect("clicked", self.__emit_borrar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8),
            rotacion=GdkPixbuf.PixbufRotation.CLOCKWISE)
        boton.set_tooltip_text("Descargar.")
        boton.connect("clicked", self.__emit_comenzar_descarga)
        self.insert(boton, -1)

        self.show_all()

    def __emit_comenzar_descarga(self, widget):
        """
        Emite la señal para comenzar a descargar
        los videos en la lista de descargas.
        """

        self.emit('comenzar_descarga')

    def __emit_aencontrados(self, widget):
        """
        Para pasar los videos en descarga a la
        lista de encontrados.
        """

        self.emit('mover_videos')

    def __emit_borrar(self, widget):
        """
        Para borrar todos los videos de la lista.
        """

        self.emit('borrar')


class Mini_Toolbar(gtk.Toolbar):
    """
    Mini toolbars Superior izquierda y derecha.
    """

    __gsignals__ = {
    "guardar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "abrir": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "menu_activo": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self, text):

        gtk.Toolbar.__init__(self)

        self.label = None
        self.texto = text
        self.numero = 0

        item = gtk.ToolItem()
        self.label = gtk.Label("%s: %s" % (text, self.numero))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Lista de Búsquedas.")
        boton.connect("clicked", self.__get_menu)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8),
            rotacion=GdkPixbuf.PixbufRotation.CLOCKWISE)
        boton.set_tooltip_text("Guardar Lista.")
        boton.connect("clicked", self.__emit_guardar)
        self.insert(boton, -1)

        self.show_all()

    def __emit_guardar(self, widget):
        """
        Emite guardar, para que se guarden todos
        los videos en un archivo shelve.
        """

        self.emit('guardar')

    def __emit_abrir(self, key):
        """
        Emite abrir, para que se carguen todos
        los videos desde un archivo shelve.
        """

        self.emit('abrir', key)

    def __get_menu(self, widget):
        """
        El menu con las listas de videos
        almacenadas en archivos shelve.
        """

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        keys = dict_tube.keys()

        dict_tube.close()

        if keys:
            self.emit("menu_activo")

            menu = gtk.Menu()

            administrar = gtk.MenuItem('Administrar')
            administrar.connect_object("activate", self.__administrar, None)
            cargar = gtk.MenuItem('Cargar')

            menu.append(administrar)
            menu.append(cargar)

            menu_listas = gtk.Menu()

            cargar.set_submenu(menu_listas)

            for key in keys:
                item = gtk.MenuItem(key)
                menu_listas.append(item)
                item.connect_object("activate", self.__emit_abrir, key)

            menu.show_all()
            menu.attach_to_widget(widget, self.__null)
            menu.popup(None, None, None, None, 1, 0)

    def __administrar(self, widget):

        dialogo = TubeListDialog(parent=self.get_toplevel())
        dialogo.run()
        dialogo.destroy()

    def __null(self):
        pass

    def set_info(self, valor):
        """
        Recibe un entero y actualiza la información.
        """

        if valor != self.numero:
            self.numero = valor
            text = "%s: %s" % (self.texto, str(self.numero))
            self.label.set_text(text)


class Toolbar_Busqueda(gtk.Toolbar):
    """
    Toolbar con widgets de busqueda.
    """

    __gsignals__ = {
    "comenzar_busqueda": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        item = gtk.ToolItem()
        label = gtk.Label("Buscar por: ")
        label.show()
        item.add(label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.entrytext = gtk.Entry()
        self.entrytext.set_size_request(400, -1)
        self.entrytext.set_max_length(50)
        self.entrytext.set_tooltip_text("Escribe lo que Buscas.")
        self.entrytext.show()
        self.entrytext.connect('activate', self.__activate_entrytext)
        item.add(self.entrytext)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8),
            rotacion=GdkPixbuf.PixbufRotation.CLOCKWISE)
        boton.set_tooltip_text("Comenzar Búsqueda")
        boton.connect("clicked", self.__emit_buscar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

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

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(BASE_PATH,
            "Iconos", "yt_videos_black.png")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        self.label = gtk.Label("")
        self.label.set_justify(gtk.Justification.LEFT)
        #self.label.set_line_wrap(True)
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.show_all()


class WidgetVideoItem(JAMediaButton):

    def __init__(self, videodict):

        JAMediaButton.__init__(self)

        self.set_border_width(2)

        self.videodict = videodict

        self.imagen.destroy()

        hbox = gtk.Box(orientation=gtk.Orientation.HORIZONTAL)
        vbox = gtk.Box(orientation=gtk.Orientation.VERTICAL)

        keys = self.videodict.keys()

        if "previews" in keys:
            imagen = gtk.Image()
            hbox.pack_start(imagen, False, False, 3)

            if type(self.videodict["previews"]) == list:
                # FIXME: siempre hay 4 previews.
                url = self.videodict["previews"][0][0]
                import time
                archivo = "/dev/shm/preview%d" % time.time()

                try:
                    # FIXME: Porque Falla si no hay Conexión.
                    import urllib
                    fileimage, headers = urllib.urlretrieve(url, archivo)
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
                        fileimage, 200, 150)
                    imagen.set_from_pixbuf(pixbuf)

                    ### Convertir imagen a string por si se quiere guardar.
                    import base64
                    pixbuf_file = open(fileimage, 'rb')
                    image_string = base64.b64encode(pixbuf_file.read())
                    pixbuf_file.close()
                    self.videodict["previews"] = image_string

                except:
                    print "No hay Conexión a Internet."

                os.remove(archivo)

            else:
                import base64
                loader = GdkPixbuf.PixbufLoader()
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

    def button_press(self, widget, event):

        self.modify_bg(0, self.colorclicked)

        if event.button == 1:
            self.emit("clicked", event)

        elif event.button == 3:
            self.emit("click_derecho", event)


class ToolbarAccionListasVideos(gtk.Toolbar):
    """
    Toolbar para que el usuario confirme "borrar"
    lista de video de JAMediaTube.
    """

    __gsignals__ = {
    "ok": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.objetos = None

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
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
            "Iconos", "acercar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__realizar_accion)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def __realizar_accion(self, widget):
        """
        Confirma borrar.
        """

        objetos = self.objetos
        self.cancelar()

        gobject.idle_add(self.__emit_ok, objetos)

    def __emit_ok(self, objetos):

        self.emit('ok', objetos)

    def set_accion(self, objetos):
        """
        Configura borrar.
        """

        self.objetos = objetos
        self.label.set_text("¿Eliminar?")
        self.show_all()

    def cancelar(self, widget=None):
        """
        Cancela borrar.
        """

        self.objetos = None
        self.label.set_text("")
        self.hide()


class Toolbar_Descarga(gtk.Box):

    __gsignals__ = {
    'end': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Box.__init__(self, orientation=gtk.Orientation.VERTICAL)

        self.toolbar = gtk.Toolbar()

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

        self.toolbar.insert(
            get_separador(draw=False,
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
        #archivo = os.path.join(BASE_PATH,
        #    "Iconos","stop.png")
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

        self.jamediayoutube.connect(
            "progress_download",
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

        self.actualizador = gobject.timeout_add(
            1000, self.__handle)

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

        # No funciona correctamente, la descarga continúa.
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

        self.escala = ProgressBar(
            gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0

        self.add(self.escala)
        self.show_all()

        self.set_size_request(-1, get_pixels(1.2))
        self.set_progress(0)

    def set_progress(self, valor=0):
        """
        El reproductor modifica la escala.
        """

        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()


class ProgressBar(gtk.Scale):
    """
    Escala de Progreso_Descarga.
    """

    def __init__(self, ajuste):

        gtk.Scale.__init__(self, orientation=gtk.Orientation.HORIZONTAL)

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.borde = get_pixels(0.5)

        self.show_all()

    def do_draw(self, contexto):
        """
        Dibuja el estado de la barra de progreso.
        """

        rect = self.get_allocation()
        w, h = (rect.width, rect.height)

        # Fondo
        #Gdk.cairo_set_source_color(contexto, G.BLANCO)
        #contexto.paint()

        # Relleno de la barra
        ww = w - self.borde * 2
        hh = h - self.borde * 2
        Gdk.cairo_set_source_color(contexto, get_color("NEGRO"))
        rect = Gdk.Rectangle()
        rect.x, rect.y, rect.width, rect.height = (
            self.borde, self.borde, ww, hh)
        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()

        # Relleno de la barra segun progreso
        Gdk.cairo_set_source_color(contexto, get_color("NARANJA"))
        rect = Gdk.Rectangle()

        ximage = int(self.ajuste.get_value() * ww / 100)
        rect.x, rect.y, rect.width, rect.height = (self.borde, self.borde,
            ximage, hh)

        Gdk.cairo_rectangle(contexto, rect)
        contexto.fill()

        return True


class Toolbar_Guardar(gtk.Toolbar):
    """
    Toolbar con widgets para guardar una lista de videos.
    """

    __gsignals__ = {
    "ok": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        item = gtk.ToolItem()
        label = gtk.Label("Nombre: ")
        label.show()
        item.add(label)
        self.insert(item, -1)

        item = gtk.ToolItem()
        self.entrytext = gtk.Entry()
        self.entrytext.set_size_request(20, -1)
        self.entrytext.set_max_length(10)
        self.entrytext.set_tooltip_text("Nombre de Archivo.")
        self.entrytext.show()
        self.entrytext.connect('activate', self.__emit_ok)
        item.add(self.entrytext)
        self.insert(item, -1)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "acercar.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_ok)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def __emit_ok(self, widget):

        texto = self.entrytext.get_text()
        self.cancelar()

        if texto:
            self.emit("ok", texto)

    def cancelar(self, widget=None):

        self.entrytext.set_text("")
        self.hide()


class Credits(gtk.Dialog):

    __gtype_name__ = 'TubeCredits'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            flags=gtk.DialogFlags.MODAL,
            buttons=["Cerrar", gtk.ResponseType.ACCEPT])

        self.set_border_width(15)

        imagen = gtk.Image()
        imagen.set_from_file(
            os.path.join(BASE_PATH,
                "Iconos", "JAMediaTubeCredits.svg"))

        self.vbox.pack_start(imagen, True, True, 0)
        self.vbox.show_all()


class Help(gtk.Dialog):

    __gtype_name__ = 'TubeHelp'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            flags=gtk.DialogFlags.MODAL,
            buttons=["Cerrar", gtk.ResponseType.ACCEPT])

        self.set_border_width(15)

        tabla1 = gtk.Table(columns=5, rows=2, homogeneous=False)

        vbox = gtk.HBox()
        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.anterior = get_boton(
            archivo, flip=True,
            pixels=get_pixels(0.8),
            tooltip_text="Anterior")
        self.anterior.connect("clicked", self.__switch)
        self.anterior.show()
        vbox.pack_start(self.anterior, False, False, 0)

        archivo = os.path.join(BASE_PATH,
            "Iconos", "play.svg")
        self.siguiente = get_boton(
            archivo,
            pixels=get_pixels(0.8),
            tooltip_text="Siguiente")
        self.siguiente.connect("clicked", self.__switch)
        self.siguiente.show()
        vbox.pack_end(self.siguiente, False, False, 0)

        tabla1.attach_defaults(vbox, 0, 5, 0, 1)

        self.helps = []

        for x in range(1, 3):
            help = gtk.Image()
            help.set_from_file(
                os.path.join(BASE_PATH,
                    "Iconos", "JAMediaTube-help%s.png" % x))
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


class TubeListDialog(gtk.Dialog):

    __gtype_name__ = 'TubeListDialog'

    def __init__(self, parent=None):

        gtk.Dialog.__init__(self,
            parent=parent,
            flags=gtk.DialogFlags.MODAL,
            buttons=["Cerrar", gtk.ResponseType.ACCEPT])

        self.set_border_width(15)
        rect = parent.get_allocation()
        self.set_size_request(rect.width - 15, rect.height - 25)

        self.actualizando = False

        self.panel = gtk.Paned(orientation=gtk.Orientation.HORIZONTAL)

        from JAMediaObjects.JAMediaWidgets import Lista

        self.listas = Lista()
        self.videos = gtk.Box(orientation=gtk.Orientation.VERTICAL)

        scroll = self.__get_scroll()
        scroll.set_policy(
            gtk.PolicyType.NEVER,
            gtk.PolicyType.AUTOMATIC)
        scroll.add_with_viewport(self.listas)
        self.panel.pack1(scroll, resize=False, shrink=True)

        scroll = self.__get_scroll()
        scroll.add_with_viewport(self.videos)
        self.panel.pack2(scroll, resize=True, shrink=False)

        self.label = gtk.Label("")
        self.vbox.pack_start(self.label, False, False, 0)
        self.vbox.pack_start(self.panel, True, True, 0)
        self.vbox.show_all()

        self.listas.connect("nueva-seleccion", self.__select_list)
        self.listas.connect("button-press-event",
            self.__click_derecho_en_lista)
        self.connect("realize", self.__do_realize)

    def __click_derecho_en_lista(self, widget, event):
        """
        Esto es para abrir un menu de opciones cuando
        el usuario hace click derecho sobre un elemento en
        la lista.
        """

        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)

        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(
                int(pos[0]), int(pos[1]))

        except:
            return

        if boton == 1:
            return

        elif boton == 3:
            menu = gtk.Menu()
            borrar = gtk.MenuItem("Eliminar")
            menu.append(borrar)

            borrar.connect_object(
                "activate", self.__eliminar,
                widget, path)

            menu.show_all()
            menu.attach_to_widget(widget, self.__null)

            menu.popup(None, None, None, None, boton, tiempo)

        elif boton == 2:
            return

    def __null(self):
        pass

    def __eliminar(self, widget, path):
        """
        Elimina una lista del archivo shelve.
        """

        if self.actualizando:
            return

        for child in self.videos.get_children():
            self.videos.remove(child)
            child.destroy()

        new_box = gtk.Box(orientation=gtk.Orientation.VERTICAL)
        new_box.show_all()
        self.videos.pack_start(
            new_box,
            True, True, 0)

        iter = widget.get_model().get_iter(path)
        key = widget.get_model().get_value(iter, 2)

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        del(dict_tube[key])

        keys = dict_tube.keys()

        dict_tube.close()

        widget.get_model().remove(iter)

        if not keys:
            dialog = gtk.Dialog(
                parent=self.get_toplevel(),
                flags=gtk.DialogFlags.MODAL,
                buttons=["OK", gtk.ResponseType.ACCEPT])

            dialog.set_border_width(15)

            label = gtk.Label("Todas las Listas han sido Eliminadas.")
            dialog.vbox.pack_start(label, True, True, 0)
            dialog.vbox.show_all()

            dialog.run()

            dialog.destroy()

            self.destroy()

    def __select_list(self, widget, valor):
        """
        Cuando se selecciona una lista, se cargan
        los videos que contiene en self.videos.
        """

        self.actualizando = True

        self.panel.set_sensitive(False)

        for child in self.videos.get_children():
            self.videos.remove(child)
            child.destroy()

        new_box = gtk.Box(orientation=gtk.Orientation.VERTICAL)
        new_box.show_all()
        self.videos.pack_start(
            new_box,
            True, True, 0)

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        videos = []
        for item in dict_tube[valor].keys():
            videos.append(dict_tube[valor][item])

        dict_tube.close()

        gobject.idle_add(self.__add_videos, videos)

    def __add_videos(self, videos):
        """
        Se crean los video_widgets de videos y
        se agregan al panel, segun destino.
        """

        if not videos:
            self.label.set_text("%s Videos Listados." % len(
                self.videos.get_children()[0].get_children()))
            self.panel.set_sensitive(True)
            self.actualizando = False
            return False

        self.label.set_text("Listando Videos . . .  Quedan %s" % len(videos))

        video = videos[0]

        videowidget = WidgetVideoItem(video)
        videowidget.connect("click_derecho", self.__clicked_videowidget)
        """
        text = TipEncontrados

        if destino == self.paneltube.encontrados:
            text = TipEncontrados

        elif destino == self.paneltube.descargar:
            text = TipDescargas

        videowidget.set_tooltip_text(text)"""
        videowidget.show_all()
        """
        videowidget.drag_source_set(
            Gdk.ModifierType.BUTTON1_MASK,
            target,
            Gdk.DragAction.MOVE)"""

        videos.remove(video)

        try:
            self.videos.get_children()[0].pack_start(
                videowidget, False, False, 1)

        except:
            return False

        gobject.idle_add(self.__add_videos, videos)

    def __clicked_videowidget(self, widget, event):
        """
        Cuando se hace click derecho sobre un video item.
        """

        boton = event.button
        #pos = (event.x, event.y)
        tiempo = event.time

        menu = gtk.Menu()
        borrar = gtk.MenuItem("Eliminar")
        menu.append(borrar)

        borrar.connect_object(
            "activate", self.__eliminar_video,
            widget)

        menu.show_all()
        menu.attach_to_widget(widget, self.__null)

        menu.popup(None, None, None, None, boton, tiempo)

    def __eliminar_video(self, widget):

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        if len(dict_tube[self.listas.valor_select].keys()) == 1:
            modelo, iter = self.listas.treeselection.get_selected()
            path = modelo.get_path(iter)
            self.__eliminar(self.listas, path)

        else:
            videos = {}
            for id in dict_tube[self.listas.valor_select].keys():
                if id != widget.videodict["id"]:
                    videos[id] = dict_tube[self.listas.valor_select][id]

            dict_tube[self.listas.valor_select] = videos

            widget.destroy()
            self.label.set_text("%s Videos Listados." % len(
                self.videos.get_children()[0].get_children()))

        dict_tube.close()

    def __do_realize(self, widget):
        """
        Carga la lista de Albums de Descargas en self.listas.
        """

        from Globales import get_data_directory
        import shelve

        dict_tube = shelve.open(
            os.path.join(get_data_directory(),
            "List.tube"))

        keys = dict_tube.keys()

        dict_tube.close()

        lista = []
        for key in keys:
            lista.append([key, key])

        self.listas.agregar_items(lista)

    def __get_scroll(self):

        scroll = gtk.ScrolledWindow()

        scroll.set_policy(
            gtk.PolicyType.AUTOMATIC,
            gtk.PolicyType.AUTOMATIC)

        return scroll
'''
