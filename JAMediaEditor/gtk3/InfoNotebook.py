#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   InfoNotebook.py por:
#       Cristian García     <cristian99garcia@gmail.com>
#       Ignacio Rodriguez   <nachoel01@gmail.com>
#       Flavio Danesse      <fdanesse@gmail.com>

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
import commands
from collections import OrderedDict
#import shutil
import shlex

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib

#from Widgets2 import Estructura_Menu
#from Widgets2 import DialogoEliminar
#from Widgets2 import BusquedaGrep
#from JAMediaPyGiHack.BusquedasTreeView import buscar_delante
from JAMediaPyGiHack.BusquedasTreeView import buscar_mas
from JAMediaPyGiHack.BusquedasTreeView import get_estructura


def get_contenido_python(texto):
    _dict = OrderedDict()
    bloqueo = False
    lineas = texto.splitlines()
    contador = -1
    buscar = ["class", "def", "import", "from"]
    for linea in lineas:
        temp = linea.strip()
        contador += 1
        if temp:
            if temp.startswith("\'\'\'") or \
                temp.startswith("\"\"\"") or \
                temp.endswith("\'\'\'") or \
                temp.endswith("\"\"\""):
                bloqueo = bool(not bloqueo)
                continue
            if bloqueo:
                continue
            try:
                items = list(shlex.shlex(temp))
                if items:
                    if items[0] in buscar:
                        l = linea.strip().split(":")[0]
                        if items[0] == "class" or items[0] == "def":
                            l = "%s:" % l
                        _dict[str(contador)] = l
            except:
                print "Error:", get_contenido_python, temp
    return _dict


def get_contenido_vala(texto):
    _dict = OrderedDict()
    bloqueo = False
    lineas = texto.splitlines()
    contador = -1
    buscar = ["public", "private", "protected", "internal", "using"]
    # FIXME: verificar casos: public abstract class Animal : Object {
    for linea in lineas:
        temp = linea.strip()
        contador += 1
        if temp:
            if temp.startswith("//"):
                continue
            if temp.startswith("/*"):
                bloqueo = True
                continue
            if temp.startswith("*/"):
                bloqueo = False
                continue
            if bloqueo:
                continue
            try:
                items = list(shlex.shlex(temp))
                if items:
                    if not "signal" in items and items[0] in buscar and not "=" in items:
                        if "{" in linea:
                            linea = linea.split("{")[0]
                        if ";" in linea:
                            linea = linea.split(";")[0]
                        _dict[str(contador)] = linea
            except:
                print "Error:", get_contenido_vala, temp
    return _dict


