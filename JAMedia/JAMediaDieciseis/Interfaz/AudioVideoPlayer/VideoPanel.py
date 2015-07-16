#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
import threading
from ..Globales import get_colors
from ..Globales import borrar
from PlayerControls import PlayerControls
from PlayerList import PlayerList
from Reproductor.JAMediaReproductor import JAMediaReproductor


class VideoPanel(gtk.HPaned):

    __gsignals__ = {
    "playing": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.set_border_width(2)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        vbox = gtk.VBox()
        self.visor = VideoVisor()
        self.progress = ProgressPlayer()
        self.playercontrols = PlayerControls()

        vbox.pack_start(self.visor, True, True, 0)
        vbox.pack_start(self.progress, False, False, 0)
        vbox.pack_start(self.playercontrols, False, False, 0)

        self.pack1(vbox, resize=True, shrink=True)

        self.playerlist = PlayerList()
        self.pack2(self.playerlist, resize=False, shrink=False)

        self.show_all()

        self.player = False

        self.visor.connect("ocultar_controles", self.__ocultar_controles)
        self.progress.connect("user-set-value", self.__user_set_progress)
        self.playercontrols.volumen.connect("volumen", self.__set_volumen)
        self.playerlist.lista.connect("nueva-seleccion",
            self.__cargar_reproducir)
        self.playerlist.connect("accion", self.__accion_menu)
        self.playercontrols.connect("accion-controls", self.__accion_controls)
        self.playerlist.balance.connect("balance-valor", self.__accion_balance)

    def __ocultar_controles(self, widget, valor):
        if valor:
            self.set_border_width(0)
            self.get_toplevel().set_border_width(0)
            self.get_toplevel().toolbar.hide()
            self.progress.hide()
            self.playercontrols.hide()
            self.playerlist.hide()
        else:
            self.get_toplevel().set_border_width(2)
            self.set_border_width(2)
            self.get_toplevel().toolbar.show()
            self.progress.show()
            self.playercontrols.show()
            self.playerlist.show()

    def __update_balance(self):
        config = {}
        if self.player:
            config = self.player.get_balance()
        self.playerlist.balance.set_balance(
            brillo=config.get('brillo', 50.0),
            contraste=config.get('contraste', 50.0),
            saturacion=config.get('saturacion', 50.0),
            hue=config.get('hue', 50.0),
            gamma=config.get('gamma', 10.0))
        return False

    def __accion_balance(self, widget, valor, prop):
        if prop == "saturacion":
            self.player.set_balance(saturacion=valor)
        elif prop == "contraste":
            self.player.set_balance(contraste=valor)
        elif prop == "brillo":
            self.player.set_balance(brillo=valor)
        elif prop == "hue":
            self.player.set_balance(hue=valor)
        elif prop == "gamma":
            self.player.set_balance(gamma=valor)

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
        elif accion == "Izquierda" or accion == "Derecha":
            if self.player:
                self.player.rotar(accion)
        elif accion == "showlist":
            if widget.lista.get_active():
                self.playerlist.show()
            else:
                self.playerlist.hide()
        elif accion == "showcontrols":
            if widget.controls.get_active():
                self.visor.set_activo(False)
            else:
                self.visor.set_activo(True)

    def __set_volumen(self, widget, valor):
        if self.player:
            self.player.set_volumen(valor)

    def __accion_menu(self, playerlist, lista, accion, _iter):
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

        xid = self.visor.get_property('window').xid
        self.player = JAMediaReproductor()

        self.player.connect("endfile", self.__endfile)
        self.player.connect("estado", self.__state_changed)
        self.player.connect("newposicion", self.progress.update_progress)
        self.player.connect("video", self.playerlist.set_video)
        self.player.connect("video", self.playercontrols.set_video)

        self.player.load(uri, xid)
        thread = threading.Thread(target=self.player.play)
        thread.start()
        self.player.set_volumen(volumen)
        self.playercontrols.volumen.set_value(volumen / 10)
        widget.set_sensitive(True)

    def __endfile(self, widget=None, senial=None):
        self.playercontrols.set_paused()
        self.playerlist.lista.seleccionar_siguiente()

    def __state_changed(self, widget=None, valor=None):
        if "playing" in valor:
            self.playercontrols.set_playing()
            self.emit("playing")
            gobject.idle_add(self.__update_balance)
        elif "paused" in valor or "None" in valor:
            self.playercontrols.set_paused()
            gobject.idle_add(self.__update_balance)
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
            self.player.disconnect_by_func(self.progress.update_progress)
            self.player.disconnect_by_func(self.playerlist.set_video)
            self.player.disconnect_by_func(self.playercontrols.set_video)
            self.player.stop()
            del(self.player)
            self.player = False
        self.progress.update_progress(None, 0.0)
        self.playerlist.set_video(False, False)
        self.playercontrols.set_video(False, False)
        self.playercontrols.set_paused()
        self.playercontrols.set_sensitive(False)
        self.visor.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))


class VideoVisor(gtk.DrawingArea):

    __gsignals__ = {
    "ocultar_controles": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,))}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.add_events(
            gtk.gdk.KEY_PRESS_MASK |
            gtk.gdk.KEY_RELEASE_MASK |
            gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.POINTER_MOTION_HINT_MASK |
            gtk.gdk.BUTTON_MOTION_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK
        )

        self._activo = False
        self.show_all()

    def do_motion_notify_event(self, event):
        if self._activo:
            x, y = (int(event.x), int(event.y))
            rect = self.get_allocation()
            xx, yy, ww, hh = (rect.x, rect.y, rect.width, rect.height)

            if x in range(ww - 60, ww) or y in range(yy, yy + 60) \
                or y in range(hh - 60, hh):
                self.emit("ocultar_controles", False)
                return True
            else:
                self.emit("ocultar_controles", True)
                return True

    def set_activo(self, valor):
        self._activo = valor
        self.emit("ocultar_controles", self._activo)


class ProgressPlayer(gtk.HScale):

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.HScale.__init__(self)

        self.set_property("adjustment",
            gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))
        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        self.set_digits(0)
        self.set_draw_value(False)
        self.presed = False

        self.connect("button-press-event", self.__button_press_event)
        self.connect("button-release-event", self.__button_release_event)
        self.connect("motion-notify-event", self.__motion_notify_event)

        self.show_all()

    def __button_press_event(self, widget, event):
        self.presed = True

    def __button_release_event(self, widget, event):
        self.presed = False

    def __motion_notify_event(self, widget, event):
        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:
            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)
            if valor >= 0.0 and valor <= 100.0:
                self.set_value(valor)
                self.emit("user-set-value", valor)

    def update_progress(self, objetoemisor, valor):
        self.set_value(float(valor))
