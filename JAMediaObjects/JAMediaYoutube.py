#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaYoutube.py por:
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

# https://developers.google.com/youtube/1.0/developers_guide_python?hl=es#RetrievingVideos

import os

from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import GLib

YOUTUBE = "gdata.youtube.com"

STDERR = "/dev/null"
youtubedl = os.path.join(os.path.dirname(__file__), "youtube-dl")

def Buscar(palabras):
    """
    Recibe una cadena de texto, separa las palabras,
    busca videos que coincidan con ellas y devuelve
    un feed no mayor a 50 videos.
    """
    
    import gdata.youtube
    import gdata.youtube.service
    
    yt_service = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.feed = 'http://%s/feeds/videos' % (YOUTUBE)
    query.max_results = 50
    query.orderby = 'viewCount'
    query.racy = 'include'
    
    for palabra in palabras.split(" "):
        query.categories.append('/%s' % palabra.lower())
        
    try: # FIXME: Porque Falla si no hay Conexión.
        feed = yt_service.YouTubeQuery(query)
        return DetalleFeed(feed)
    
    except:
        return []

def DetalleFeed(feed):
    """
    Recibe un feed de videos y devuelve una
    lista con diccionarios por video.
    """
    
    videos = []
    
    for entry in feed.entry:
        videos.append(DetalleVideo(entry))
        
    return videos

def DetalleVideo(entry):
    """
    Recibe un video en un feed y devuelve
    un diccionario con su información.
    """
    
    metadata = entry.media.__dict__
    entrada = entry.__dict__
    
    video = {}
    
    video["id"] = entrada['_GDataEntry__id'].text
    video["titulo"] = metadata['title'].text
    video["descripcion"] = metadata['description'].text
    video["categoria"] = metadata['category'][0].text
    #video["etiquetas"] = entry.media.keywords.text
    video["url"] = metadata['player'].url.split("&")[0]
    #video["flash player"] = entry.GetSwfUrl()
    video["duracion"] = metadata['duration'].seconds
    
    try:
        previews = []
        
        for thumbnail in metadata['thumbnail']:
            tubn = [thumbnail.url, thumbnail.height, thumbnail.width]
            previews.append(tubn)
            
        video["previews"] = previews
        
    except:
        pass
    
    return video

