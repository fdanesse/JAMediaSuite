#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SourceView.py por:
#     Cristian García    <cristian99garcia@gmail.com>
#     Ignacio Rodriguez  <nachoel01@gmail.com>
#     Flavio Danesse     <fdanesse@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import os
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GtkSource
from gi.repository import Pango
from gi.repository import Gdk
from gi.repository import GLib

from Widgets1 import DialogoSobreEscritura
from Widgets1 import My_FileChooser
from Widgets1 import DialogoBuscar
from Widgets1 import DialogoReemplazar
from Widgets1 import DialogoAlertaSinGuardar
from Widgets2 import DialogoErrores

home = os.environ["HOME"]
BatovideWorkSpace = os.path.join(home, 'BatovideWorkSpace')


class SourceView(GtkSource.View):
    """
    Visor de código para archivos abiertos.
    """

    __gtype_name__ = 'JAMediaEditorSourceView'

    __gsignals__ = {
    'update': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,)),
    "force-select": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_STRING)),
    "update-label": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self, config):

        GtkSource.View.__init__(self)

        self.actualizador = False
        self.control = False
        self.archivo = False
        self.lenguaje = False
        self.tab = "    "

        self.lenguaje_manager = GtkSource.LanguageManager()

        self.set_show_line_numbers(config['numeracion'])
        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)
        self.set_show_right_margin(True)
        self.set_auto_indent(True)
        self.set_smart_home_end(True)
        self.set_highlight_current_line(True)

        font = "%s %s" % (config['fuente'], config['tamanio'])
        self.modify_font(Pango.FontDescription(font))

        self.show_all()
        self.connect("key-press-event", self.__key_press_event)

    def __force_emit_new_select(self):
        # Forzando Instrospección en Panel Lateral.
        lenguaje = False
        if self.lenguaje:
            lenguaje = self.lenguaje.get_name().lower()
        self.emit("force-select", self, lenguaje)
        return False

    def __procesar_y_guardar(self):
        if self.archivo:
            if os.path.exists(self.archivo):
                if not os.access(self.archivo, os.W_OK):
                    print "No tienes permiso para guardar:", self.archivo
                    return False
        _buffer = self.get_buffer()
        inicio, fin = _buffer.get_bounds()
        texto = _buffer.get_text(inicio, fin, 0)

        # Para devolver el scroll a donde estaba.
        textmark = _buffer.get_insert()
        textiter = _buffer.get_iter_at_mark(textmark)
        _id = textiter.get_line()

        # FIXME: Falta que  al guardar archivos py establezca tipo y
        # codificación de los archivos.
        texto = self.__limpiar_codigo(texto)
        archivo = open(self.archivo, "w")
        archivo.write(texto)
        archivo.close()
        self.set_archivo(self.archivo)

        # Devolver el scroll a donde estaba.
        linea_iter = self.get_buffer().get_iter_at_line(_id)
        GLib.idle_add(self.scroll_to_iter, linea_iter, 0.1, 1, 1, 0.1)

    def __limpiar_codigo(self, texto):
        # Cuando se abre o guarda un archivo, se limpia el código en él.
        limpio = ""
        for line in texto.splitlines():
            # Eliminar espacios al final de la linea y en lineas vacías.
            text_line = "%s\n" % (line.rstrip())
            # Cambiar Tabulaciones por 4 espacios
            ret = []
            for l in text_line:
                x = l
                if ord("\t") == ord(l):
                    x = "    "
                ret.append(x)
            text_line = ""
            for l in ret:
                text_line = "%s%s" % (text_line, l)
            limpio = "%s%s" % (limpio, text_line)
        return limpio

    def __guardar_como(self, widget, archivo):
        if archivo:
            archivo = os.path.realpath(archivo)
            if os.path.exists(archivo):
                dialog = DialogoSobreEscritura(
                    parent_window=self.get_toplevel())
                respuesta = dialog.run()
                dialog.destroy()
                if respuesta == Gtk.ResponseType.ACCEPT:
                    self.archivo = archivo
                    self.__procesar_y_guardar()
                elif respuesta == Gtk.ResponseType.CANCEL:
                    return
            else:
                self.archivo = archivo
                self.__procesar_y_guardar()

    def __identar(self):
        """
        Agrega la identación especificada en el texto seleccionado o en la
        linea en que el usuario se encuentra parado.
        """
        _buffer = self.get_buffer()
        if _buffer.get_selection_bounds():
            start, end = _buffer.get_selection_bounds()
            id_0 = start.get_line()
            id_1 = end.get_line()
            for _id in range(id_0, id_1 + 1):
                _iter = _buffer.get_iter_at_line(_id)
                _buffer.insert(_iter, self.tab)
        else:
            textmark = _buffer.get_insert()
            textiter = _buffer.get_iter_at_mark(textmark)
            _id = textiter.get_line()
            line_iter = _buffer.get_iter_at_line(_id)
            _buffer.insert(line_iter, self.tab)

    def __de_identar(self):
        """
        Saca una tabulación a las líneas seleccionadas o en
        la linea donde se encuentra parado el usuario.
        """
        _buffer = self.get_buffer()
        if _buffer.get_selection_bounds():
            start, end = _buffer.get_selection_bounds()
            id_0 = start.get_line()
            id_1 = end.get_line()
            for _id in range(id_0, id_1 + 1):
                line_iter = _buffer.get_iter_at_line(_id)
                chars = line_iter.get_chars_in_line()
                line_end_iter = _buffer.get_iter_at_line_offset(_id, chars - 1)
                texto = _buffer.get_text(line_iter, line_end_iter, True)
                if texto.startswith(self.tab):
                    _buffer.delete(line_iter,
                        _buffer.get_iter_at_line_offset(_id, len(self.tab)))
        else:
            textmark = _buffer.get_insert()
            textiter = _buffer.get_iter_at_mark(textmark)
            _id = textiter.get_line()
            line_iter = _buffer.get_iter_at_line(_id)
            chars = line_iter.get_chars_in_line()
            line_end_iter = _buffer.get_iter_at_line_offset(_id, chars - 1)
            texto = _buffer.get_text(line_iter, line_end_iter, True)
            if texto.startswith(self.tab):
                _buffer.delete(line_iter,
                    _buffer.get_iter_at_line_offset(_id, len(self.tab)))

    def __cerrar(self):
        # Cierra la página en el Notebook_SourceView de este sourceview.
        self.new_handle(False)
        scroll = self.get_parent()
        notebook = scroll.get_parent()
        paginas = notebook.get_n_pages()
        if paginas:
            for indice in range(paginas):
                page = notebook.get_children()[indice]
                if page == scroll:
                    notebook.remove_page(indice)
                    page.destroy()
                    return

    def __key_press_event(self, widget, event):
        # Pretende ser un Tabulador Inteligente.
        if event.keyval == 65421:
            _buffer = self.get_buffer()
            textmark = _buffer.get_insert()
            textiter = _buffer.get_iter_at_mark(textmark)
            _id = textiter.get_line()
            line_iter = _buffer.get_iter_at_line(_id)
            chars = line_iter.get_chars_in_line()
            if chars > 3:
                # Ultimo caracter.
                start_iter = _buffer.get_iter_at_line_offset(_id, chars - 2)
                end_iter = _buffer.get_iter_at_line_offset(_id, chars - 1)
                texto = _buffer.get_text(start_iter, end_iter, True)
                if texto == ":":
                    # Tola la linea.
                    line_end_iter = _buffer.get_iter_at_line_offset(
                        _id, chars - 1)
                    texto = _buffer.get_text(line_iter, line_end_iter, True)
                    tabs = 0
                    if texto.startswith(self.tab):
                        tabs = len(texto.split(self.tab)) - 1
                    GLib.idle_add(self.__forzar_identacion, tabs + 1)

    def __forzar_identacion(self, tabs):
        # FIXME: Verificar esto
        _buffer = self.get_buffer()
        textmark = _buffer.get_insert()
        textiter = _buffer.get_iter_at_mark(textmark)
        _id = textiter.get_line()
        line_iter = _buffer.get_iter_at_line(_id)
        chars = line_iter.get_chars_in_line()
        _buffer.delete(line_iter,
            _buffer.get_iter_at_line_offset(_id, chars - 1))
        for tab in range(0, tabs):
            self.__identar()
        return False

    def __control_cambios(self):
        # Alerta sobre cambios externos al archivo.
        if self.archivo:
            if os.path.exists(self.archivo):
                if self.control:
                    if self.control != os.path.getmtime(self.archivo):
                        dialogo = Gtk.Dialog(parent=self.get_toplevel(),
                            flags=Gtk.DialogFlags.MODAL,
                            buttons=[
                                "Recargar", Gtk.ResponseType.ACCEPT,
                                "Continuar sin Recargar",
                                Gtk.ResponseType.CANCEL])
                        dialogo.set_border_width(15)
                        lab = "El archivo ha sido modificado "
                        lab = "%s%s" % (lab, "por otra aplicación.")
                        label = Gtk.Label(lab)
                        label.show()
                        dialogo.vbox.pack_start(label, True, True, 0)
                        response = dialogo.run()
                        dialogo.destroy()
                        if Gtk.ResponseType(response) == \
                            Gtk.ResponseType.ACCEPT:
                            self.set_archivo(self.archivo)
                        elif Gtk.ResponseType(response) == \
                            Gtk.ResponseType.CANCEL:
                            self.archivo = False
                            self.get_buffer().set_modified(True)
                else:
                    self.control = os.path.getmtime(self.archivo)
            elif not os.path.exists(self.archivo):
                dialogo = Gtk.Dialog(parent=self.get_toplevel(),
                    flags=Gtk.DialogFlags.MODAL,
                    buttons=[
                        "Guardar", Gtk.ResponseType.ACCEPT,
                        "Continuar sin Guardar", Gtk.ResponseType.CANCEL])
                dialogo.set_border_width(15)
                lab = "El archivo fue Eliminado o\n"
                lab = "%s%s" % (lab, "Movido de Lugar por Otra Oplicación.")
                label = Gtk.Label(lab)
                label.show()
                dialogo.vbox.pack_start(label, True, True, 0)
                response = dialogo.run()
                dialogo.destroy()
                if Gtk.ResponseType(response) == Gtk.ResponseType.ACCEPT:
                    self.guardar()
                elif Gtk.ResponseType(response) == Gtk.ResponseType.CANCEL:
                    self.archivo = False
                    self.get_buffer().set_modified(True)
        else:
            self.archivo = False
            self.get_buffer().set_modified(True)

    def __senialar(self, valor=False):
        # Pinta la etiqueta cuando el archivo contiene cambios sin guardar.
        scroll = self.get_parent()
        if not scroll:
            return
        notebook = scroll.get_parent()
        if not notebook:
            return
        paginas = notebook.get_n_pages()
        if not paginas:
            return
        for indice in range(paginas):
            page = notebook.get_children()[indice]
            if page == scroll:
                color = Gdk.Color(0, 0, 0)
                if valor:
                    color = Gdk.Color(65000, 26000, 0)
                pag = notebook.get_children()[indice]
                label = notebook.get_tab_label(pag).get_children()[0]
                #label.modify_fg(0, color)
                return

    def __handle(self):
        # Emite una señal con el estado general del archivo.
        self.new_handle(False)
        self.__control_cambios()

        _buffer = self.get_buffer()
        inicio, fin = _buffer.get_bounds()

        # FIXME: Verificar con Limpieza de codigo
        modificado = self.get_buffer().get_modified()
        tiene_texto = bool(self.get_buffer().get_char_count())
        texto_seleccionado = bool(_buffer.get_selection_bounds())

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard_texto = bool(clipboard.wait_for_text())

        deshacer = False
        rehacer = False
        try:
            deshacer = _buffer.can_undo()
        except:
            pass
        try:
            rehacer = _buffer.can_redo()
        except:
            pass

        renglones = self.get_buffer().get_line_count()
        caracteres = self.get_buffer().get_char_count()
        archivo = self.archivo

        _dict = {
            'modificado': modificado,
            'tiene_texto': tiene_texto,
            'texto_seleccionado': texto_seleccionado,
            'clipboard_texto': clipboard_texto,
            'deshacer': deshacer,
            'rehacer': rehacer,
            'renglones': renglones,
            'caracteres': caracteres,
            'archivo': archivo,
            }

        self.emit('update', _dict)
        self.__senialar(modificado)
        self.new_handle(True)
        return False

    def set_archivo(self, archivo):
        # Setea el archivo cuyo codigo debe mostrarse.
        self.new_handle(False)
        if archivo:
            archivo = os.path.realpath(archivo)
            if os.path.exists(archivo):
                self.archivo = archivo
                texto_file = open(self.archivo, 'r')
                texto = texto_file.read()
                texto = self.__limpiar_codigo(texto)
                texto_file.close()

                self.set_buffer(GtkSource.Buffer())
                self.get_buffer().begin_not_undoable_action()
                self.lenguaje = self.lenguaje_manager.guess_language(
                    self.archivo, "text")
                self.get_buffer().set_highlight_syntax(True)
                self.get_buffer().set_language(self.lenguaje)
                GLib.timeout_add(3, self.__force_emit_new_select)
                self.get_buffer().set_text(texto)
                self.control = os.path.getmtime(self.archivo)
        else:
            self.set_buffer(GtkSource.Buffer())
            self.get_buffer().begin_not_undoable_action()

        self.get_buffer().end_not_undoable_action()
        self.get_buffer().set_modified(False)
        # Necesario cuando se guarda cambiando el nombre del archivo.
        self.emit("update-label", self.archivo)
        self.new_handle(True)

    def guardar_archivo_como(self):
        # Abre un Filechooser para guardar como.
        parent = self.get_parent().get_parent()
        parent = parent.get_parent().get_parent()
        proyecto = parent.get_parent().proyecto
        defaultpath = BatovideWorkSpace
        if proyecto:
            defaultpath = proyecto["path"]
        filechooser = My_FileChooser(parent_window=self.get_toplevel(),
            action_type=Gtk.FileChooserAction.SAVE,
            title="Guardar Archivo Como . . .", path=defaultpath)
        filechooser.connect('load', self.__guardar_como)

    def guardar(self):
        """
        Si el archivo tiene cambios, lo guarda,
        de lo contrario ejecuta Guardar Como.
        """
        if self.archivo:
            if self.get_buffer().get_modified() and \
                os.path.exists(self.archivo):
                    self.__procesar_y_guardar()
            elif not os.path.exists(self.archivo):
                return self.guardar_archivo_como()
        else:
            return self.guardar_archivo_como()

    def set_formato(self, fuente, tamanio):
        """
        Setea el formato de la fuente. Recibe fuente o tamaño.
            fuente es: 'Monospace 10'
        """
        if not fuente or not tamanio:
            return
        self.modify_font(Pango.FontDescription("%s %s" % (fuente, tamanio)))

    def set_accion(self, accion, valor=True):
        # Ejecuta acciones sobre el código.
        _buffer = self.get_buffer()
        if accion == "Deshacer":
            if _buffer.can_undo():
                _buffer.undo()

        elif accion == "Rehacer":
            if _buffer.can_redo():
                _buffer.redo()

        elif accion == "Seleccionar Todo":
            inicio, fin = _buffer.get_bounds()
            _buffer.select_range(inicio, fin)

        elif accion == "Copiar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            if _buffer.get_selection_bounds():
                inicio, fin = _buffer.get_selection_bounds()
                texto = _buffer.get_text(inicio, fin, 0)
                clipboard.set_text(texto, -1)

        elif accion == "Pegar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            texto = clipboard.wait_for_text()
            if texto != None:
                if _buffer.get_selection_bounds():
                    start, end = _buffer.get_selection_bounds()
                    texto_seleccion = _buffer.get_text(start, end, 0)
                    _buffer.delete(start, end)
                _buffer.insert_at_cursor(texto)

        elif accion == "Cortar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            if _buffer.get_selection_bounds():
                start, end = _buffer.get_selection_bounds()
                texto_seleccion = _buffer.get_text(start, end, 0)
                _buffer.delete(start, end)
                clipboard.set_text(texto_seleccion, -1)

        elif accion == "Buscar Texto":
            try:
                inicio, fin = _buffer.get_selection_bounds()
                texto = _buffer.get_text(inicio, fin, 0)
            except:
                texto = None
            dialogo = DialogoBuscar(self, parent_window=self.get_toplevel(),
                title="Buscar Texto", texto=texto)
            dialogo.run()
            dialogo.destroy()

        elif accion == "Reemplazar Texto":
            texto = ""
            try:
                inicio, fin = _buffer.get_selection_bounds()
                texto = _buffer.get_text(inicio, fin, 0)
            except:
                texto = None
            dialogo = DialogoReemplazar(self,
                parent_window=self.get_toplevel(),
                title="Reemplazar Texto", texto=texto)
            dialogo.run()
            dialogo.destroy()

        elif accion == "Cerrar Archivo":
            if _buffer.get_modified():
                dialog = DialogoAlertaSinGuardar(
                    parent_window=self.get_toplevel())
                respuesta = dialog.run()
                dialog.destroy()
                if respuesta == Gtk.ResponseType.ACCEPT:
                    self.guardar()
                elif respuesta == Gtk.ResponseType.CANCEL:
                    return
                elif respuesta == Gtk.ResponseType.CLOSE:
                    self.__cerrar()
            else:
                self.__cerrar()

        elif accion == "Numeracion":
            self.set_show_line_numbers(valor)

        elif accion == "Identar":
            self.__identar()

        elif accion == "De Identar":
            self.__de_identar()

        elif accion == "Chequear":
            if self.lenguaje:
                if self.lenguaje.get_name() == "Python":
                    numeracion = self.get_show_line_numbers()
                    self.set_show_line_numbers(True)
                    self.get_toplevel().set_sensitive(False)
                    dialogo = DialogoErrores(self,
                        parent_window=self.get_toplevel())
                    dialogo.run()
                    dialogo.destroy()
                    self.set_show_line_numbers(numeracion)
                    self.get_toplevel().set_sensitive(True)
                    return

            dialogo = Gtk.Dialog(parent=self.get_toplevel(),
                flags=Gtk.DialogFlags.MODAL,
                buttons=["OK", Gtk.ResponseType.ACCEPT])
            dialogo.set_size_request(300, 100)
            dialogo.set_border_width(15)

            lab = "El Archivo no Contiene Código python\n"
            lab = "%s%s" % (lab, "o Todavía no ha Sido Guardado.")
            label = Gtk.Label(lab)
            label.show()

            dialogo.vbox.pack_start(label, True, True, 0)
            dialogo.run()
            dialogo.destroy()

    def marcar_error(self, linea):
        # Selecciona el error en la línea especificada.
        # FIXME: Esto no funciona en la última línea.
        if not linea > -1:
            return
        _buffer = self.get_buffer()
        start, end = _buffer.get_bounds()
        linea_iter = _buffer.get_iter_at_line(linea - 1)
        linea_iter_next = _buffer.get_iter_at_line(linea)
        _buffer.select_range(linea_iter, linea_iter_next)
        self.scroll_to_iter(linea_iter_next, 0.1, 1, 1, 0.1)

    def new_handle(self, reset):
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
        if reset:
            # FIXME: El intervalo puedes alargarlo si tu maquina es lenta.
            self.actualizador = GLib.timeout_add(1000, self.__handle)
