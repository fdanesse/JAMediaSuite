#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaYoutube.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

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

# https://developers.google.com/youtube/1.0/developers_guide_python?hl=
# es#RetrievingVideos
# http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs

import os
import gobject
import time
import subprocess
import urllib

from Globales import get_tube_directory

BASE_PATH = os.path.dirname(__file__)
STDERR = "/dev/null"
youtubedl = os.path.join(BASE_PATH, "youtube-dl") #"/usr/bin/youtube-dl"

FEED = {
    "id": "",
    "titulo": "",
    "descripcion": "",
    "categoria": "",
    "url": "",
    "duracion": 0,
    "previews": ""
    }

CODECS = [
    [43, "WebM", "360p VP8 N/A 0.5 Vorbis 128"],
    [5, "FLV", "240p Sorenson H.263    N/A    0.25 MP3 64"],
    [18, "MP4", "270p/360p H.264 Baseline 0.5 AAC 96"],
    [82, "MP4", "360p H.264 3D 0.5 AAC 96"],
    ]


class Buscar(gobject.GObject):

    __gsignals__ = {
    'encontrado': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, gobject.TYPE_STRING)),
    'end': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}

    def __init__(self, ):

        gobject.GObject.__init__(self)

    def __get_videos(self, consulta, limite):
        # Obtener web principal con resultado de busqueda y recorrer todas
        # las pags de la busqueda obtenida hasta conseguir el id de los videos.
        params = urllib.urlencode({'search_query': consulta})
        urls = {}
        print "Comezando la búsqueda de %i videos sobre %s" % (limite, consulta)
        for pag in range(1, 10):
            f = urllib.urlopen("http://www.youtube.com/results?%s&filters=video&page=%i" % (params, pag))
            text = f.read().replace("\n", "")
            f.close()
            for item in text.split("data-context-item-id=")[1:]:
                _id = item.split("\"")[1].strip()
                url = "http://www.youtube.com/watch?v=%s" % _id
                if not _id in urls.keys():
                    urls[_id] = {"url": url}
                    self.emit("encontrado", _id, url)
                if len(urls.keys()) >= limite:
                    break
            if len(urls.keys()) >= limite:
                break
        print "Búsqueda finalizada para:", consulta, "Videos encontrados:", len(urls.keys())
        self.emit("end")

    def buscar(self, palabras, cantidad):
        buscar = ""
        for palabra in palabras.split(" "):
            buscar = "%s%s+" % (buscar, palabra.lower())
        if buscar.endswith("+"):
            buscar = str(buscar[:-1])
        try:  # FIXME: Porque falla si no hay Conexión.
            if buscar:
                self.__get_videos(buscar, cantidad)
        except:
            pass


class JAMediaYoutube(gobject.GObject):

    __gsignals__ = {
    'progress_download': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gobject.GObject.__init__(self)

        self.ultimosdatos = False
        self.contador = 0
        self.datos_originales = [False, False]

        self.url = False
        self.titulo = False
        self.estado = False

        self.youtubedl = False
        self.salida = False
        self.actualizador = False
        self.STDOUT = False

        self.codec = 0

    def __get_titulo(self, titulo):
        texto = ""
        excluir = ["\\", "/", ",", ".", "&",
        "¿", "?", "@", "#", "$", "\'", ":", ";", "|",
        "!", "¡", "%", "+", "*", "ª", "º", "~", "{",
        "}", "Ç", "[", "]", "^", "`", "=", "¬", "\""]
        for l in titulo:
            if not l in excluir:
                texto += l
        return str(texto).replace(" ", "_")

    def __get_progress(self):
        """
        Actualiza el Progreso de la descarga.
        """
        progress = self.salida.readline()
        if progress:
            if "100.0%" in progress.split():
                self.estado = False
            self.emit("progress_download", progress)

        # control switch codec.
        if self.ultimosdatos != progress:
            self.ultimosdatos = progress
            self.contador = 0
        else:
            self.contador += 1

        if self.contador > 15:
            if self.codec + 1 < len(CODECS):
                self.end()
                self.codec += 1
                url, titulo = self.datos_originales
                self.download(url, titulo)
        return self.estado

    def download(self, url, titulo):
        """
        Inicia la descarga de un archivo.
        """
        self.datos_originales = [url, titulo]

        self.ultimosdatos = False
        self.contador = 0

        #print "Intentando Descargar:", titulo
        #print "\t En Formato:", CODECS[self.codec]

        self.estado = True
        # http://youtu.be/XWDZMMMbvhA => codigo compartir
        # url del video => 'http://www.youtube.com/watch?v=XWDZMMMbvhA'
        # FIXME: HACK: 5 de octubre 2012
        #self.url = url # https://youtu.be/wgdbZhnFD5g #https://www.youtube.com/watch?t=187&v=wgdbZhnFD5g
        #self.url = "http://youtu.be/" + url.split(
        #    "http://www.youtube.com/watch?v=")[1]
        self.url = "http://youtu.be/" + url.split("=")[1]
        self.titulo = self.__get_titulo(titulo)
        self.STDOUT = "/tmp/jamediatube%d" % time.time()

        archivo = "%s%s%s" % ("\"", self.titulo, "\"")
        destino = os.path.join(get_tube_directory(), archivo)

        estructura = "python %s %s -i -R %s -f %s --no-part -o %s" % (
            youtubedl, self.url, 1, CODECS[self.codec][0], destino)

        self.youtubedl = subprocess.Popen(estructura, shell=True,
            stdout=open(self.STDOUT, "w+b"), stderr=open(self.STDOUT, "r+b"),
            universal_newlines=True)

        self.salida = open(self.STDOUT, "r")

        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False

        self.actualizador = gobject.timeout_add(500, self.__get_progress)

    def reset(self):
        self.end()
        self.codec = 0

    def end(self):
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False
        self.youtubedl.kill()
        if self.salida:
            self.salida.close()
        if os.path.exists(self.STDOUT):
            os.unlink(self.STDOUT)
        self.estado = False
