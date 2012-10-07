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
import gobject
import subprocess
import time
import gtk
import sys

#import JAMediaGlobals as G

import gdata.youtube
import gdata.youtube.service

YOUTUBE = "gdata.youtube.com"

UPDATE_TIME = 30
STDERR = "/dev/null"
#youtubedl = os.path.join(G.DIRECTORIO_BASE, "youtube-dl")

def Buscar(palabras):
    """ Recibe una cadena de texto, separa las palabras,
    busca videos que coincidan con ellas y devuelve
    un feed no mayor a 50 videos."""
    
    yt_service = gdata.youtube.service.YouTubeService()
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.feed = 'http://%s/feeds/videos' % (YOUTUBE)
    query.max_results = 50
    query.orderby = 'viewCount'
    query.racy = 'include'
    for palabra in palabras.split(" "):
        query.categories.append('/%s' % palabra.lower())
    feed = yt_service.YouTubeQuery(query)
    return DetalleFeed(feed)

def DetalleFeed(feed):
    """Recibe un feed de videos y devuelve una
    lista con diccionarios por video."""
    
    videos = []
    for entry in feed.entry:
        videos.append(DetalleVideo(entry))
    return videos

def DetalleVideo(entry):
    """Recibe un video en un feed y devuelve
    un diccionario con su información."""
    
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
'''
class JAMediaYouyubeDownload(gtk.Widget):
    """Widget para descarga de videos a través de youtube_dl."""
    
    __gsignals__ = {
        'progressdownload':(gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}
    
    def __init__(self, url, titulo):
        
        gtk.Widget.__init__(self)
        
        self.url = url
        self.titulo = self.get_titulo(titulo)
        
        self.youtubedlprocess = None
        self.salida = None
        self.actualizador = None
        self.STDOUT = "/tmp/jamediatube%d" % time.time()
        
    def get_titulo(self, titulo):
        texto = ""
        excluir = ["\\", "/", ",",".","&","¿","?","@","#","$","\'",":",";","|",
        "!", "¡","%","+","*","ª","º","~","{", "}","Ç","[","]","^","`","=","¬","\""]
        for l in titulo:
            if not l in excluir:
                texto += l
        return str(texto)
    
    def download_archivo(self):
        """Inicia la descarga de un archivo."""
        
        archivo = "%s%s%s" % ("\"", self.titulo, "\"")
        destino = os.path.join(G.DIRECTORIO_YOUTUBE, archivo)
        #estructura = "%s %s -i -R %s -f %s -w --no-part -o %s" % (youtubedl, self.url, 1, 34, destino)
        estructura = "%s %s -i -R %s -f %s --no-part -o %s" % (youtubedl, self.url, 1, 34, destino)
        self.youtubedl = subprocess.Popen(estructura, shell=True, stdout=open(self.STDOUT,"w+b"),
        stderr=open(self.STDOUT,"r+b"), universal_newlines=True)
        self.salida = open(self.STDOUT,"r")
        
        if self.actualizador: gobject.source_remove(self.actualizador)
        self.actualizador = gobject.timeout_add(UPDATE_TIME, self.get_progress)
        
    def get_progress(self):
        """Actualiza el Progreso de la descarga."""
        
        continuar = True
        line = self.salida.readline()
        if line:
            if "100.0%" in line.split(): continuar = False
        if line: self.emit_progress(line)
        return continuar
        # mensajes en los que cuelga:
        # Extracting video information
        
    def emit_progress(self, progress):
        self.emit("progressdownload", progress)
        
    def end(self):
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = None
        if self.salida: self.salida.close()
        if os.path.exists(self.STDOUT): os.unlink(self.STDOUT)
        self.youtubedl.kill()
        self.destroy()'''
        
if __name__=="__main__":
    entrada = sys.argv[1:]
    palabras = ""
    for palabra in entrada:
        palabras += "%s " % (palabra)
    videos = Buscar(palabras)
    for video in videos:
        for item in video.items():
            print item
            pass
            