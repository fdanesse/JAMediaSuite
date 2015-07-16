#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import os
import gtk
import gobject
import webkit
from ..Globales import get_colors
#from ..Globales import borrar
#from PlayerControls import PlayerControls
from PlayerList import PlayerList


class TvPanel(gtk.HPaned):

    __gsignals__ = {
    "playing": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.HPaned.__init__(self)

        self.set_border_width(2)
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        self.navegador = Navegador()
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(self.navegador)

        self.pack1(scroll, resize=True, shrink=True)

        self.playerlist = PlayerList()
        self.pack2(self.playerlist, resize=False, shrink=False)

        self.show_all()

        self.playerlist.lista.connect("nueva-seleccion",
            self.__cargar_reproducir)
        self.playerlist.connect("accion", self.__accion_menu)

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
                dialog.set_current_folder_uri(
                    "file://%s" % os.path.dirname(uri))
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
        if not uri:
            uri = ""
        widget.set_sensitive(False)
        self.stop()
        #self.navegador.load_uri(uri)
        self.navegador.open(uri)
        widget.set_sensitive(True)

    '''
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
    '''

    def stop(self):
        pass


class Navegador(webkit.WebView):

    def __init__(self):

        webkit.WebView.__init__(self)
        self.set_zoom_level(1.0)
        self.settings = self.get_settings()
        self.settings.set_property("enable-plugins", True)
        self.settings.set_property("enable-scripts", True)
        self.settings.set_property("auto-load-images", True)
        self.settings.set_property("enable-webgl", True)
        self.settings.set_property("enable-media-stream", True)
        self.settings.set_property("enable-webaudio", True)
        self.settings.set_property("enable-mediasource", True)
        self.settings.set_property("enable-html5-database", True)
        self.settings.set_property("enable-html5-local-storage", True)
        self.settings.set_property("enable-java-applet", True)
        self.settings.set_property("enable-running-of-insecure-content", True)
        self.settings.set_property("enable-display-of-insecure-content", True)
        self.settings.set_property("enable-developer-extras", True)
        self.settings.set_property("enable-private-browsing", True)
        self.settings.set_property("enable-caret-browsing", True)
        self.settings.set_property("enable-xss-auditor", True)
        self.settings.set_property(
            "javascript-can-open-windows-automatically", True)
        self.settings.set_property("javascript-can-access-clipboard", True)
        self.settings.set_property(
            "enable-offline-web-application-cache", True)
        self.settings.set_property(
            "enable-universal-access-from-file-uris", True)
        self.settings.set_property("enable-file-access-from-file-uris", True)
        print "OK", self.settings.get_property('user-agent')
        #self.settings.set_property('user-agent', '')
        self.set_settings(self.settings)
        self.show_all()

        #self.connect("title-changed", self.__title_changed)
        #self.connect("load-started", self.__load_started)
        #self.connect("load-error", self.__load_error)

    def __load_started(self, widget, frame):
        print "Load:", frame

    def __load_error(self, widget, x, y, z):
        print self.__load_error, x, y, z

    def __title_changed(self, widget, frame, title):
        print "Titulo", title