class InfoNotebook(Gtk.Notebook):
    """
    Notebook Izquierdo, para introspección y Estructura de proyecto.
    """

    __gtype_name__ = 'JAMediaEditorInfoNotebook'

    __gsignals__ = {
    'new_select': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,
        GObject.TYPE_STRING)),
    'open': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
    'search_on_grep': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,
        GObject.TYPE_PYOBJECT)),
    'remove_proyect': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Notebook.__init__(self)

        self.accion_instrospeccion = []
        self.copy_cut = []
        self.path_actual = False

        self.estructura_proyecto = Estructura_Proyecto()
        self.introspeccion = Introspeccion()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.introspeccion)
        self.append_page(scroll, Gtk.Label("Introspección"))

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.estructura_proyecto)
        self.append_page(scroll, Gtk.Label("Proyecto"))

        self.show_all()

        self.introspeccion.connect("new_select", self.__re_emit_new_select)
        # FIXME: La Interfaz se cuelga
        #self.estructura_proyecto.connect("button-press-event",
        #    self.__click_derecho_en_estructura)
        self.estructura_proyecto.connect("open", self.__re_emit_open)

    '''
    def __click_derecho_en_estructura(self, widget, event):
        """
        Abrir un menu de opciones cuando el usuario hace click derecho sobre
        un elemento en la Introspección.
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
        if boton == 3:
            menu = Estructura_Menu(widget, boton, pos, tiempo,
                path, widget.get_model(), self.accion_instrospeccion)
            menu.connect('accion', self.__set_accion_estructura)
            menu.popup(None, None, None, None, boton, tiempo)

    def __set_accion_estructura(self, widget, lista, accion, iter):
        """
        Responde a la seleccion del usuario sobre el menu
        que se despliega al hacer click derecho sobre un elemento
        en la estructura del proyecto.
        """
        self.accion_instrospeccion = [accion, iter]
        filepath = lista.get_model().get_value(iter, 2)

        if accion == "abrir":
            self.copy_cut = []
            self.__re_emit_open(None, filepath)

        elif accion == "copiar":
            self.copy_cut = [accion, iter]

        elif accion == "cortar":
            self.copy_cut = [accion, iter]

        elif accion == "pegar":
            path = lista.get_model().get_value(self.copy_cut[1], 2)
            if path != filepath and \
                not os.path.basename(path) in os.listdir(filepath):
                expresion = ""
                if os.path.isdir(path):
                    expresion = "cp -r \"" + path + "\" \"" + filepath + "\""
                elif os.path.isfile(path):
                    expresion = "cp \"" + path + "\" \"" + filepath + "\""
                os.system(expresion)
                if "cortar" in self.copy_cut[0]:
                    if os.path.isdir(path):
                        shutil.rmtree("%s" % (os.path.join(path)))
                    elif os.path.isfile(path):
                        os.remove("%s" % (os.path.join(path)))
                self.copy_cut = []
                self.set_path_estructura(self.path_actual)
            else:
                dialogo = Gtk.Dialog(parent=self.get_toplevel(),
                    flags=Gtk.DialogFlags.MODAL,
                    buttons=["OK", Gtk.ResponseType.ACCEPT])
                dialogo.set_size_request(300, 100)
                dialogo.set_border_width(15)
                text = ""
                if path == filepath:
                    text = "No se Puede Pegar aquí"
                    text = "%s%s" % (
                        text, ", Origen y Destino son Iguales.")
                elif os.path.basename(path) in os.listdir(filepath):
                    text = "No se Puede Pegar aquí, Ya hay un\n"
                    text = "%s%s" % (
                        text, "Archivo con el Mismo Nombre en el Destino.")
                label = Gtk.Label(text)
                label.show()
                dialogo.vbox.pack_start(label, True, True, 0)
                dialogo.run()
                dialogo.destroy()

        elif accion == "suprimir" or accion == "eliminar proyecto":
            tipo = ""
            self.copy_cut = []
            if os.path.isdir(filepath):
                tipo = "Directorio"
                text = "Directorio"
            elif os.path.isfile(filepath):
                tipo = "Archivo"
                text = "Archivo"
            if accion == "eliminar proyecto":
                text = "Proyecto"
            dialogo = DialogoEliminar(tipo=text,
                parent_window=self.get_toplevel())
            resp = dialogo.run()
            dialogo.destroy()
            if resp == Gtk.ResponseType.ACCEPT:
                if tipo == "Directorio":
                    shutil.rmtree("%s" % (os.path.join(filepath)))
                elif tipo == "Archivo":
                    os.remove("%s" % (os.path.join(filepath)))
                lista.get_model().remove(iter)
                if accion == "eliminar proyecto":
                    self.emit("remove_proyect")

        elif accion == "buscar":
            self.copy_cut = []
            dialogo = BusquedaGrep(path=filepath,
                parent_window=self.get_toplevel())
            dialogo.connect("nueva-seleccion", self.__seleccion_in_grep)
            dialogo.run()
            dialogo.destroy()

        elif accion == "Crear Directorio":
            dialog = Gtk.Dialog("Crear Directorio . . .",
                self.get_toplevel(), Gtk.DialogFlags.MODAL, None)
            etiqueta = Gtk.Label("Nombre del Directorio: ")
            entry = Gtk.Entry()
            etiqueta.show()
            entry.show()
            dialog.vbox.pack_start(etiqueta, True, True, 5)
            dialog.vbox.pack_start(entry, True, True, 5)
            dialog.add_button("Crear Directorio", Gtk.ResponseType.ACCEPT)
            dialog.add_button("Cancelar", Gtk.ResponseType.CANCEL)
            resp = dialog.run()
            if resp == Gtk.ResponseType.ACCEPT:
                self.copy_cut = []
                filepath = lista.get_model().get_value(iter, 2)
                directorio_nuevo = os.path.join(filepath, entry.get_text())
                if directorio_nuevo != "" and directorio_nuevo != None:
                    try:
                        expresion = 'mkdir \"%s\"' % directorio_nuevo
                        os.system(expresion)
                        self.set_path_estructura(self.path_actual)
                    except:
                        pass
            dialog.destroy()
        else:
            print accion

    def __seleccion_in_grep(self, widget, valor):
        # Cuando se hace doble click en una linea de la búsqueda grep.
        self.emit("search_on_grep", valor, widget)
    '''

    def __re_emit_open(self, widget, filepath):
        # Manda abrir un archivo segun filepath.
        self.emit("open", filepath)

    def __re_emit_new_select(self, widget, index, texto):
        """
        Emite la señal new_select cuando se hace doble
        click sobre una fila en la instrospeccion.
        """
        self.emit('new_select', index, texto)

    def set_path_estructura(self, path):
        # Setea estructura de directorios y archivos del proyecto según path.
        self.estructura_proyecto.set_path_estructura(path)
        self.path_actual = path

    def set_introspeccion(self, nombre, texto, view, tipo):
        # Recibe nombre y contenido de archivo para realizar introspeccion.
        if len(nombre) > 15:
            nombre = str(nombre[0:16]) + " . . . "
        self.set_tab_label_text(self.get_nth_page(0), nombre)
        self.introspeccion.set_introspeccion(nombre, texto, view, tipo)

    def buscar_mas(self, accion, texto):
        self.get_nth_page(self.get_current_page(
            )).get_child().buscar_mas(accion, texto)

    def get_estructura(self):
        return self.get_nth_page(
            self.get_current_page()).get_child().get_estructura()