class JAMediaYoutube(Gtk.Widget):
    """
    Widget para descarga de videos a través de youtube_dl.
    """
    
    __gsignals__ = {
    'progress_download':(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}
    
    def __init__(self):
        
        Gtk.Widget.__init__(self)
        
        self.url = False
        self.titulo = False
        self.estado = False
        
        self.youtubedl = False
        self.salida = False
        self.actualizador = False
        self.STDOUT = False
        
    def get_titulo(self, titulo):
        
        texto = ""
        excluir = ["\\", "/", ",",".","&","¿","?","@","#","$","\'",":",";","|",
        "!", "¡","%","+","*","ª","º","~","{", "}","Ç","[","]","^","`","=","¬","\""]
        
        for l in titulo:
            if not l in excluir:
                texto += l
                
        return str(texto)
    
    def download(self, url, titulo):
        """
        Inicia la descarga de un archivo.
        """
        
        import time
        import subprocess
        
        from JAMediaGlobales import get_tube_directory
        
        self.estado = True
        # http://youtu.be/XWDZMMMbvhA => codigo compartir
        # url del video => 'http://www.youtube.com/watch?v=XWDZMMMbvhA'
        # HACK: 5 de octubre 2012
        # self.url = url
        self.url = "http://youtu.be/" + url.split("http://www.youtube.com/watch?v=")[1]
        self.titulo = self.get_titulo(titulo)
        self.STDOUT = "/tmp/jamediatube%d" % time.time()
        
        archivo = "%s%s%s" % ("\"", self.titulo, "\"")
        destino = os.path.join(get_tube_directory(), archivo)
        #estructura = "%s %s -i -R %s -f %s -w --no-part -o %s" % (youtubedl, self.url, 1, 34, destino)
        estructura = "%s %s -i -R %s -f %s --no-part -o %s" % (youtubedl, self.url, 1, 34, destino)
        self.youtubedl = subprocess.Popen(estructura, shell = True, stdout = open(self.STDOUT,"w+b"),
        stderr = open(self.STDOUT,"r+b"), universal_newlines=True)
        self.salida = open(self.STDOUT,"r")
        
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
            
        self.actualizador = GLib.timeout_add(500, self.get_progress)
        
    def get_progress(self):
        """
        Actualiza el Progreso de la descarga.
        """
        
        continuar = True
        line = self.salida.readline()
        
        if line:
            if "100.0%" in line.split(): continuar = False
            
        if line: self.emit_progress(line)
        
        return continuar
    
        # mensajes en los que cuelga:
        # Extracting video information
        
    def emit_progress(self, progress):
        
        self.emit("progress_download", progress)
        
    def end(self):
        
        if self.actualizador:
            GLib.source_remove(self.actualizador)
            self.actualizador = False
            
        if self.salida: self.salida.close()
        
        if os.path.exists(self.STDOUT): os.unlink(self.STDOUT)
        
        self.youtubedl.kill()
        self.estado = False
        
if __name__=="__main__":
    
    import sys
    
    entrada = sys.argv[1:]
    palabras = ""
    
    for palabra in entrada:
        palabras += "%s " % (palabra)
        
    videos = Buscar(palabras)
    
    for video in videos:
        for item in video.items():
            print item
            
'''
Ejemplo de detalles en un video.
Corresponde a def DetalleVideo(entry)

metadata {
    'category': [<gdata.media.Category object at 0x19f8c10>],
    'extension_attributes': {},
    'title': <gdata.media.Title object at 0x19f8f10>,
    'text': None,
    'description': <gdata.media.Description object at 0x19f8d10>,
    'private': None,
    'content': [<gdata.media.Content object at 0x19f8c50>,
        <gdata.media.Content object at 0x19f8c90>,
        <gdata.media.Content object at 0x19f8cd0>],
    'credit': None,
    'player': <gdata.media.Player object at 0x19f8d90>,
    'keywords': <gdata.media.Keywords object at 0x19f8d50>,
    'extension_elements': [<atom.ExtensionElement object at 0x19f8dd0>],
    'thumbnail': [<gdata.media.Thumbnail object at 0x19f8e10>,
        <gdata.media.Thumbnail object at 0x19f8e50>,
        <gdata.media.Thumbnail object at 0x19f8e90>,
        <gdata.media.Thumbnail object at 0x19f8ed0>],
    'duration': <gdata.media.Duration object at 0x19f8f50>,
    'name': None}

entrada {
    'control': None,
    'rating': <gdata.youtube.Rating object at 0x19f8650>,
    '_GDataEntry__id': <atom.Id object at 0x19f8750>,
    'text': None,
    'contributor': [],
    'summary': None,
    'category': [<atom.Category object at 0x19f86d0>,
        <atom.Category object at 0x19f8710>],
    'statistics': <gdata.youtube.Statistics object at 0x19f8bd0>,
    'author': [<atom.Author object at 0x19f8790>],
    'media': <gdata.media.Group object at 0x19f8b50>,
    'recorded': None,
    'comments': <gdata.youtube.Comments object at 0x19f8b10>,
    'content': <atom.Content object at 0x19f87d0>,
    'source': None,
    'extension_elements': [],
    'updated': <atom.Updated object at 0x1750890>,
    'link': [<atom.Link object at 0x19f8910>,
        <atom.Link object at 0x19f8950>,
        <atom.Link object at 0x19f89d0>,
        <atom.Link object at 0x19f8a50>,
        <atom.Link object at 0x19f8a90>],
    'geo': None,
    'noembed': None,
    'extension_attributes': {},
    'rights': None,
    'title': <atom.Title object at 0x19f88d0>,
    'racy': None,
    'published': <atom.Published object at 0x1750a90>} '''
    