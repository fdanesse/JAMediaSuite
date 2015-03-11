#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ApiProyecto.py por:
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

RECHAZAExtension = [".pyc", ".pyo", ".bak", ".ide", ".gitignore", ".git"]
RECHAZAFiles = ["proyecto.ide", ".gitignore"]
RECHAZADirs = [".git", "build", "dist"]


def __colectdir(direccion, directorios):
    """
    Recolecta todos los directorios en el directorio que recibe.
    tomando en cuenta la lista de directorios a rechazar.
    """
    if os.path.exists(direccion) and os.path.isdir(direccion):
        os.chmod(direccion, 0755)
        for direct in os.listdir(direccion):
            directorio = u'%s'.encode('utf8') % os.path.join(direccion, direct)
            if os.path.isdir(directorio):
                leer = True
                # Rechazar Directorios preestablecidos como no distribuibles.
                for _dir in RECHAZADirs:
                    if _dir in directorio:
                        leer = False
                        break
                if leer:
                    os.chmod(directorio, 0755)
                    directorios.append(directorio)
                else:
                    commands.getoutput('rm -r \"%s\"' % directorio)
    return directorios


def __colectfiles(directorio, manifest_list):
    """
    Recolecta todos los archivos en el directorio que recibe,
    tomando en cuenta la lista de extensiones a rechazar.
    """
    for archivo in os.listdir(directorio):
        fil = u'%s'.encode('utf8') % os.path.join(directorio, archivo)
        if os.path.isfile(fil):
            agregar = True
            # Rechazar Archivos según nombres preestablecidos
            for _file in RECHAZAFiles:
                if _file in fil:
                    agregar = False
                    break
            if not agregar:
                os.remove(fil)
                continue
            # Rechazar Archivos según extensiones preestablecidos
            extension = os.path.splitext(os.path.split(archivo)[1])[1]
            for rechazar in RECHAZAExtension:
                if rechazar in extension:
                    agregar = False
                    break
            if agregar:
                os.chmod(fil, 0644)
                manifest_list.append(fil)
            else:
                os.remove(fil)
    return manifest_list


def get_installers_data(directorio):
    """
    Devuelve la lista de archivos a escribir en MANIFEST y
    y la lista de archivos a escribir en el campo data_files de setup.py
    Además, establece los permisos 755 para directorios y 644 para archivos y
    borra directorios y archivos no deseados.
    """
    raiz = u'%s'.encode('utf8') % directorio
    manifest_list = []      # La lista para MANIFEST.
    data_files = {}         # Diccionario.
    directorios = [raiz]
    # Todos los directorios en el Proyecto.
    for directorio in directorios:
        directorios = __colectdir(directorio, directorios)
    # Todos los archivos en el proyecto.
    manifest_list_temp = []
    for directorio in directorios:
        manifest_list_temp = __colectfiles(directorio, manifest_list_temp)
    # Construir Lista de Archivos para MANIFEST y
    # data_files para setup.py.
    for archivo in manifest_list_temp:
        parent = os.path.dirname(archivo)
        directorio = parent.split(raiz)[-1]
        if not data_files.get(directorio, False):
            data_files[directorio] = []
        item = archivo.replace("%s/" % (raiz), "")
        manifest_list.append(item)
        data_files[directorio].append(item)
    return (manifest_list, data_files)
