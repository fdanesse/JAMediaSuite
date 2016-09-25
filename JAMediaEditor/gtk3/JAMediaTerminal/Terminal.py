#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTerminal.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay

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
import mimetypes
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import Vte
from gi.repository import Pango

from Widgets import ToolbarTerminal
from Widgets import DialogoFormato
from Globales import get_boton

BASE_PATH = os.path.dirname(__file__)
Width_Button = 18


class Terminal(Gtk.EventBox):
    """
    Terminal (NoteBook + Vtes) + Toolbar.
    """

    __gtype_name__ = 'JAMediaTerminal'

    __gsignals__ = {
    "ejecucion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
    "reset": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_PYOBJECT, GObject.TYPE_INT))}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        vbox = Gtk.VBox()

        self.notebook = NoteBookTerminal()
        self.toolbar = ToolbarTerminal()

        vbox.pack_start(self.notebook, True, True, 0)
        vbox.pack_start(self.toolbar, False, False, 0)

        self.add(vbox)
        self.show_all()

        self.toolbar.connect('accion', self.__accion_terminal)
        self.toolbar.connect('reset', self.__reset_terminal)
        self.toolbar.connect('formato', self.__set_formato)

        self.notebook.agregar_terminal()
        self.notebook.connect("reset", self.__re_emit_reset)

    def __set_formato(self, widget):
        """
        Abre el Diálogo de Formato y Setea el tipo y tamaño de
        fuentes en las terminales según selección del usuario.
        """
        string = self.notebook.fuente.to_string()
        tamanio = int(string.split(" ")[-1])
        fuente = string.replace("%s" % tamanio, "").strip()
        dialogo = DialogoFormato(parent_window=self.get_toplevel(),
            fuente=fuente, tamanio=tamanio)
        self.get_toplevel().set_sensitive(False)
        respuesta = dialogo.run()
        font = ""
        if respuesta == Gtk.ResponseType.ACCEPT:
            font = "%s %s" % dialogo.get_font()
        dialogo.destroy()
        self.get_toplevel().set_sensitive(True)
        if font:
            self.notebook.set_font(font)

    def __re_emit_reset(self, notebook, terminal, pag_indice):
        """
        Cuando se resetea una terminal, se emite la señal reset con:
            1- Notebook contenedor de terminales.
            2- Terminal reseteada.
            3- Indice de la página que le corresponde en el notebook.
            4- Botón cerrar de la lengueta específica.
            5- Etiqueta de la lengüeta específica.
        """
        self.emit("reset", notebook, terminal, pag_indice)

    def __reset_terminal(self, widget, interprete):
        """
        Resetea la terminal en interprete según valor.
        """
        self.notebook.reset_terminal(interprete=interprete)

    def __accion_terminal(self, widget, accion):
        """
        Soporte para clipboard.
        """
        self.notebook.accion_terminal(accion)

    def ejecutar(self, archivo):
        """
        Ejecuta un archivo en una nueva terminal.
        """
        if os.path.exists(archivo):
            path = os.path.basename(archivo)
            terminal = self.notebook.agregar_terminal(
                path=path, interprete='/bin/bash', ejecutar=archivo)
            self.emit("ejecucion", terminal)

    def ejecute_script(self, dirpath, interprete, path_script, param):
        """
        Ejecuta un script con parámetros, en la terminal activa
        Por ejemplo:
            python setup.py sdist

            dirpath     =   directorio base donde se encuentra setup.py
            interprete  =   python en este caso
            path_script =   dirpath + 'setup.py'
            param       =   'sdist' en est caso
        """
        terminal = self.notebook.get_children()[
            self.notebook.get_current_page()].get_child()
        pty_flags = Vte.PtyFlags(0)
        # FIXME: en versiones nuevas es spawn_sync
        try:
            self.fork_command_full(pty_flags, dirpath,
                (interprete, path_script, param), "", 0, None, None)
        except:
            self.spawn_sync(pty_flags, dirpath,
                (interprete, path_script, param), "", 0, None, None)
            

