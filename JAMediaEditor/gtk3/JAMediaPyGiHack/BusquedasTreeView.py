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


def __check(treeview, texto, _iter):
    model = treeview.get_model()
    texto = texto.lower()
    contenido = model.get_value(_iter, 1).lower()
    if texto in contenido:
        treeview.get_selection().select_iter(_iter)
        treeview.scroll_to_cell(model.get_path(_iter))
        return True
    else:
        return False


def __buscar_delante_en_nodo(treeview, model, _iter, texto):
    if __check(treeview, texto, _iter):
        return True
    else:
        if model.iter_has_child(_iter):
            _iter = model.iter_children(_iter)
            while _iter:
                if __buscar_delante_en_nodo(treeview, model, _iter, texto):
                    return True
                _iter = model.iter_next(_iter)
    return False


def buscar_delante(treeview, texto, _iter):
    if not _iter:
        return
    model = treeview.get_model()
    texto = texto.lower()
    while _iter:
        if __buscar_delante_en_nodo(treeview, model, _iter, texto):
            return True
        _iter = model.iter_next(_iter)
    return False


def __get_ultimo(treeview, _iter):
    model = treeview.get_model()
    if not _iter:
        _iter = model.get_iter_first()
    item = _iter
    _iter = None
    while item:
        _iter = item
        item = model.iter_next(item)
    if model.iter_has_child(_iter):
        _iter = model.iter_children(_iter)
        _iter = __get_ultimo(treeview, _iter)
    return _iter


def __Buscar_detras_en_nodo(treeview, texto, _iter):
    model = treeview.get_model()
    _iter = model.iter_children(_iter)
    item = _iter
    _iter2 = None
    while item:
        _iter2 = item
        item = model.iter_next(item)
    while _iter2 :
        if model.iter_has_child(_iter2):
            if __Buscar_detras_en_nodo(treeview, texto, _iter2):
                return True
        if __check(treeview, texto, _iter2):
            return True
        _iter2 = model.iter_previous(_iter2)
    return False


def __buscar_detras(treeview, texto, _iter, child=True):
    if not _iter:
        return
    model = treeview.get_model()
    texto = texto.lower()
    while _iter:
        if model.iter_has_child(_iter) and child:
            if __Buscar_detras_en_nodo(treeview, texto, _iter):
                return True
        if __check(treeview, texto, _iter):
            return True
        _iter2 = _iter
        _iter = model.iter_previous(_iter)
        child=True
    _iter = model.iter_parent(_iter2)
    if _iter:
        if __buscar_detras(treeview, texto, _iter, child=False):
            return True
    return False


def buscar_mas(treeview, accion, texto):
    treeview.expand_all()
    model, _iter = treeview.get_selection().get_selected()
    if accion == "Buscar Siguiente":
        if not _iter:
            _iter = model.get_iter_first()
        if model.iter_has_child(_iter):
            _iter2 = model.iter_children(_iter)
            if buscar_delante(treeview, texto, _iter2):
                return True
        _iter2 = model.iter_next(_iter)
        if _iter2:
            if buscar_delante(treeview, texto, _iter2):
                return True
        _iter2 = model.iter_parent(_iter)
        if _iter2:
            if buscar_delante(treeview, texto, model.iter_next(_iter2)):
                return True
    elif accion == "Buscar Anterior":
        if _iter:
            _iter2 = model.iter_previous(_iter)
            if _iter2:
                if __buscar_detras(treeview, texto, _iter2, child=True):
                    return True
            else:
                _iter2 = model.iter_parent(_iter)
                if _iter2:
                    if __buscar_detras(treeview, texto, _iter2, child=False):
                        return True
        else:
            _iter2 = __get_ultimo(treeview, False)
            if __buscar_detras(treeview, texto, _iter2, child=True):
                return True
    return False


def __get_estructura_en_nodo(treeview, model, _iter, tab=0):
    t = "    " * tab
    text = "%s%s" % (t, model.get_value(_iter, 1))
    if model.iter_has_child(_iter):
        _iter = model.iter_children(_iter)
        while _iter:
            text = "%s\n%s" % (text, __get_estructura_en_nodo(
                treeview, model, _iter, tab+1))
            _iter = model.iter_next(_iter)
    return text


def get_estructura(treeview, model):
    text = ""
    _iter = model.get_iter_first()
    while _iter:
        if text:
            text = "%s\n%s" % (text, __get_estructura_en_nodo(
                treeview, model, _iter))
        else:
            text = "%s" % (__get_estructura_en_nodo(
                treeview, model, _iter))
        _iter = model.iter_next(_iter)
    return text
