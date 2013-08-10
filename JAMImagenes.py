#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaImagenes.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM! - Uruguay

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

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects

from JAMImagenes.JAMImagenes import JAMImagenes

class Ventana(Gtk.Window):
    
    def __init__(self):
        
        super(Ventana, self).__init__()
        
        self.set_title("JAMImagenes")
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(3)
        
        self.socket = Gtk.Socket()
        self.add(self.socket)
        self.jamediaimagenes = JAMImagenes()
        self.socket.add_id(self.jamediaimagenes.get_id())
        
        self.show_all()
        self.realize()
        
        self.connect("destroy", self.__salir)
        self.jamediaimagenes.connect("salir", self.__salir)
        
    def set_lista(self, lista):
        """
        Carga una lista de Imágenes.
        """
        
        GObject.idle_add(self.jamediaimagenes.set_lista, lista)
        
    def __salir(self, widget = None, senial = None):
        """
        Sale de la Aplicación.
        """
        
        import sys
        sys.exit(0)
    
def get_item_list(path):
    """
    Devuelve nombre y path de un archivo, para ser
    agregado como item de una lista genérica.
    """
    
    if os.path.exists(path):
        if os.path.isfile(path):
            archivo = os.path.basename(path)
            from JAMediaObjects.JAMFileSystem import describe_archivo
            if 'image' in describe_archivo(path):
                return [archivo, path]
        
    return False

if __name__ == "__main__":
    
    items = []
    
    import sys
    
    if len(sys.argv) > 1:
        
        for campo in sys.argv[1:]:
            path = os.path.join(campo)
            
            if os.path.isfile(path):
                item = get_item_list(path)
                
                if item:
                    items.append( item )
                    
            elif os.path.isdir(path):
                
                for arch in os.listdir(path):
                    newpath = os.path.join(path, arch)
                    
                    if os.path.isfile(newpath):
                        item = get_item_list(newpath)
                        
                        if item:
                            items.append( item )
                            
        if items:
            jamediaimagenes = Ventana()
            jamediaimagenes.set_lista(items)
            
        else:
            jamediaimagenes = Ventana()
        
    else:
        jamediaimagenes = Ventana()
        
    Gtk.main()
    