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

home = os.environ["HOME"]

BatovideWorkSpace = os.path.join(
    home, 'BatovideWorkSpace')


class SourceView(GtkSource.View):
    """
    Visor de código para archivos abiertos.
    """

    __gtype_name__ = 'JAMediaEditorSourceView'

    __gsignals__ = {
    'update': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,))}

    def __init__(self, config):

        GtkSource.View.__init__(self)

        self.actualizador = False
        self.control = False
        self.archivo = False
        self.lenguaje = False
        self.tab = "    "

        self.set_show_line_numbers(config['numeracion'])

        self.lenguaje_manager = GtkSource.LanguageManager()

        self.lenguajes = {}
        for id in self.lenguaje_manager.get_language_ids():
            lang = self.lenguaje_manager.get_language(id)
            self.lenguajes[id] = lang.get_mime_types()

        self.set_insert_spaces_instead_of_tabs(True)
        self.set_tab_width(4)
        self.set_show_right_margin(True)
        self.set_auto_indent(True)
        self.set_smart_home_end(True)
        self.set_highlight_current_line(True)
        #self.set_accepts_tab(True)
        #self.set_pixels_above_lines(5)

        font = "%s %s" % (config['fuente'], config['tamanio'])
        self.modify_font(Pango.FontDescription(font))

        self.show_all()

        self.connect("key-press-event", self.__key_press_event)

    def set_archivo(self, archivo):
        """
        Setea el archivo cuyo codigo debe mostrarse.
        """

        if archivo:
            archivo = os.path.join(archivo.replace("//", "/"))

            if os.path.exists(archivo):
                self.archivo = archivo
                texto_file = open(self.archivo, 'r')
                texto = texto_file.read()
                texto_file.close()

                self.set_buffer(GtkSource.Buffer())
                self.get_buffer().begin_not_undoable_action()
                self.__set_lenguaje(archivo)
                self.get_buffer().set_text(texto)

                nombre = os.path.basename(self.archivo)

                if len(nombre) > 13:
                    nombre = nombre[0:13] + " . . . "

                GLib.idle_add(self.__set_label, nombre)

                self.control = os.path.getmtime(self.archivo)

        else:
            self.set_buffer(GtkSource.Buffer())
            self.get_buffer().begin_not_undoable_action()

        self.get_buffer().end_not_undoable_action()
        self.get_buffer().set_modified(False)

        # FIXME: Anular Autocompletado, no es importante.
        #completion = self.get_completion()

        #prov_words = GtkSource.CompletionWords.new(None, None)
        #prov_words.register(self.get_buffer())

        #autocompletado = AutoCompletado(
        #    self.get_buffer(), self.archivo, self)
        #completion.add_provider(autocompletado)

        #completion.set_property("remember-info-visibility", True)
        #completion.set_property("select-on-show", True)
        #completion.set_property("show-headers", True)
        #completion.set_property("show-icons", True)

    def __set_label(self, nombre):
        """
        Setea la etiqueta en notebook con el nombre del archivo.
        """

        scroll = self.get_parent()
        notebook = scroll.get_parent()

        paginas = notebook.get_n_pages()

        for indice in range(paginas):
            page = notebook.get_children()[indice]

            if page == scroll:
                pag = notebook.get_children()[indice]
                label = notebook.get_tab_label(pag).get_children()[0]
                label.set_text(nombre)

        return False

    def __set_lenguaje(self, archivo):
        """
        Setea los colores del texto según tipo de archivo.
        """

        self.lenguaje = False
        self.get_buffer().set_highlight_syntax(False)
        self.get_buffer().set_language(None)

        import mimetypes

        tipo = mimetypes.guess_type(archivo)[0]

        if tipo:
            for key in self.lenguajes.keys():
                if tipo in self.lenguajes[key]:
                    self.lenguaje = self.lenguaje_manager.get_language(key)
                    self.get_buffer().set_language(self.lenguaje)
                    self.get_buffer().set_highlight_syntax(True)
                    break

    def guardar_archivo_como(self):
        """
        Abre un Filechooser para guardar como.
        """

        parent = self.get_parent().get_parent()
        parent = parent.get_parent().get_parent()
        proyecto = parent.get_parent().proyecto

        if proyecto:
            defaultpath = proyecto["path"]

        else:
            defaultpath = BatovideWorkSpace

        from Widgets import My_FileChooser

        filechooser = My_FileChooser(
            parent_window=self.get_toplevel(),
            action_type=Gtk.FileChooserAction.SAVE,
            title="Guardar Archivo Como . . .",
            path=defaultpath)

        filechooser.connect('load', self.__guardar_como)

    def guardar(self):
        """
        Si el archivo tiene cambios, lo guarda,
        de lo contrario ejecuta Guardar Como.
        """

        if self.archivo and self.archivo != None:
            buffer = self.get_buffer()

            if buffer.get_modified() and \
                os.path.exists(self.archivo):

                self.__procesar_y_guardar()

            elif not os.path.exists(self.archivo):
                return self.guardar_archivo_como()

        else:
            return self.guardar_archivo_como()

    def __procesar_y_guardar(self):

        buffer = self.get_buffer()

        inicio, fin = buffer.get_bounds()
        texto = buffer.get_text(inicio, fin, 0)

        # Para devolver el scroll a donde estaba.
        textmark = buffer.get_insert()
        textiter = buffer.get_iter_at_mark(textmark)
        id = textiter.get_line()

        #if self.archivo.endswith(".py"):
        texto = self.__limpiar_codigo(texto)

        archivo = open(self.archivo, "w")
        archivo.write(texto)
        archivo.close()

        self.set_archivo(self.archivo)

        # Forzando actualización de Introspección.
        # FIXME: Esto debiera hacerse al cargar el archivo.
        # FIXME: Forzando Introspección.
        self.get_parent().get_parent().emit(
            'new_select', self)

        # Devolver el scroll a donde estaba.
        linea_iter = self.get_buffer().get_iter_at_line(id)
        GLib.idle_add(self.scroll_to_iter, linea_iter, 0.1, 1, 1, 0.1)

    def __limpiar_codigo(self, texto):
        """
        Cuando se guarda un archivo,
        se limpia el código en él.
        """

        limpio = ''
        for line in texto.splitlines():
            # Eliminar espacios al final de la linea.
            text_line = line.rstrip()
            # Elimina espacios en lineas vacías.
            limpio = "%s%s\n" % (limpio, text_line)

        return limpio

    def __guardar_como(self, widget, archivo):
        """
        Ejecuta guardar Como.
        """

        if archivo and archivo != None:
            archivo = os.path.join(archivo.replace("//", "/"))

            if os.path.exists(archivo):
                from Widgets import DialogoSobreEscritura

                dialog = DialogoSobreEscritura(
                    parent_window=self.get_toplevel())

                respuesta = dialog.run()
                dialog.destroy()

                if respuesta == Gtk.ResponseType.ACCEPT:
                    self.archivo = os.path.join(
                        archivo.replace("//", "/"))

                    self.__procesar_y_guardar()

                elif respuesta == Gtk.ResponseType.CANCEL:
                    return

            else:
                self.archivo = os.path.join(
                    archivo.replace("//", "/"))

                self.__procesar_y_guardar()

    def set_formato(self, fuente, tamanio):
        """
        Setea el formato de la fuente.

        Recibe fuente o tamaño.
            fuente es: 'Monospace 10'
        """

        if not fuente or not tamanio:
            return

        self.modify_font(
            Pango.FontDescription(
            "%s %s" % (fuente, tamanio)))

    def set_accion(self, accion, valor=True):
        """
        Ejecuta acciones sobre el código.
        """

        buffer = self.get_buffer()

        if accion == "Deshacer":
            if buffer.can_undo():
                buffer.undo()

        elif accion == "Rehacer":
            if buffer.can_redo():
                buffer.redo()

        elif accion == "Seleccionar Todo":
            inicio, fin = buffer.get_bounds()
            buffer.select_range(inicio, fin)

        elif accion == "Copiar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

            if buffer.get_selection_bounds():
                inicio, fin = buffer.get_selection_bounds()
                texto = buffer.get_text(inicio, fin, 0)

                clipboard.set_text(texto, -1)

        elif accion == "Pegar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            texto = clipboard.wait_for_text()

            if texto != None:
                if buffer.get_selection_bounds():
                    start, end = buffer.get_selection_bounds()
                    texto_seleccion = buffer.get_text(
                        start, end, 0)
                    buffer.delete(start, end)

                buffer.insert_at_cursor(texto)

        elif accion == "Cortar":
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

            if buffer.get_selection_bounds():
                start, end = buffer.get_selection_bounds()
                texto_seleccion = buffer.get_text(
                    start, end, 0)
                buffer.delete(start, end)
                clipboard.set_text(texto_seleccion, -1)

        elif accion == "Buscar Texto":
            try:
                inicio, fin = buffer.get_selection_bounds()
                texto = buffer.get_text(inicio, fin, 0)

            except:
                texto = None

            from Widgets import DialogoBuscar

            dialogo = DialogoBuscar(self,
                parent_window=self.get_toplevel(),
                title="Buscar Texto", texto=texto)

            dialogo.run()

            dialogo.destroy()

        elif accion == "Reemplazar Texto":

            texto = ""

            try:
                inicio, fin = buffer.get_selection_bounds()
                texto = buffer.get_text(inicio, fin, 0)

            except:
                texto = None

            from Widgets import DialogoReemplazar

            dialogo = DialogoReemplazar(self,
                parent_window=self.get_toplevel(),
                title="Reemplazar Texto", texto=texto)

            dialogo.run()

            dialogo.destroy()

        elif accion == "Cerrar Archivo":
            if buffer.get_modified():
                from Widgets import DialogoAlertaSinGuardar

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

        elif accion == "Identar con Espacios":
            # FIXME: convertir . . .
            self.tab = '    '
            #self.__identar()

        elif accion == "Identar con Tabulaciones":
            # FIXME: convertir . . .
            self.tab = '\t'
            #self.__identar()

        elif accion == "De Identar":
            self.__de_identar()

        elif accion == "Chequear":
            if self.lenguaje:
                if self.lenguaje.get_name() == "Python":
                    numeracion = self.get_show_line_numbers()
                    self.set_show_line_numbers(True)

                    # HACK: No se debe permitir usar
                    # la interfaz de la aplicación.
                    self.get_toplevel().set_sensitive(False)

                    from Widgets import DialogoErrores

                    dialogo = DialogoErrores(self,
                        parent_window=self.get_toplevel())

                    dialogo.run()
                    dialogo.destroy()

                    self.set_show_line_numbers(numeracion)

                    # HACK: No se debe permitir usar
                    # la interfaz de la aplicación.
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

    def __identar(self):
        """
        Agrega la identación especificada en el
        texto seleccionado o en la linea en que el
        usuario se encuentra parado.
        """

        buffer = self.get_buffer()

        if buffer.get_selection_bounds():
            start, end = buffer.get_selection_bounds()
            #texto = buffer.get_text(start, end, True)

            id_0 = start.get_line()
            id_1 = end.get_line()

            for id in range(id_0, id_1 + 1):
                iter = buffer.get_iter_at_line(id)
                buffer.insert(iter, self.tab)

        else:
            textmark = buffer.get_insert()
            textiter = buffer.get_iter_at_mark(textmark)
            id = textiter.get_line()
            line_iter = buffer.get_iter_at_line(id)
            buffer.insert(line_iter, self.tab)

    def __de_identar(self):
        """
        Saca una tabulación a las líneas seleccionadas o en
        la linea donde se encuentra parado el usuario.
        """

        buffer = self.get_buffer()

        if buffer.get_selection_bounds():
            start, end = buffer.get_selection_bounds()

            id_0 = start.get_line()
            id_1 = end.get_line()

            for id in range(id_0, id_1 + 1):
                line_iter = buffer.get_iter_at_line(id)
                chars = line_iter.get_chars_in_line()
                line_end_iter = buffer.get_iter_at_line_offset(id, chars - 1)

                texto = buffer.get_text(line_iter, line_end_iter, True)

                if texto.startswith(self.tab):
                    buffer.delete(line_iter,
                        buffer.get_iter_at_line_offset(id, len(self.tab)))

        else:
            textmark = buffer.get_insert()
            textiter = buffer.get_iter_at_mark(textmark)
            id = textiter.get_line()

            line_iter = buffer.get_iter_at_line(id)
            chars = line_iter.get_chars_in_line()
            line_end_iter = buffer.get_iter_at_line_offset(id, chars - 1)

            texto = buffer.get_text(line_iter, line_end_iter, True)

            if texto.startswith(self.tab):
                buffer.delete(line_iter,
                    buffer.get_iter_at_line_offset(id, len(self.tab)))

    def __cerrar(self):
        """
        Cierra la página en el Notebook_SourceView
        que contiene este sourceview.
        """

        self.get_toplevel().set_sensitive(False)

        self.new_handle(False)

        scroll = self.get_parent()
        notebook = scroll.get_parent()

        paginas = notebook.get_n_pages()

        if paginas:
            for indice in range(paginas):
                page = notebook.get_children()[indice]

                if page == scroll:
                    notebook.remove_page(indice)
                    break

    def _marcar_error(self, linea):
        """
        Selecciona el error en la línea especificada.
        """

        # FIXME: Esto no funciona en la última línea.
        if not linea > -1:
            return

        buffer = self.get_buffer()
        start, end = buffer.get_bounds()

        linea_iter = buffer.get_iter_at_line(linea - 1)
        linea_iter_next = buffer.get_iter_at_line(linea)

        #texto = buffer.get_text(linea_iter, linea_iter_next, True)

        buffer.select_range(linea_iter, linea_iter_next)
        self.scroll_to_iter(linea_iter_next, 0.1, 1, 1, 0.1)

    def __key_press_event(self, widget, event):
        """
        Tabulador Inteligente.
        """

        if event.keyval == 65421:
            buffer = self.get_buffer()

            textmark = buffer.get_insert()
            textiter = buffer.get_iter_at_mark(textmark)

            id = textiter.get_line()

            line_iter = buffer.get_iter_at_line(id)
            chars = line_iter.get_chars_in_line()

            if chars > 3:
                # Ultimo caracter.
                start_iter = buffer.get_iter_at_line_offset(id, chars - 2)
                end_iter = buffer.get_iter_at_line_offset(id, chars - 1)

                texto = buffer.get_text(start_iter, end_iter, True)

                if texto == ":":
                    # Tola la linea.
                    line_end_iter = buffer.get_iter_at_line_offset(
                        id, chars - 1)
                    texto = buffer.get_text(line_iter, line_end_iter, True)

                    tabs = 0
                    if texto.startswith(self.tab):
                        tabs = len(texto.split(self.tab)) - 1

                    GLib.idle_add(self.__forzar_identacion, tabs + 1)

    def __forzar_identacion(self, tabs):

        buffer = self.get_buffer()

        textmark = buffer.get_insert()
        textiter = buffer.get_iter_at_mark(textmark)
        id = textiter.get_line()

        line_iter = buffer.get_iter_at_line(id)
        chars = line_iter.get_chars_in_line()

        buffer.delete(line_iter,
            buffer.get_iter_at_line_offset(id, chars - 1))

        for tab in range(0, tabs):
            self.__identar()

        return False

    def __control_cambios(self):
        """
        Alerta sobre cambios externos al archivo.
        """

        if self.archivo:
            if os.path.exists(self.archivo):
                if self.control:

                    if self.control != os.path.getmtime(self.archivo):

                        dialogo = Gtk.Dialog(
                            parent=self.get_toplevel(),
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

                dialogo = Gtk.Dialog(
                    parent=self.get_toplevel(),
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

        return True

    def __senialar(self, valor=False):
        """
        Pinta la etiqueta cuando el archivo
        contiene cambios sin guardar.
        """

        color = Gdk.Color(0, 0, 0)

        if valor:
            color = Gdk.Color(65000, 26000, 0)

        scroll = self.get_parent()
        notebook = scroll.get_parent()

        paginas = notebook.get_n_pages()

        for indice in range(paginas):
            page = notebook.get_children()[indice]

            if page == scroll:
                pag = notebook.get_children()[indice]
                label = notebook.get_tab_label(pag).get_children()[0]
                label.modify_fg(0, color)
                return

    def new_handle(self, reset):

        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False

        if reset:
            self.actualizador = GLib.timeout_add(
                1000, self.__handle)

    def __handle(self):
        """
        Emite una señal con el estado general del archivo.
        """

        self.new_handle(False)

        self.__control_cambios()

        buffer = self.get_buffer()
        inicio, fin = buffer.get_bounds()

        modificado = self.get_buffer().get_modified()
        tiene_texto = bool(buffer.get_text(inicio, fin, 0))
        texto_seleccionado = bool(buffer.get_selection_bounds())

        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard_texto = bool(clipboard.wait_for_text())

        deshacer = buffer.can_undo()
        rehacer = buffer.can_redo()

        renglones = self.get_buffer().get_line_count()
        caracteres = self.get_buffer().get_char_count()
        archivo = self.archivo

        dict = {
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

        self.emit('update', dict)

        self.__senialar(modificado)

        self.new_handle(True)

        return False


class AutoCompletado(GObject.Object, GtkSource.CompletionProvider):

    __gtype_name__ = 'AutoCompletado'

    def __init__(self, buffer, archivo, parent):

        GObject.Object.__init__(self)

        self.parent = parent
        self.archivo = archivo
        self.buffer = buffer
        self.opciones = []
        self.priority = 1

        from SpyderHack.SpyderHack import SpyderHack

        self.spyder_hack = SpyderHack()

    def do_get_name(self):
        return "AutoCompletado"

    def do_populate(self, context):
        """
        Cuando se producen cambios en el buffer.

        Metodología para autocompletado:
            * Importar todos los paquetes y módulos que se están
                importando en el archivo sobre el cual estamos
                auto completando.
            * Hacer el auto completado propiamente dicho,
                trabajando sobre
                la línea de código que se está editando.
        """

        # Iterador de texto sobre el código actual.
        textiter = context.get_iter()
        indice_de_linea_activa = textiter.get_line()
        texto_de_linea_en_edicion = textiter.get_slice(
            self.buffer.get_iter_at_line(indice_de_linea_activa))

        expresion = ''
        # Auto completado se hace sobre "."
        if texto_de_linea_en_edicion.endswith("."):

            expresion = str(texto_de_linea_en_edicion.split()[-1][:-1]).strip()

            if expresion:
                # Caso: class V(Gtk.
                if "(" in expresion:
                    expresion = expresion.split("(")[-1].strip()

                lista = self.__get_list(expresion)

                opciones = []
                self.opciones = []

                for item in lista:
                    self.opciones.append(item)
                    opciones.append(
                        GtkSource.CompletionItem.new(
                            item, item, None, None))

                context.add_proposals(self, opciones, True)

        else:
            # Actualizando Autocompletado cuando está Visible.
            text = texto_de_linea_en_edicion.split(".")[-1]

            new_opciones = []
            opciones = []

            for opcion in self.opciones:
                if opcion.startswith(text):
                    new_opciones.append(opcion)
                    opciones.append(GtkSource.CompletionItem.new(
                        opcion, opcion, None, None))

            self.opciones = new_opciones
            context.add_proposals(self, opciones, True)

    def __get_list(self, expresion):
        """
        Devuelve la lista de opciones para autocompletado.
        """

        if self.archivo:
            workpath = os.path.dirname(self.archivo)

        elif self.parent.get_toplevel().base_panel.proyecto:
            workpath = self.parent.get_toplevel().base_panel.proyecto.get(
                "path", "")

        else:
            home = os.environ["HOME"]
            workpath = os.path.join(
                home, 'BatovideWorkSpace')

        return self.spyder_hack.Run(workpath, expresion, self.buffer)

GObject.type_register(AutoCompletado)
