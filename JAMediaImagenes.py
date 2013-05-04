#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

#commands.getoutput('PATH=%s:$PATH' % (os.path.dirname(__file__)))

import JAMediaObjects
import JAMediaObjects.JAMFileSystem as JAMF

JAMediaObjectsPath = JAMediaObjects.__path__[0]

import JAMImagenes
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
        
        sys.exit(0)
    
def get_item_list(path):
    """
    Devuelve nombre y path de un archivo, para ser
    agregado como item de una lista genérica.
    """
    
    if os.path.exists(path):
        if os.path.isfile(path):
            archivo = os.path.basename(path)
            
            if 'image' in JAMF.describe_archivo(path):
                return [archivo, path]
        
    return False

if __name__ == "__main__":
    
    items = []
    
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
    