class Introspeccion(Gtk.TreeView):
    """
    TreeView para la Introspección
    """

    __gtype_name__ = 'JAMediaEditorIntrospeccion'

    __gsignals__ = {
    'new_select': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_INT,
        GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.TreeStore(GObject.TYPE_INT,
            GObject.TYPE_STRING, Gdk.Color))

        self._dict = {}

        self.__set_columnas()
        self.connect("key-press-event", self.key_press_event)
        self.set_rules_hint(True)
        self.set_property("enable-tree-lines", True)
        self.set_headers_visible(False)
        self.show_all()

    def __append(self, _iter, key, color, texto):
        new_iter = self.get_model().append(_iter, [int(key), texto, color])
        return new_iter

    def __get_datos_introspeccion(self, texto, tipo):
        _dict = OrderedDict()
        if tipo == "python":
            _dict = get_contenido_python(texto)
        elif tipo == "vala":
            _dict = get_contenido_vala(texto)
        else:
            print "FIXME: Introspección no implementada para:", tipo
        return _dict

    def __set_columnas(self):
        # Crea y agrega las columnas.
        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Indice', render, text=0)
        columna.set_property('visible', False)
        columna.set_property('resizable', False)
        self.append_column(columna)

        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('Datos', render, text=1)
        columna.add_attribute(render, 'foreground-gdk', 2)
        columna.set_property('visible', True)
        columna.set_property('resizable', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

    def buscar_mas(self, accion, texto):
        buscar_mas(self, accion, texto)

    def do_row_activated(self, path, column):
        # Emite la señal new_select cuando se hace doble click sobre una fila
        self.expand_to_path(path)
        _iter = self.get_model().get_iter(path)
        index = self.get_model().get_value(_iter, 0)
        texto = self.get_model().get_value(_iter, 1)
        texto = texto.split(":")[0]
        self.emit('new_select', index, texto)

    def set_introspeccion(self, nombre, texto, view, tipo):
        # Recibe nombre y contenido de archivo para realizar introspeccion.
        if self.get_model():
            self._dict = {}
            self.get_model().clear()
        else:
            return
        if not texto:
            return
        self._dict = self.__get_datos_introspeccion(texto, tipo)
        iterbase = self.get_model().get_iter_first()
        new_class = iterbase
        new_funcion = iterbase
        if tipo == "python":
            for key in self._dict.keys():
                temp = self._dict[key].strip()
                items = list(shlex.shlex(temp))
                if "class" in items:
                    color = Gdk.color_parse("#a40000")
                    new_class = self.__append(iterbase, key, color, temp)
                    new_funcion = new_class
                elif "import" in items:
                    color = Gdk.color_parse("#006e00")
                    self.__append(new_funcion, key, color, temp)
                else:  #"def" in items
                    color = Gdk.color_parse("#000091")
                    new_funcion = self.__append(new_class, key, color, temp)
        elif tipo == "vala":
            for key in self._dict.keys():
                temp = self._dict[key].strip()
                items = list(shlex.shlex(temp))
                if "class" in items:
                    color = Gdk.color_parse("#a40000")
                    new_class = self.__append(iterbase, key, color, temp)
                    new_funcion = new_class
                elif "using" in items:
                    color = Gdk.color_parse("#006e00")
                    self.__append(new_funcion, key, color, temp)
                else:
                    color = Gdk.color_parse("#000091")
                    new_funcion = self.__append(new_class, key, color, temp)
        else:
            #print "FIXME: Completar Introspección para otros lenguajes"
            pass
        GLib.idle_add(self.expand_all)

    def key_press_event(self, widget, event):
        # Funciones adicionales para moverse en el TreeView
        tecla = event.keyval
        model, _iter = self.get_selection().get_selected()
        if _iter is None:
            return
        path = self.get_model().get_path(_iter)
        if tecla == 65293:
            if self.row_expanded(path):
                self.collapse_row(path)
            else:
                self.expand_to_path(path)
        elif tecla == 65361:
            if self.row_expanded(path):
                self.collapse_row(path)
                return False
            len_max = len(str(path).split(":"))
            if len_max > 1:
                path = str(path).split(":")
                path_str = ""
                for x in path:
                    if path_str != "":
                        path_str = path_str + ":" + x
                    else:
                        path_str = x
                n = len(path[len(path) - 1]) + 1
                path_str = path_str[:-n]
                try:
                    new_path = Gtk.TreePath.new_from_string(path_str)
                    _iter = self.get_model().get_iter(new_path)
                    self.get_selection().select_iter(_iter)
                    self.scroll_to_cell(new_path)
                except:
                    return False
            else:
                _iter = self.get_model().get_iter_first()
                self.get_selection().select_iter(_iter)
                new_path = model.get_path(_iter)
                self.scroll_to_cell(new_path)
        elif tecla == 65363:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        else:
            pass
        return False

    def get_estructura(self):
        return get_estructura(self, self.get_model())


class Estructura_Proyecto(Gtk.TreeView):
    """
    TreeView para la estructura del proyecto.
    """

    __gtype_name__ = 'JAMediaEditorEstructura_Proyecto'

    __gsignals__ = {
    'open': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}

    def __init__(self):

        Gtk.TreeView.__init__(self, Gtk.TreeStore(GObject.TYPE_STRING,
            GObject.TYPE_STRING, GObject.TYPE_STRING))

        self.set_property("rules-hint", True)
        self.set_property("enable-tree-lines", True)
        self.__set_columnas()
        self.set_headers_visible(False)

        self.connect("key-press-event", self.__key_press_event)
        self.show_all()

    def __set_columnas(self):
        # Crea y agrega las columnas al TreeView.
        render = Gtk.CellRendererPixbuf()
        columna = Gtk.TreeViewColumn('pixbuf', render, stock_id=0)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('text', render, text=1)
        columna.set_property('resizable', False)
        columna.set_property('visible', True)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

        render = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn('text', render, text=2)
        columna.set_property('resizable', False)
        columna.set_property('visible', False)
        columna.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        self.append_column(columna)

    def __load_estructura(self, estructura):
        """
        Función Recursiva que agrega directorios y
        archivos al modelo, según "estructura".
        estructura es:
            una lista de tuplas que contienen:
                (directorio, path en el modelo donde debe agregarse).
        """
        if not estructura:
            self.expand_all()
            return False

        item = estructura[0]
        directorio, path = item
        estructura.remove(estructura[0])

        # Establecer el iter donde debe agregarse el item
        if path:
            _iter = self.get_model().get_iter(path)
        else:
            _iter = self.get_model().get_iter_first()

        # Leer archivos y directorios en este nivel
        archivos = []
        dir_list = os.listdir(directorio)
        dir_list.sort()

        for archivo in dir_list:
            if archivo.endswith(".ide") or \
                archivo.endswith(".bak") or \
                archivo.endswith(".pyc") or \
                archivo.endswith(".pyo") or \
                archivo == ".git" or \
                archivo == "build" or \
                archivo == "dist":
                    continue
            direccion = os.path.join(directorio, archivo)
            # Si es un directorio, se agrega y se guarda
            # en una lista para hacer recurrencia sobre esta función.
            if os.path.isdir(direccion):
                iteractual = self.get_model().append(
                    _iter, [Gtk.STOCK_DIRECTORY, archivo, direccion])
                # Para Recursividad.
                estructura.append((direccion,
                    self.get_model().get_path(iteractual)))
            # Si es un archivo.
            elif os.path.isfile(direccion):
                archivos.append(direccion)

        # Agregar todos los archivos en este nivel.
        for x in archivos:
            self.get_model().append(
                _iter, [Gtk.STOCK_FILE, os.path.basename(x), x])

        # Recursividad en la función.
        self.__load_estructura(estructura)
        return False

    def __key_press_event(self, widget, event):
        # Funciones adicionales para moverse en el TreeView
        tecla = event.keyval
        model, _iter = self.get_selection().get_selected()
        if _iter is None:
            return
        path = self.get_model().get_path(_iter)
        if tecla == 65293:
            if self.row_expanded(path):
                self.collapse_row(path)
            else:
                self.expand_to_path(path)
        elif tecla == 65361:
            if self.row_expanded(path):
                self.collapse_row(path)
                return False
            len_max = len(str(path).split(":"))
            if len_max > 1:
                path = str(path).split(":")
                path_str = ""
                for x in path:
                    if path_str != "":
                        path_str = path_str + ":" + x
                    else:
                        path_str = x
                n = len(path[len(path) - 1]) + 1
                path_str = path_str[:-n]
                try:
                    new_path = Gtk.TreePath.new_from_string(path_str)
                    _iter = self.get_model().get_iter(new_path)
                    self.get_selection().select_iter(_iter)
                    self.scroll_to_cell(new_path)
                except:
                    return False
            else:
                _iter = self.get_model().get_iter_first()
                self.get_selection().select_iter(_iter)
                path = model.get_path(iter)
                self.scroll_to_cell(path)
        elif tecla == 65363:
            if not self.row_expanded(path):
                self.expand_to_path(path)
        else:
            pass
        return False

    def buscar_mas(self, accion, texto):
        buscar_mas(self, accion, texto)

    def set_path_estructura(self, path):
        # Carga la estructura de directorios y archivos del proyecto.
        if self.get_model():
            self.get_model().clear()
        else:
            return
        if not path:
            return
        _iter = self.get_model().get_iter_first()
        self.get_model().append(_iter, [Gtk.STOCK_DIRECTORY,
            os.path.basename(path), path])
        estructura = []
        estructura.append((path, None))
        self.__load_estructura(estructura)

    def do_row_activated(self, path, column):
        # Cuando se hace doble click sobre una fila
        _iter = self.get_model().get_iter(path)
        direccion = self.get_model().get_value(_iter, 2)
        direccion = os.path.realpath(direccion)
        if os.path.isdir(direccion):
            if self.row_expanded(path):
                self.collapse_row(path)
            else:
                self.expand_to_path(path)
        elif os.path.isfile(direccion):
            datos = commands.getoutput(
                'file -ik %s%s%s' % ("\"", direccion, "\""))
            if "text" in datos or "x-python" in datos or \
                "x-empty" in datos or "svg+xml" in datos:
                self.emit('open', direccion)

    def get_estructura(self):
        return get_estructura(self, self.get_model())
