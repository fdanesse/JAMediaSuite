#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   BusquedasTreeView.py por:
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


def __buscar_recursivo_delante(treeview, model, _iter, texto):
    contenido = model.get_value(_iter, 1).lower()
    if texto in contenido:
        treeview.get_selection().select_iter(_iter)
        treeview.scroll_to_cell(model.get_path(_iter))
        return True
    else:
        if model.iter_has_child(_iter):
            treeview.expand_to_path(model.get_path(_iter))
            _iter = model.iter_children(_iter)
            while _iter:
                ret = __buscar_recursivo_delante(treeview, model, _iter, texto)
                if ret:
                    return ret
                _iter = model.iter_next(_iter)
    return False


def __buscar_recursivo_atras(treeview, model, _iter, texto):
    if model.iter_has_child(_iter):
        model2, _iter2 = treeview.get_selection().get_selected()
        _iter3 = model.iter_parent(_iter2)
        # valores del item analizado
        v1 = model.get_value(_iter, 1).lower()
        if _iter3:
            # valores del padre de lo seleccionado
            v11 = model2.get_value(_iter3, 1).lower()
            print 1, v1, v11
        else:
            # valores de lo seleccionado
            v11 = model2.get_value(_iter2, 1).lower()
            print 2, v1, v11
        if v1 != v11:
            treeview.expand_to_path(model.get_path(_iter))
            _iter2 = model.iter_children(_iter)
            item = _iter2
            _iter3 = None
            while item:
                _iter3 = item
                item = model.iter_next(item)
            while _iter3:
                ret = __buscar_recursivo_atras(treeview, model, _iter3, texto)
                if ret:
                    return ret
                _iter3 = model.iter_previous(_iter3)
        else:
            print 3, v1, v11
            print bool(model.iter_previous(_iter)), bool(model.iter_parent(_iter))
            '''
            1 clases clases
            3 clases clases
            False True
            '''
    contenido = model.get_value(_iter, 1).lower()
    if texto in contenido:
        treeview.get_selection().select_iter(_iter)
        treeview.scroll_to_cell(model.get_path(_iter))
        return True
    return False


def __buscar_detras(treeview, texto, _iter=False):
    model = treeview.get_model()
    texto = texto.lower()
    while _iter:
        ret = __buscar_recursivo_atras(treeview, model, _iter, texto)
        if ret:
            return ret
        _iter = model.iter_previous(_iter)
    return False


def buscar_delante(treeview, texto, _iter=False):
    model = treeview.get_model()
    texto = texto.lower()
    while _iter:
        ret = __buscar_recursivo_delante(treeview, model, _iter, texto)
        if ret:
            return ret
        _iter = model.iter_next(_iter)
    return False


def buscar_mas(treeview, accion, texto):
    model, _iter = treeview.get_selection().get_selected()
    if not _iter:
        _iter = model.get_iter_first()
    if accion == "Buscar Siguiente":
        if model.iter_has_child(_iter):
            # Si tiene hijos, buscar entre ellos
            treeview.expand_to_path(model.get_path(_iter))
            _iter2 = model.iter_children(_iter)
            ret = buscar_delante(treeview, texto, _iter2)
            if ret:
                return ret
        # Si no tiene hijos, continuar en el mismo nivel
        _iter2 = model.iter_next(_iter)
        if _iter2:
            ret = buscar_delante(treeview, texto, _iter2)
            if ret:
                return ret
        # Probablemente no hay mas iters en este nivel, buscar en el padre
        _iter2 = model.iter_parent(_iter)
        if _iter2:
            ret = buscar_delante(treeview, texto, model.iter_next(_iter2))
            if ret:
                return ret
    elif accion == "Buscar Anterior":
        _iter2 = model.iter_previous(_iter)
        if _iter2:
            ret = __buscar_detras(treeview, texto, _iter2)
            if ret:
                return ret
        _iter2 = model.iter_parent(_iter)
        if _iter2:
            ret = __buscar_detras(treeview, texto, _iter2)
            if ret:
                return ret