class NoteBookTerminal(Gtk.Notebook):
    """
    Notebook Contenedor de Terminales.
    """

    __gtype_name__ = 'NoteBookTerminal'

    __gsignals__ = {
    "reset": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_INT))}

    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.set_scrollable(True)
        self.fuente = Pango.FontDescription("Monospace %s" % 10)
        self.show_all()
        self.connect('switch_page', self.__switch_page)

    def __re_emit_reset(self, terminal):
        """
        Cuando se resetea una terminal.
        """
        paginas = self.get_n_pages()
        for pag_indice in range(paginas):
            if terminal == self.get_nth_page(pag_indice):
                break
        self.emit("reset", terminal, pag_indice)

    def __switch_page(self, widget, widget_child, indice):
        """
        Cuando el usuario selecciona una lengüeta en el notebook.
        """
        widget_child.child_focus(True)

    def __cerrar(self, widget):
        """
        Cerrar la terminal a través de su botón cerrar.
        """
        paginas = self.get_n_pages()
        for indice in range(paginas):
            boton = self.get_tab_label(self.get_children()[
                indice]).get_children()[1]
            if boton == widget:
                self.remove_page(indice)
                break

    def set_font(self, fuente):
        """
        Setea la fuente en las terminales.
        """
        self.fuente = Pango.FontDescription(fuente)
        paginas = self.get_children()
        if not paginas:
            return
        for pagina in paginas:
            pagina.get_child().re_set_font(self.fuente)

    def do_page_removed(self, scroll, num):
        paginas = self.get_children()
        if not paginas:
            self.agregar_terminal()

    def agregar_terminal(self, path=os.environ["HOME"],
        interprete="/bin/bash", ejecutar=None):
        """
        Agrega una nueva Terminal al Notebook.
        """
        ### Label.
        hbox = Gtk.HBox()
        archivo = os.path.join(BASE_PATH, "Iconos", "button-cancel.svg")
        boton = get_boton(archivo,
            pixels=Width_Button, tooltip_text="Cerrar")

        text = "bash"
        if "bash" in interprete:
            text = "bash"
        elif "python" in interprete:
            text = "python"
        if "ipython" in interprete:
            text = "ipython"

        label = Gtk.Label(text)
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(boton, False, False, 0)

        ### Area de Trabajo.
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        terminal = VTETerminal(path=path, interprete=interprete,
            archivo=ejecutar, fuente=self.fuente)
        scroll.add(terminal)
        self.append_page(scroll, hbox)

        label.show()
        self.show_all()

        boton.connect("clicked", self.__cerrar)
        terminal.connect("reset", self.__re_emit_reset)

        self.set_current_page(-1)
        return terminal

    def reset_terminal(self, path=os.environ["HOME"],
        interprete="/bin/bash"):
        """
        Resetea la terminal activa, a un determinado interprete.
        """
        if not self.get_children():
            self.agregar_terminal(path, interprete)
            return

        text = "bash"
        if "bash" in interprete:
            text = "bash"
        elif "python" in interprete:
            text = "python"
        if "ipython" in interprete:
            text = "ipython"

        label = self.get_tab_label(self.get_children()[
            self.get_current_page()]).get_children()[0]
        label.set_text(text)

        terminal = self.get_children()[self.get_current_page()].get_child()
        terminal.set_interprete(path=path, interprete=interprete)

    def accion_terminal(self, accion):
        """
        Soporte para clipboard y agregar una terminal nueva.
        """
        if self.get_children():
            terminal = self.get_children()[self.get_current_page()].get_child()
            terminal.child_focus(True)
            if accion == 'copiar':
                if terminal.get_has_selection():
                    terminal.copy_clipboard()
            elif accion == 'pegar':
                terminal.paste_clipboard()
            elif accion == "agregar":
                self.agregar_terminal()
        else:
            self.agregar_terminal()
            terminal = self.get_children()[self.get_current_page()].get_child()
            terminal.child_focus(True)
            if accion == 'copiar':
                if terminal.get_has_selection():
                    terminal.copy_clipboard()
            elif accion == 'pegar':
                terminal.paste_clipboard()


class VTETerminal(Vte.Terminal):
    """
    Terminal Configurable en distintos intérpretes.
    """

    __gtype_name__ = 'Terminal'

    __gsignals__ = {
    "reset": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, path=os.environ["HOME"], interprete="/bin/bash",
        archivo=None, fuente=Pango.FontDescription("Monospace %s" % 10)):

        Vte.Terminal.__init__(self)

        self.set_encoding('utf-8')
        self.set_font(fuente)

        #self.set_colors(Gdk.color_parse('#ffffff'),
        #    Gdk.color_parse('#000000'), [])

        self.path = path
        self.interprete = interprete

        self.show_all()
        self.__reset(archivo=archivo)

    def __reset(self, archivo=None):
        """
        Reseteo de la Terminal.
        """
        if archivo:
            interprete = "/bin/bash"
            try:
                if "python" in mimetypes.guess_type(archivo)[0]:
                    interprete = "python"
                    if os.path.exists(os.path.join("/bin", interprete)):
                        interprete = os.path.join("/bin", interprete)
                    elif os.path.exists(os.path.join("/usr/bin", interprete)):
                        interprete = os.path.join("/usr/bin", interprete)
                    elif os.path.exists(os.path.join("/sbin", interprete)):
                        interprete = os.path.join("/sbin", interprete)
                    elif os.path.exists(
                        os.path.join("/usr/local", interprete)):
                        interprete = os.path.join("/usr/local", interprete)
            except:
                ### Cuando se intenta ejecutar un archivo no ejecutable.
                return self.set_interprete()
            path = os.path.dirname(archivo)
            pty_flags = Vte.PtyFlags(0)
            # FIXME: en versiones nuevas es spawn_sync
            try:
                self.fork_command_full(pty_flags, path,
                    (interprete, archivo), "", 0, None, None)
            except:
                self.spawn_sync(pty_flags, path,
                    (interprete, archivo), "", 0, None, None)
        else:
            interprete = self.interprete
            path = self.path
            pty_flags = Vte.PtyFlags(0)
            # FIXME: en versiones nuevas es spawn_sync
            try:
                self.fork_command_full(pty_flags, path,
                    (interprete,), "", 0, None, None)
            except:
                self.spawn_sync(pty_flags, path,
                (interprete,), "", 0, None, None)
        self.child_focus(True)

    def re_set_font(self, fuente):
        """
        Setea la fuente.
        """
        self.set_font(fuente)

    def do_child_exited(self, ret=0):
        """
        Cuando se hace exit en la terminal, esta se resetea.
        FIXME: ret es un parámetro nuevo de VTE.
        """
        self.__reset()
        self.emit("reset")

    def set_interprete(self, path=os.environ["HOME"],
        interprete="/bin/bash"):
        """
        Setea la terminal a un determinado interprete.
        """
        self.path = path
        self.interprete = interprete
        self.__reset()
