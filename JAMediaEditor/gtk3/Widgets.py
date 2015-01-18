#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Widgets.py por:
#     Cristian García    <cristian99garcia@gmail.com>
#     Ignacio Rodriguez  <nachoel01@gmail.com>
#     Flavio Danesse     <fdanesse@gmail.com>

# This program is free software; you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110 - 1301 USA

import os
import commands

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

BASE_PATH = os.path.dirname(__file__)


class Menu(Gtk.MenuBar):
    """
    Toolbar Principal.
    """

    __gtype_name__ = 'JAMediaEditorMenu'

    __gsignals__ = {
    'accion_proyecto': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    'accion_archivo': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    'accion_ver': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN)),
    'accion_codigo': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    'run_jamediapygihack': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, accel_group):

        Gtk.MenuBar.__init__(self)

        self.dict_archivo = {}
        self.dict_proyecto = {}

        item_proyectos = Gtk.MenuItem('Proyecto')
        item_archivos = Gtk.MenuItem('Archivo')
        item_edicion = Gtk.MenuItem('Edición')
        item_ver = Gtk.MenuItem('Ver')
        item_codigo = Gtk.MenuItem('Código')
        item_ayuda = Gtk.MenuItem('Ayuda')

        menu_proyectos = Gtk.Menu()
        menu_archivos = Gtk.Menu()
        menu_edicion = Gtk.Menu()
        menu_ver = Gtk.Menu()
        menu_codigo = Gtk.Menu()
        menu_ayuda = Gtk.Menu()

        item_proyectos.set_submenu(menu_proyectos)
        item_archivos.set_submenu(menu_archivos)
        item_edicion.set_submenu(menu_edicion)
        item_ver.set_submenu(menu_ver)
        item_codigo.set_submenu(menu_codigo)
        item_ayuda.set_submenu(menu_ayuda)

        self.append(item_proyectos)
        self.append(item_archivos)
        self.append(item_edicion)
        self.append(item_ver)
        self.append(item_codigo)
        self.append(item_ayuda)

        # Items del Menú Proyectos
        item = Gtk.MenuItem('Nuevo . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Nuevo Proyecto")
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('N'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Abrir . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Abrir Proyecto")
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('O'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Editar . . .')
        item.connect("activate",
            self.__emit_accion_proyecto, "Editar Proyecto")
        self.dict_proyecto["Editar Proyecto"] = item
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('E'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Cerrar')
        item.connect("activate",
            self.__emit_accion_proyecto, "Cerrar Proyecto")
        self.dict_proyecto["Cerrar Proyecto"] = item
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('W'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Guardar')
        item.connect("activate",
            self.__emit_accion_proyecto, "Guardar Proyecto")
        self.dict_proyecto["Guardar Proyecto"] = item
        menu_proyectos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('S'), Gdk.ModifierType.SHIFT_MASK |
            Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Construir . . .')
        item.connect("activate", self.__emit_accion_proyecto, "Construir")
        self.dict_proyecto["Construir"] = item
        menu_proyectos.append(item)

        # Items del Menú Archivos
        item = Gtk.MenuItem('Nuevo')
        item.connect("activate", self.__emit_accion_archivo, "Nuevo Archivo")
        menu_archivos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('N'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Abrir . . .')
        item.connect("activate", self.__emit_accion_archivo, "Abrir Archivo")
        menu_archivos.append(item)
        item.add_accelerator("activate", accel_group,
            ord('O'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Guardar')
        item.connect("activate", self.__emit_accion_archivo, "Guardar Archivo")
        menu_archivos.append(item)
        self.dict_archivo['Guardar'] = item
        item.add_accelerator("activate", accel_group,
            ord('S'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Guardar Como ...')
        item.connect("activate", self.__emit_accion_archivo, "Guardar Como")
        menu_archivos.append(item)

        # Items del Menú Edición
        item = Gtk.MenuItem('Deshacer')
        item.connect("activate", self.__emit_accion_archivo, "Deshacer")
        menu_edicion.append(item)
        self.dict_archivo['Deshacer'] = item
        item.add_accelerator("activate", accel_group,
            ord('Z'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Rehacer')
        item.connect("activate", self.__emit_accion_archivo, "Rehacer")
        menu_edicion.append(item)
        self.dict_archivo['Rehacer'] = item
        item.add_accelerator("activate", accel_group,
            ord('Z'), Gdk.ModifierType.CONTROL_MASK |
            Gdk.ModifierType.SHIFT_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Cortar')
        item.connect("activate", self.__emit_accion_archivo, "Cortar")
        menu_edicion.append(item)
        self.dict_archivo['Cortar'] = item
        item.add_accelerator("activate", accel_group,
            ord('X'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Copiar')
        item.connect("activate", self.__emit_accion_archivo, "Copiar")
        menu_edicion.append(item)
        self.dict_archivo['Copiar'] = item
        item.add_accelerator("activate", accel_group,
            ord('C'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Pegar')
        item.connect("activate", self.__emit_accion_archivo, "Pegar")
        self.dict_archivo['Pegar'] = item
        menu_edicion.append(item)
        item.add_accelerator("activate", accel_group,
            ord('V'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Seleccionar Todo')
        item.connect("activate",
            self.__emit_accion_archivo, "Seleccionar Todo")
        self.dict_archivo['Seleccionar Todo'] = item
        menu_edicion.append(item)
        item.add_accelerator("activate", accel_group,
            ord('A'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        # Items del menú Ver
        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()
        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.CheckButton()
        button.set_active(True)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("Numeros de línea")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_ver, "Numeracion")
        menu_ver.append(item)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()
        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.CheckButton()
        button.set_active(False)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("Panel inferior")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_ver, "Panel inferior")
        menu_ver.append(item)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()
        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.CheckButton()
        button.set_active(True)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("Panel lateral")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_ver, "Panel lateral")
        menu_ver.append(item)

        # Items del Menú Código
        item = Gtk.MenuItem('Aumentar')
        item.connect("activate", self.__emit_accion_codigo, "Aumentar")
        self.dict_archivo['Aumentar'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord("+"), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Disminuir')
        item.connect("activate", self.__emit_accion_codigo, "Disminuir")
        self.dict_archivo['Disminuir'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('-'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Formato de Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Formato")
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('T'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Identar')
        item.connect("activate", self.__emit_accion_codigo, "Identar")
        self.dict_archivo['Identar'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('I'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('De Identar')
        item.connect("activate", self.__emit_accion_codigo, "De Identar")
        self.dict_archivo['De Identar'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('I'), Gdk.ModifierType.CONTROL_MASK |
            Gdk.ModifierType.SHIFT_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Buscar Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Buscar Texto")
        self.dict_archivo['Buscar Texto'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('B'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Reemplazar Texto . . .')
        item.connect("activate", self.__emit_accion_codigo, "Reemplazar Texto")
        self.dict_archivo['Reemplazar Texto'] = item
        menu_codigo.append(item)
        item.add_accelerator("activate", accel_group,
            ord('R'), Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)

        item = Gtk.MenuItem('Chequear sintaxis')
        item.connect("activate", self.__emit_accion_codigo, "Chequear")
        self.dict_archivo['Chequear'] = item
        menu_codigo.append(item)

        # Items del Menú Ayuda
        item = Gtk.MenuItem('Créditos')
        item.connect("activate", self.__run_about)
        menu_ayuda.append(item)

        item = Gtk.MenuItem('JAMediaPyGiHack')
        item.connect("activate", self.__emit_run_jamediapygihack)
        menu_ayuda.append(item)

        self.show_all()

    def __emit_run_jamediapygihack(self, widget):
        self.emit('run_jamediapygihack')

    def __run_about(self, widget):
        dialog = Credits(parent=self.get_toplevel())
        dialog.run()
        dialog.destroy()

    def __emit_accion_codigo(self, widget, accion):
        self.emit('accion_codigo', accion)

    def __emit_accion_ver(self, widget, accion):
        valor = not widget.get_children()[0].get_children()[0].get_active()
        widget.get_children()[0].get_children()[0].set_active(valor)
        self.emit('accion_ver', accion, valor)

    def __emit_accion_archivo(self, widget, accion):
        self.emit('accion_archivo', accion)

    def __emit_accion_proyecto(self, widget, accion):
        self.emit('accion_proyecto', accion)

    def activar_proyecto(self, sensitive):
        # Activa o desactiva opciones.
        if sensitive:
            map(self.__activar, self.dict_proyecto.values())
        else:
            map(self.__desactivar, self.dict_proyecto.values())

    def update_archivos(self, _dict):
        # Activa o desactiva opciones.
        activar = []
        desactivar = []

        if _dict['rehacer']:
            activar.append(self.dict_archivo['Rehacer'])
        else:
            desactivar.append(self.dict_archivo['Rehacer'])

        if _dict['deshacer']:
            activar.append(self.dict_archivo['Deshacer'])
        else:
            desactivar.append(self.dict_archivo['Deshacer'])

        if _dict['modificado']:
            activar.append(self.dict_archivo['Guardar'])
        else:
            desactivar.append(self.dict_archivo['Guardar'])

        if _dict['clipboard_texto']:
            activar.append(self.dict_archivo['Pegar'])
        else:
            desactivar.append(self.dict_archivo['Pegar'])

        if _dict['texto_seleccionado']:
            activar.extend([
                self.dict_archivo['Cortar'],
                self.dict_archivo['Copiar'],
                ])
        else:
            desactivar.extend([
                self.dict_archivo['Cortar'],
                self.dict_archivo['Copiar'],
                ])

        if _dict['tiene_texto']:
            activar.extend([
                self.dict_archivo['Identar'],
                self.dict_archivo['De Identar'],
                self.dict_archivo['Buscar Texto'],
                self.dict_archivo['Reemplazar Texto'],
                self.dict_archivo['Seleccionar Todo'],
                self.dict_archivo['Chequear'],
                self.dict_archivo['Disminuir'],
                self.dict_archivo['Aumentar'],
                ])
        else:
            desactivar.extend([
                self.dict_archivo['Identar'],
                self.dict_archivo['De Identar'],
                self.dict_archivo['Buscar Texto'],
                self.dict_archivo['Reemplazar Texto'],
                self.dict_archivo['Seleccionar Todo'],
                self.dict_archivo['Chequear'],
                self.dict_archivo['Disminuir'],
                self.dict_archivo['Aumentar'],
                ])

        map(self.__activar, activar)
        map(self.__desactivar, desactivar)

    def __activar(self, option):
        if not option.get_sensitive():
            option.set_sensitive(True)

    def __desactivar(self, option):
        if option.get_sensitive():
            option.set_sensitive(False)


class DialogoBuscar(Gtk.Dialog):

    __gtype_name__ = 'JAMediaEditorDialogoBuscar'

    def __init__(self, view, parent_window=None,
        title="Buscar Texto", texto=None):

        Gtk.Dialog.__init__(self, title=title, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL)

        self.set_border_width(15)

        self.view = view
        self.entrada = Gtk.Entry()

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Buscar:"), True, True, 3)
        hbox.pack_start(self.entrada, False, False, 0)
        hbox.show_all()

        self.vbox.pack_start(hbox, False, False, 3)

        self.boton_anterior = Gtk.Button('Buscar anterior')
        self.boton_siguiente = Gtk.Button('Buscar siguiente')
        self.boton_cerrar = Gtk.Button('Cerrar')

        hbox = Gtk.HBox()
        hbox.pack_start(self.boton_anterior, True, True, 3)
        hbox.pack_start(self.boton_siguiente, True, True, 3)
        hbox.pack_start(self.boton_cerrar, True, True, 0)
        hbox.show_all()

        self.vbox.pack_start(hbox, False, False, 0)

        self.boton_anterior.set_sensitive(False)
        self.boton_siguiente.set_sensitive(False)

        self.boton_anterior.connect('clicked', self.__buscar, 'Atras')
        self.boton_siguiente.connect('clicked', self.__buscar, 'Adelante')
        self.boton_cerrar.connect('clicked', self.__destroy)
        self.entrada.connect("changed", self.__changed)

        if texto:
            self.entrada.set_text(texto)
            seleccion = self.view.get_buffer().get_selection_bounds()
            GLib.idle_add(self.__update, texto, seleccion)

    def __update(self, texto, selection):
        # Cuando se abre el dialogo selecciona la primer ocurrencia.
        _buffer = self.view.get_buffer()
        start, end = _buffer.get_bounds()
        contenido = _buffer.get_text(start, end, 0)
        numero = len(contenido)
        if end.get_offset() == numero and not selection:
            # Si está al final, vuelve al principio.
            inicio = _buffer.get_start_iter()
            self.__seleccionar_texto(texto, inicio, 'Adelante')
        else:
            if selection:
                inicio, fin = selection
                _buffer.select_range(inicio, fin)
        return False

    def __changed(self, widget):
        # Habilita y deshabilita los botones de busqueda y reemplazo.
        self.boton_anterior.set_sensitive(bool(self.entrada.get_text()))
        self.boton_siguiente.set_sensitive(bool(self.entrada.get_text()))

    def __buscar(self, widget, direccion):
        # Busca el texto en el buffer.
        texto = self.entrada.get_text()
        _buffer = self.view.get_buffer()
        inicio, fin = _buffer.get_bounds()

        texto_actual = _buffer.get_text(inicio, fin, 0)
        posicion = _buffer.get_iter_at_mark(_buffer.get_insert())
        if texto:
            if texto in texto_actual:
                inicio = posicion
                if direccion == 'Adelante':
                    if inicio.get_offset() == _buffer.get_char_count():
                        inicio = _buffer.get_start_iter()

                elif direccion == 'Atras':
                    if _buffer.get_selection_bounds():
                        start, end = _buffer.get_selection_bounds()
                        contenido = _buffer.get_text(start, end, 0)
                        numero = len(contenido)
                        if end.get_offset() == numero:
                            inicio = _buffer.get_end_iter()
                        else:
                            inicio = _buffer.get_selection_bounds()[0]
                self.__seleccionar_texto(texto, inicio, direccion)
            else:
                _buffer.select_range(posicion, posicion)

    def __seleccionar_texto(self, texto, inicio, direccion):
        # Selecciona el texto solicitado, y mueve el scroll sí es necesario.
        _buffer = self.view.get_buffer()
        if direccion == 'Adelante':
            match = inicio.forward_search(texto, 0, None)
        elif direccion == 'Atras':
            match = inicio.backward_search(texto, 0, None)
        if match:
            match_start, match_end = match
            _buffer.select_range(match_end, match_start)
            self.view.scroll_to_iter(match_end, 0.1, 1, 1, 0.1)
        else:
            if direccion == 'Adelante':
                inicio = _buffer.get_start_iter()
            elif direccion == 'Atras':
                inicio = _buffer.get_end_iter()
            self.__seleccionar_texto(texto, inicio, direccion)

    def __destroy(self, widget=None):
        self.destroy()


class DialogoReemplazar(Gtk.Dialog):

    __gtype_name__ = 'JAMediaEditorDialogoReemplazar'

    def __init__(self, view, parent_window=None,
        title="Reemplazar Texto", texto=None):

        Gtk.Dialog.__init__(self, title=title, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL)

        self.set_border_width(15)
        self.view = view

        # Entries.
        self.buscar_entry = Gtk.Entry()
        self.reemplazar_entry = Gtk.Entry()

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Buscar:"), True, True, 3)
        hbox.pack_start(self.buscar_entry, False, False, 0)
        hbox.show_all()
        self.vbox.pack_start(hbox, False, False, 3)

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Reemplazar:"), True, True, 3)
        hbox.pack_start(self.reemplazar_entry, False, False, 0)
        hbox.show_all()
        self.vbox.pack_start(hbox, False, False, 10)

        # Buttons.
        cerrar = Gtk.Button("Cerrar")
        self.reemplazar = Gtk.Button("Reemplazar")
        self.button_buscar = Gtk.Button("Saltear")

        hbox = Gtk.HBox()
        hbox.pack_start(self.reemplazar, True, True, 3)
        hbox.pack_start(self.button_buscar, True, True, 3)
        hbox.pack_start(cerrar, True, True, 0)
        hbox.show_all()
        self.vbox.pack_start(hbox, False, False, 0)

        self.reemplazar.set_sensitive(False)
        self.button_buscar.set_sensitive(False)

        cerrar.connect("clicked", self.__destroy)
        self.button_buscar.connect('clicked', self.__buscar, 'Adelante')
        self.reemplazar.connect("clicked", self.__reemplazar)

        if texto:
            self.buscar_entry.set_text(texto)
            seleccion = self.view.get_buffer().get_selection_bounds()
            GLib.idle_add(self.__update, texto, seleccion)

        GLib.idle_add(self.__changed)

    def __update(self, texto, selection):
        # Cuando se abre el dialogo selecciona la primer ocurrencia.
        _buffer = self.view.get_buffer()
        start, end = _buffer.get_bounds()
        contenido = _buffer.get_text(start, end, 0)
        numero = len(contenido)
        if end.get_offset() == numero and not selection:
            inicio = _buffer.get_start_iter()
            self.__seleccionar_texto(texto, inicio, 'Adelante')
        else:
            inicio, fin = selection
            _buffer.select_range(inicio, fin)

    def __changed(self):
        # Habilita y deshabilita los botones de busqueda y reemplazo.
        self.button_buscar.set_sensitive(bool(self.buscar_entry.get_text()))
        _buffer = self.view.get_buffer()
        select = _buffer.get_selection_bounds()
        if len(select) == 2:
            select = True
        else:
            select = False
        self.reemplazar.set_sensitive(select and \
            bool(self.buscar_entry.get_text()) and \
            bool(self.reemplazar_entry.get_text()))
        return True

    def __buscar(self, widget, direccion):
        try:
            texto = self.buscar_entry.get_text()
            _buffer = self.view.get_buffer()
            inicio, fin = _buffer.get_bounds()
            texto_actual = _buffer.get_text(inicio, fin, 0)
            posicion = _buffer.get_iter_at_mark(_buffer.get_insert())
            if texto:
                if texto in texto_actual:
                    inicio = posicion
                    if direccion == 'Adelante':
                        if inicio.get_offset() == _buffer.get_char_count():
                            inicio = _buffer.get_start_iter()
                    elif direccion == 'Atras':
                        if _buffer.get_selection_bounds():
                            start, end = _buffer.get_selection_bounds()
                            contenido = _buffer.get_text(start, end, 0)
                            numero = len(contenido)
                            if end.get_offset() == numero:
                                inicio = _buffer.get_end_iter()
                            else:
                                inicio = _buffer.get_selection_bounds()[0]
                    self.__seleccionar_texto(texto, inicio, direccion)
                else:
                    buffer.select_range(posicion, posicion)
        except:
            print "FIXME: Error en:", self.__buscar
            # Cuando se reemplaza texto y llega al final del archivo,
            # al parecer no afecta en nada a la aplicación.

    def __destroy(self, widget=None, event=None):
        self.destroy()

    def __reemplazar(self, widget):
        _buffer = self.view.get_buffer()
        inicio, fin = _buffer.get_selection_bounds()
        texto_reemplazo = self.reemplazar_entry.get_text()
        _buffer.delete(inicio, fin)
        _buffer.insert_at_cursor(texto_reemplazo)
        self.button_buscar.clicked()

    def __seleccionar_texto(self, texto, inicio, direccion):
        # Selecciona el texto solicitado, y mueve el scroll sí es necesario.
        _buffer = self.view.get_buffer()
        if direccion == 'Adelante':
            match = inicio.forward_search(texto, 0, None)
        elif direccion == 'Atras':
            match = inicio.backward_search(texto, 0, None)

        if match:
            match_start, match_end = match
            _buffer.select_range(match_end, match_start)
            self.view.scroll_to_iter(match_end, 0.1, 1, 1, 0.1)
        else:
            if direccion == 'Adelante':
                inicio = _buffer.get_start_iter()
            elif direccion == 'Atras':
                inicio = _buffer.get_end_iter()
            self.__seleccionar_texto(texto, inicio, direccion)


class My_FileChooser(Gtk.FileChooserDialog):

    __gtype_name__ = 'JAMediaEditorMy_FileChooser'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, parent_window=None, action_type=None, filter_type=[],
        title=None, path=None, mime_type=[]):

        Gtk.FileChooserDialog.__init__(self, parent=parent_window,
            action=action_type, flags=Gtk.DialogFlags.MODAL, title=title)

        self.set_default_size(640, 480)
        self.set_select_multiple(False)

        if os.path.isfile(path):
            self.set_filename(path)
        else:
            self.set_current_folder_uri("file://%s" % path)

        if filter_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for fil in filter_type:
                _filter.add_pattern(fil)
            self.add_filter(_filter)

        elif mime_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for mime in mime_type:
                _filter.add_mime_type(mime)
            self.add_filter(_filter)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        texto = ""
        if action_type == Gtk.FileChooserAction.OPEN or \
            action_type == Gtk.FileChooserAction.SELECT_FOLDER:
            texto = "Abrir"

        elif action_type == Gtk.FileChooserAction.SAVE:
            texto = "Guardar"

        abrir = Gtk.Button(texto)
        salir = Gtk.Button("Salir")

        hbox.pack_end(salir, True, True, 5)
        hbox.pack_end(abrir, True, True, 5)
        self.set_extra_widget(hbox)

        salir.connect("clicked", self.__salir)
        abrir.connect("clicked", self.__abrir)
        self.show_all()
        self.connect("file-activated", self.__file_activated)

    def __file_activated(self, widget):
        # Cuando se hace doble click sobre un archivo.
        self.__abrir()

    def __abrir(self, widget=None):
        direccion = self.get_filename()
        if not direccion:
            return self.__salir()

        direccion = os.path.realpath(direccion)
        # Para abrir solo archivos, de lo contrario el filechooser
        # se está utilizando para "guardar como".
        if os.path.exists(direccion):
            if not os.path.isfile(direccion):
                return self.__salir()

        # Emite el path del archivo seleccionado.
        self.emit('load', direccion)
        self.__salir()

    def __salir(self, widget=None):
        self.destroy()


class Multiple_FileChooser(Gtk.FileChooserDialog):

    __gtype_name__ = 'JAMediaEditorMultiple_FileChooser'

    __gsignals__ = {
    'load': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, parent_window=None, filter_type=[], title=None,
        path=None, mime_type=[]):

        Gtk.FileChooserDialog.__init__(self, parent=parent_window,
            action=Gtk.FileChooserAction.OPEN, flags=Gtk.DialogFlags.MODAL,
            title=title)

        self.set_default_size(640, 480)
        self.set_select_multiple(True)

        if os.path.isfile(path):
            self.set_filename(path)
        else:
            self.set_current_folder_uri("file://%s" % path)

        if filter_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for fil in filter_type:
                _filter.add_pattern(fil)
            self.add_filter(_filter)

        elif mime_type:
            _filter = Gtk.FileFilter()
            _filter.set_name("Filtro")
            for mime in mime_type:
                _filter.add_mime_type(mime)
            self.add_filter(_filter)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        abrir = Gtk.Button("Abrir")
        salir = Gtk.Button("Salir")

        hbox.pack_end(salir, True, True, 5)
        hbox.pack_end(abrir, True, True, 5)
        self.set_extra_widget(hbox)

        salir.connect("clicked", self.__salir)
        abrir.connect("clicked", self.__abrir)
        self.show_all()
        self.connect("file-activated", self.__file_activated)

    def __file_activated(self, widget):
        # Cuando se hace doble click sobre un archivo.
        self.__abrir()

    def __abrir(self, widget=None):
        files = self.get_filenames()
        if files:
            for _file in files:
                direccion = os.path.realpath(_file)
                if os.path.exists(direccion) and os.path.isfile(direccion):
                    # Emite el path del archivo seleccionado.
                    self.emit('load', direccion)
        self.__salir()

    def __salir(self, widget=None):
        self.destroy()


class DialogoAlertaSinGuardar(Gtk.Dialog):
    """
    Diálogo para Alertar al usuario al cerrar un archivo
    que contiene cambios sin guardar.
    """

    __gtype_name__ = 'JAMediaEditorDialogoAlertaSinGuardar'

    def __init__(self, parent_window=None):

        Gtk.Dialog.__init__(self, title="ATENCION !", parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Guardar y Continuar", Gtk.ResponseType.ACCEPT,
                "Continuar sin Guardar", Gtk.ResponseType.CLOSE,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.set_size_request(400, 150)
        self.set_border_width(15)

        label = Gtk.Label(
            "No se han guardado los ultimos cambios en el archivo.")

        label.show()
        self.vbox.add(label)


class DialogoSobreEscritura(Gtk.Dialog):
    """
    Diálogo para Alertar al usuario sobre reescritura de un archivo.
    """

    __gtype_name__ = 'JAMediaEditorDialogoSobreEscritura'

    def __init__(self, parent_window=None):

        Gtk.Dialog.__init__(self, title="ATENCION !", parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Guardar", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.set_size_request(400, 150)
        self.set_border_width(15)

        label = Gtk.Label("El archivo ya axiste. ¿Deseas sobre escribirlo?")

        label.show()
        self.vbox.add(label)


class DialogoErrores(Gtk.Dialog):
    """
    Diálogo para chequear errores
    """

    __gtype_name__ = 'JAMediaEditorDialogoErrores'

    def __init__(self, view, parent_window=None):

        Gtk.Dialog.__init__(self, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Aceptar", Gtk.ResponseType.ACCEPT])

        self.set_size_request(600, 250)
        self.set_border_width(15)

        errores = ErroresTreeview(view)
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(errores)

        label = Gtk.Label("Errores")

        label.show()
        scroll.show_all()

        self.vbox.pack_start(label, False, False, 0)
        self.vbox.pack_start(scroll, True, True, 3)


class ErroresTreeview(Gtk.TreeView):

    __gtype_name__ = 'JAMediaEditorErroresTreeview'

    def __init__(self, view):

        Gtk.TreeView.__init__(self,
            Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.view = view

        columna = Gtk.TreeViewColumn("Línea", Gtk.CellRendererText(), text=0)
        self.append_column(columna)

        columna = Gtk.TreeViewColumn("Error", Gtk.CellRendererText(), text=1)
        self.append_column(columna)

        _buffer = view.get_buffer()
        start, end = _buffer.get_bounds()
        texto = _buffer.get_text(start, end, True)

        path = os.path.join("/dev/shm", "check_temp.py")
        arch = open(path, "w")
        arch.write(texto)
        arch.close()

        check = os.path.join(BASE_PATH, "Check1.py")
        errores = commands.getoutput('python %s %s' % (check, path))

        for linea in errores.splitlines():
            try:
                item_str = linea.split("%s:" % path)[1]
                #if not path in item_str:
                numero = item_str.split(":")[0].strip()
                comentario = item_str.replace(item_str.split()[0], "").strip()
                item = [numero, comentario]
                self.get_model().append(item)

            except:
                pass

        check = os.path.join(BASE_PATH, "Check2.py")
        errores = commands.getoutput('python %s %s' % (check, path))

        for linea in errores.splitlines():
            try:
                item_str = linea.split("%s:" % path)[1]
                #if not path in item_str:
                numero = item_str.split(":")[0].strip()
                comentario = item_str.replace(item_str.split()[0], "").strip()
                item = [numero, comentario]
                self.get_model().append(item)

            except:
                pass

        self.show_all()
        self.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        self.get_selection().set_select_function(
            self.__clicked, self.get_model())

    def __clicked(self, treeselection,
        model, path, is_selected, listore):
        iter_sel = model.get_iter(path)
        linea = model.get_value(iter_sel, 0)
        self.view.marcar_error(int(linea))
        return True


class Estructura_Menu(Gtk.Menu):
    """
    Menu con opciones para treeview de Estructura.
    """

    __gtype_name__ = 'JAMediaEditorEstructura_Menu'

    __gsignals__ = {
    'accion': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING, GObject.TYPE_PYOBJECT))}

    def __init__(self, widget, boton, pos,
        tiempo, path, modelo, accion_previa):

        Gtk.Menu.__init__(self)

        iterfirst = modelo.get_iter_first()
        _iter = modelo.get_iter(path)
        filepath = modelo.get_value(_iter, 2)

        lectura, escritura, ejecucion = self.__verificar_permisos(filepath)
        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                datos = commands.getoutput(
                    'file - ik %s%s%s' % ("\"", filepath, "\""))

                if "text" in datos or "x - python" in datos and lectura:
                    self.__get_item(widget, path, "abrir")

                if lectura:
                    self.__get_item(widget, path, "copiar")

                if escritura:
                    self.__get_item(widget, path, "cortar")

                if escritura:
                    self.__get_item(widget, path, "suprimir")

                if "text" in datos or "x-python" in datos and lectura:
                    self.__get_item(widget, path, "buscar")

            elif os.path.isdir(filepath):
                if filepath == modelo.get_value(iterfirst, 2):
                    self.__get_item(widget, path, "eliminar proyecto")
                    self.__get_item(widget, path, "Crear Directorio")

                    if escritura and "copiar" in accion_previa or \
                        "cortar" in accion_previa:
                        self.__get_item(widget, path, "pegar")

                    self.__get_item(widget, path, "buscar")

                else:
                    if lectura:
                        self.__get_item(widget, path, "copiar")

                    if escritura and lectura:
                        self.__get_item(widget, path, "cortar")

                    if escritura and "copiar" in accion_previa or \
                        "cortar" in accion_previa:
                        self.__get_item(widget, path, "pegar")

                    if escritura:
                        self.__get_item(widget, path, "suprimir")
                        self.__get_item(widget, path, "Crear Directorio")

                    if lectura:
                        self.__get_item(widget, path, "buscar")

        self.show_all()
        self.attach_to_widget(widget, self.__null)

    def __verificar_permisos(self, path):
        # verificar:
        # 1 - Si es un archivo o un directorio
        # 2 - Si sus permisos permiten la copia, escritura y borrado

        # Comprobar existencia y permisos:
        # http://docs.python.org/library/os.html?highlight=os#module-os
        # os.access(path, mode)
        # os.F_OK # si existe la direccion
        # os.R_OK # Permisos de lectura
        # os.W_OK # Permisos de escritura
        # os.X_OK # Permisos de ejecucion

        if not os.path.exists(path):
            return False, False, False

        try:
            if os.access(path, os.F_OK):
                r = os.access(path, os.R_OK)
                w = os.access(path, os.W_OK)
                x = os.access(path, os.X_OK)
                return r, w, x

            else:
                return False, False, False

        except:
            return False, False, False

    def __null(self):
        pass

    def __get_item(self, widget, path, accion):
        """
        Agrega un item al menu.
        """
        item = Gtk.MenuItem("%s%s" % (accion[0].upper(), accion[1:]))
        self.append(item)
        item.connect_object("activate", self.__set_accion, widget,
            path, accion)

    def __set_accion(self, widget, path, accion):
        """
        Responde a la seleccion del usuario sobre el menu.
        """
        _iter = widget.get_model().get_iter(path)
        self.emit('accion', widget, accion, _iter)


class DialogoEliminar(Gtk.Dialog):
    """
    Diálogo para confirmar la eliminación del archivo / directorio seleccionado
    """

    __gtype_name__ = 'JAMediaEditorDialogoEliminar'

    def __init__(self, tipo="Archivo", parent_window=None):

        Gtk.Dialog.__init__(self, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Si, eliminar!", Gtk.ResponseType.ACCEPT,
                "Cancelar", Gtk.ResponseType.CANCEL])

        self.set_size_request(300, 100)
        self.set_border_width(15)

        label = Gtk.Label(
            "Estás Seguro de que Deseas Eliminar\nel %s Seleccionado?" % tipo)

        label.show()
        self.vbox.pack_start(label, True, True, 0)


class BusquedaGrep(Gtk.Dialog):
    """
    Dialogo con un TreeView para busquedas con Grep
    """

    __gtype_name__ = 'JAMediaEditorBusquedaGrep'

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self, path=None, parent_window=None):

        Gtk.Dialog.__init__(self, parent=parent_window,
            flags=Gtk.DialogFlags.MODAL,
            buttons=[
                "Cerrar", Gtk.ResponseType.ACCEPT])

        self.path = path

        self.set_size_request(600, 250)
        self.set_border_width(15)

        self.treeview = TreeViewBusquedaGrep()
        self.entry = Gtk.Entry()
        buscar = Gtk.Button("Buscar")

        hbox = Gtk.HBox()
        hbox.pack_start(self.entry, False, False, 0)
        hbox.pack_start(buscar, False, False, 0)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.treeview)

        scroll.show_all()
        hbox.show_all()

        self.vbox.pack_start(hbox, False, False, 0)
        self.vbox.pack_start(scroll, True, True, 0)

        buscar.connect("clicked", self.__buscar)
        self.treeview.connect("nueva-seleccion",
            self.__re_emit_nueva_seleccion)

    def __re_emit_nueva_seleccion(self, widget, valor):
        self.emit("nueva-seleccion", valor)

    def __buscar(self, widget):
        """
        Realiza la búsqueda solicitada.
        """
        text = self.entry.get_text().strip()
        if text:
            if os.path.isdir(self.path):
                result = commands.getoutput(
                    "less | grep -R -n \'%s\' %s" % (text, self.path))
                result = result.splitlines()

            elif os.path.isfile(self.path):
                result = commands.getoutput(
                    "less | grep -n \'%s\' %s" % (text, self.path))
                result = result.splitlines()

            items = []
            for line in result:
                dat = line.split(":")
                if os.path.isdir(self.path):
                    if len(dat) == 3:
                        items.append([dat[0], dat[1], dat[2].strip()])

                elif os.path.isfile(self.path):
                    if len(dat) == 2:
                        items.append([self.path, dat[0], dat[1].strip()])

            self.treeview.limpiar()
            self.treeview.agregar_items(items)


class TreeViewBusquedaGrep(Gtk.TreeView):

    __gtype_name__ = 'JAMediaEditorTreeViewBusquedaGrep'

    __gsignals__ = {
    "nueva-seleccion": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT, ))}

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.ListStore(
            GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_headers_clickable(True)
        self.set_headers_visible(True)

        self.__setear_columnas()
        self.treeselection = self.get_selection()
        self.show_all()

    def do_row_activated(self, path, treviewcolumn):
        model = self.get_model()
        _iter = model.get_iter(path)
        valor = [
            model.get_value(_iter, 0),
            model.get_value(_iter, 1),
            model.get_value(_iter, 2)]

        self.emit("nueva-seleccion", valor)

    def __setear_columnas(self):
        self.append_column(
            self.__construir_columa('Archivo', 0, True))
        self.append_column(
            self.__construir_columa('N° de línea', 1, True))
        self.append_column(
            self.__construir_columa('Línea', 2, True))

    def __construir_columa(self, text, index, visible):
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn(text, render, text=index)
        columna.set_sort_column_id(index)
        columna.set_property('visible', visible)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        return columna

    def limpiar(self):
        self.get_model().clear()

    def agregar_items(self, elementos):
        self.__ejecutar_agregar_elemento(elementos)

    def __ejecutar_agregar_elemento(self, elementos):
        """
        Agrega los items a la lista, uno a uno, actualizando.
        """
        if not elementos:
            self.seleccionar_primero()
            return False

        self.get_model().append(elementos[0])
        elementos.remove(elementos[0])
        GLib.idle_add(self.__ejecutar_agregar_elemento, elementos)
        return False

    def seleccionar_primero(self, widget=None):
        self.treeselection.select_path(0)


class Credits(Gtk.Dialog):

    __gtype_name__ = 'JAMediaEditorCredits'

    def __init__(self, parent=None):

        Gtk.Dialog.__init__(self, parent=parent,
            flags=Gtk.DialogFlags.MODAL,
            buttons=["Cerrar", Gtk.ResponseType.ACCEPT])

        self.set_border_width(15)

        imagen = Gtk.Image()
        imagen.set_from_file(os.path.join(BASE_PATH,
            "Iconos", "JAMediaEditorCredits.svg"))

        self.vbox.pack_start(imagen, False, False, 0)
        self.vbox.show_all()
