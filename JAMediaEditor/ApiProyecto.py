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

RECHAZAExtension = [".pyc", ".pyo", ".bak"]
RECHAZAFiles = ["proyecto.ide", ".gitignore"]
RECHAZADirs = [".git", "build", "dist"]

def colectdir(direccion, directorios):
    """
    Recolecta todos los directorios en el directorio que recibe.
    tomando en cuenta la lista de directorios a rechazar.
    """
    
    if os.path.exists(direccion) and os.path.isdir(direccion):
        
        for direct in os.listdir(direccion):
            directorio = os.path.join(direccion, direct)
            
            if os.path.isdir(directorio):
                
                leer = True
                
                ### Rechazar Directorios preestablecidos como no distribuibles.
                for dir in RECHAZADirs:
                    if dir in directorio:
                        leer = False
                        break
                    
                if leer: directorios.append(directorio)
                    
    return directorios

def colectfiles(directorio, manifest_list):
    """
    Recolecta todos los archivos en el directorio que recibe,
    tomando en cuenta la lista de extensiones a rechazar.
    """
    
    for archivo in os.listdir(directorio):
        fil = os.path.join(directorio, archivo)
        
        if os.path.isfile(fil):
            
            agregar = True
            
            ### Rechazar Archivos según nombres preestablecidos como no distribuibles.
            for file in RECHAZAFiles:
                if file in fil:
                    agregar = False
                    break
                    
            if not agregar: continue
        
            ### Rechazar Archivos según extensiones preestablecidos como no distribuibles.
            extension = os.path.splitext(os.path.split(archivo)[1])[1]
            
            for rechazar in RECHAZAExtension:
                if rechazar in extension:
                    agregar = False
                    break
                
            if agregar:
                manifest_list.append(fil)

    return manifest_list

def get_installers_data(directorio):
    """
    Devuelve la lista de archivos a escribir en MANIFEST y
    y la lista de archivos a escribir en el campo data_files de setup.py
    """
    
    raiz = directorio
    
    manifest_list = []      # La lista para MANIFEST.
    data_files = {}         # Diccionario.
    
    directorios = [raiz]
    
    ### Todos los directorios en el Proyecto.
    for directorio in directorios:
        directorios = colectdir(directorio, directorios)
        
    ### Todos los archivos en el proyecto.
    manifest_list_temp = []
    
    for directorio in directorios:
        manifest_list_temp = colectfiles(directorio, manifest_list_temp)
    
    ### Construir Lista de Archivos para MANIFEST y
    ### data_files para setup.py.
    for archivo in manifest_list_temp:
        
        filename = os.path.basename(archivo)
        parent = os.path.dirname(archivo)
        directorio = parent.split(raiz)[-1]
        
        if not data_files.get(directorio, False):
            data_files[directorio] = []
            
        item = archivo.replace("%s/" % (raiz), "")
        manifest_list.append(item)
        
        data_files[directorio].append(item)
        
    return (manifest_list, data_files)
