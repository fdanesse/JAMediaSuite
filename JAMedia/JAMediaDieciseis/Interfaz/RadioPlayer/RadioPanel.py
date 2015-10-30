#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
import threading
from ..Globales import get_colors
from ..Globales import get_ip
#from ..Globales import borrar
from PlayerControls import PlayerControls
from PlayerList import PlayerList
from Reproductor.JAMediaReproductor import JAMediaReproductor


class RadioPanel(gtk.EventBox):

    __gsignals__ = {
    "playing": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(2)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        vbox = gtk.VBox()
        self.playerlist = PlayerList()
        vbox.pack_start(self.playerlist, True, True, 0)

        self.playercontrols = PlayerControls()
        vbox.pack_end(self.playercontrols, False, False)

        self.add(vbox)
        self.show_all()

        self.player = False
        self.datos = False

        self.playercontrols.volumen.connect("volumen", self.__set_volumen)
        self.playerlist.lista.connect("nueva-seleccion",
            self.__cargar_reproducir)
        self.playerlist.connect("accion", self.__accion_menu)
        self.playercontrols.connect("accion-controls", self.__accion_controls)
        self.connect("show", self.__show)
        self.connect("hide", self.__hide)
        #gobject.timeout_add(5000, self.__check_ip)

    def __show(self, widget):
        win = self.get_toplevel()
        screen = win.get_screen()
        w, h = win.get_size()
        ww, hh = (screen.get_width(), screen.get_height())
        if w == ww and h == hh:
            self.datos = ["fullscreen", w, h]
        elif w == ww and h != hh:
            self.datos = ["maximizado", w, h]
        else:
            self.datos = ["unfullscreen", w, h]
        win.unmaximize()
        win.unfullscreen()
        win.set_resizable(False)
        self.get_toplevel().set_size_request(320, 335)

    def __hide(self, widget):
        if self.datos:
            estado, w, h = self.datos
            win = self.get_toplevel()
            win.set_resizable(True)
            if estado == "fullscreen":
                win.fullscreen()
            elif estado == "maximizado":
                win.maximize()
            elif estado == "unfullscreen":
                self.get_toplevel().resize(w, h)

    def __accion_controls(self, widget, accion):
        if accion == "atras":
            self.playerlist.lista.seleccionar_anterior()
        elif accion == "siguiente":
            self.playerlist.lista.seleccionar_siguiente()
        elif accion == "stop":
            if self.player:
                self.player.stop()
        elif accion == "pausa-play":
            if self.player:
                self.player.pause_play()
        elif accion == "showlist":
            if widget.lista.get_active():
                self.playerlist.show()
                self.get_toplevel().toolbar.show()
                self.get_toplevel().set_size_request(320, 335)
            else:
                self.playerlist.hide()
                self.get_toplevel().toolbar.hide()
                x, y, w, h = self.playercontrols.get_allocation()
                self.get_toplevel().set_size_request(w, h+5)

    def __set_volumen(self, widget, valor):
        if self.player:
            self.player.set_volumen(valor)

    def __accion_menu(self, playerlist, lista, accion, _iter):
        print accion
        '''
        if lista and accion and _iter:
            uri = lista.get_model().get_value(_iter, 2)
            if accion == "Quitar" or accion == "Borrar":
                dialog = gtk.Dialog(parent=self.get_toplevel(),
                    title="Alerta",
                    buttons=("Si", gtk.RESPONSE_ACCEPT,
                    "No", gtk.RESPONSE_CANCEL))
                dialog.set_border_width(15)
                dialog.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
                texto = uri
                if len(texto) > 30:
                    texto = " . . . " + str(texto[len(texto) - 30:-1])
                label = gtk.Label("¿%s:  %s?" % (accion, texto))
                label.show()
                dialog.vbox.pack_start(label, True, True, 5)
                if dialog.run() == gtk.RESPONSE_ACCEPT:
                    self.stop()
                    path = lista.get_model().get_path(_iter)
                    path = (path[0], )
                    lista.get_model().remove(_iter)
                    self.__reselect(lista, path)
                    if accion == "Quitar":
                        pass
                    elif accion == "Borrar":
                        if os.path.isfile(uri):
                            borrar(uri)
                dialog.destroy()
            elif accion == "Subtitulos":
                dialog = gtk.FileChooserDialog(
                    title="Cargar Subtitulos", parent=self.get_toplevel(),
                    action=gtk.FILE_CHOOSER_ACTION_OPEN,
                    buttons=("Abrir", gtk.RESPONSE_ACCEPT,
                    "Salir", gtk.RESPONSE_CANCEL))
                dialog.set_border_width(15)
                dialog.modify_bg(gtk.STATE_NORMAL, get_colors("window"))
                dialog.set_current_folder_uri("file://%s" % os.path.dirname(uri))
                dialog.set_select_multiple(False)
                filtro = gtk.FileFilter()
                filtro.set_name("text")
                filtro.add_mime_type("text/*")
                dialog.add_filter(filtro)
                if dialog.run() == gtk.RESPONSE_ACCEPT:
                    self.player.player.set_property(
                        "suburi", "file://" + dialog.get_filename())
                    self.player.player.set_property(
                        "subtitle-font-desc", "sans bold 18")
                dialog.destroy()
        '''
    def __reselect(self, lista, path):
        try:
            if path[0] > -1:
                lista.get_selection().select_iter(
                    lista.get_model().get_iter(path))
            else:
                lista.seleccionar_primero()
        except:
            lista.seleccionar_primero()

    def __cargar_reproducir(self, widget, uri):
        widget.set_sensitive(False)
        volumen = 1.0
        if self.player:
            volumen = float("{:.1f}".format(
                self.playercontrols.volumen.get_value() * 10))
        self.stop()

        if get_ip():
            xid = "" #self.visor.get_property('window').xid
            self.player = JAMediaReproductor()

            self.player.connect("endfile", self.__endfile)
            self.player.connect("estado", self.__state_changed)

            self.player.load(uri, xid)
            thread = threading.Thread(target=self.player.play)
            thread.start()
            self.player.set_volumen(volumen)
            self.playercontrols.volumen.set_value(volumen / 10)
        else:
            print "No hay conexión a Internet"
        widget.set_sensitive(True)

    def __endfile(self, widget=None, senial=None):
        self.playercontrols.set_paused()
        self.playerlist.lista.seleccionar_siguiente()

    def __state_changed(self, widget=None, valor=None):
        if "playing" in valor:
            self.playercontrols.set_playing()
            self.emit("playing")
        elif "paused" in valor or "None" in valor:
            self.playercontrols.set_paused()
        else:
            print "Estado del Reproductor desconocido:", valor
        self.playercontrols.set_sensitive(True)

    def __user_set_progress(self, widget, valor):
        if self.player:
            self.player.set_position(valor)

    def stop(self):
        if self.player:
            self.player.disconnect_by_func(self.__endfile)
            self.player.disconnect_by_func(self.__state_changed)
            self.player.stop()
            del(self.player)
            self.player = False
        self.playercontrols.set_paused()
        self.playercontrols.set_sensitive(False)
