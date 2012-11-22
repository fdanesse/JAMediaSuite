#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   MplayerReproductor.py por:
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

import time
import os
import subprocess

import gi
from gi.repository import GObject

STDOUT = "/tmp/mplayerout%d" % time.time()
MPLAYER = "mplayer"

class MplayerReproductor(GObject.GObject):
    """
    Reproductor de Audio, Video y Streaming de
    Radio y Television. Implementado sobre:
        
        python 2.7.3
        Gtk 3
        mplayer (a traves de python.subprocess)
    """
    
    __gsignals__ = {
    "endfile":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    "estado":(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_STRING,)),
    "newposicion":(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_INT,)),
    "volumen":(GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE,
        (GObject.TYPE_FLOAT,))}
    
    # Estados: playing, paused, None
    
    def __init__(self, ventana_id):
        """ Recibe el id de un DrawingArea
        para mostrar el video. """
        
        GObject.GObject.__init__(self)
        
        self.name = "MplayerReproductor"
        self.ventana_id = ventana_id
        self.mplayer = None
        self.salida = None
        self.entrada = None
        self.estado = None
        self.duracion = 0
        self.posicion = 0
        self.volumen = 0
        self.actualizador = None
        self.uri = None
        
        self.config = {
            'saturacion': 0,
            'contraste': 0,
            'brillo': 0,
            'hue': 0,
            'gamma': 0
            }
            
    def stop(self):
        """Detiene todo."""
        
        try:
            if self.entrada:
                self.entrada.write('%s 0\n' % "quit")
                self.entrada.flush()
                self.new_handle(False)
                
        except Exception, e:
            #print "HA OCURRIDO UN ERROR EN QUIT DEL REPRODUCTOR", e
            pass
        
        self.posicion = 0
        if os.path.exists(STDOUT): os.unlink(STDOUT)
        self.estado = None
        self.emit("estado", "None")

    def load(self, uri):
        """Carga y Reproduce un archivo o streaming."""
        
        self.stop()
        self.uri = uri
        if os.path.exists(self.uri):
            uri = "%s%s%s" % ("\"", self.uri, "\"")
        
        cache_pantalla = "%s -cache %i -wid %i" % (MPLAYER, 1024, self.ventana_id)
        estructura = "%s -slave -idle -nolirc -rtc -nomouseinput -noconsolecontrols -nojoystick" % (cache_pantalla)
        self.mplayer = subprocess.Popen(estructura, shell = True, stdin = subprocess.PIPE,
            stdout = open(STDOUT,"w+b"), stderr=open(STDOUT,"r+b"), universal_newlines=True)
        self.entrada = self.mplayer.stdin
        self.salida = open(STDOUT,"r")
        self.entrada.write("loadfile %s 0\n" % uri)
        self.entrada.flush()
        self.new_handle(True)
        
    def handle(self):
        """Consulta el estado y progreso del
        la reproduccion actual."""
        
        if not self.entrada.closed:
            # Control por tiempo
            #self.entrada.write("%s 0\n" % ("get_time_length"))
            #self.entrada.flush()
            #duracion = self.salida.readline()
            #if "ANS_LENGTH" in duracion:
            #    duracion = float(duracion.split("=")[1]) # Duración en Segundos
            #    print "dur", duracion
                
            #self.entrada.write("%s 0\n" % ("get_time_pos"))
            #self.entrada.flush()
            #posicion = self.salida.readline()
            #if "ANS_TIME_POSITION" in posicion:
            #    posicion = float(posicion.split("=")[1]) # Posición en Segundos
            #    print "pos", posicion
            
            self.entrada.write("%s 0\n" % ("get_property percent_pos"))
            self.entrada.flush()
            linea = self.salida.readline()
            
            if linea:
                if "ANS_percent_pos" in linea:
                    "Información sobre el porcentaje Reproducido hasta el momento. Ejemplo:"
                    "ANS_percent_pos=0"
                    self.get_progress_in_mplayer(linea)
                    self.get_volumen()
                    
                elif "Video: no video" in linea or "Audio only file format detected" in linea:
                    "Cuando no hay video en la fuente. Ejemplo"
                    "Audio only file format detected."
                    "Video: no video"
                    #self.emit("video", False)
                    pass
                
                elif "Cache" in linea:
                    "Información Sobre Carga de caché. Ejemplo:"
                    "Cache fill:  6.25% (65536 bytes)"
                    #self.get_progress_cache_in_mplayer(linea)
                    pass
                
                elif "Movie-Aspect" in linea:
                    "Información sobre el aspecto del video. Ejemplo:"
                    "Movie-Aspect is 1.78:1 - prescaling to correct movie aspect."
                    #self.emit("video", True)
                    pass
                    
                elif "Starting playback" in linea:
                    "Cuando comienza la Reproducción. Ejemplo:"
                    "Starting playback..."
                    self.estado = "playing"
                    self.emit("estado", "playing")
                    
                elif "AO:" in linea:
                    "Información Sobre Audio en la pista. Ejemplo:"
                    "AO: [pulse] 44100Hz 2ch s16le (2 bytes per sample)"
                    pass
                
                elif "VO:" in linea:
                    "Información sobre Video en la pista. Ejemplo:"
                    "VO: [xv] 428x240 => 428x240 Planar YV12"
                    pass
                    
                elif "Resolving" in linea:
                    "Información sobre Resolución de Streamings. Ejemplo:"
                    "Resolving radio1.oceanofm.com for AF_INET6..."
                    pass
                
                elif "Connecting" in linea:
                    "Información sobre Conexión a un Streaming. Ejemplo:"
                    "Connecting to server main-office.rautemusik.fm[87.230.101.9]: 80..."
                    pass
                
                elif "Name" in linea:
                    "El nombre de una streaming de Radio. Ejemplo:"
                    "Name   : #MUSIK.MAIN - WWW.RAUTEMUSIK.FM - 24H TOP 40 POP HITS 80S 90S DANCE HOUSE ROCK RNB AND MORE!"
                    pass
                
                elif "Playing" in linea:
                    "La Pista que se está reproduciendo. Ejemplo:"
                    "Playing /media/4E432D364BC64012/E - Videos/Tylor swift/Back to December-Taylor Swift Lyrics."
                    pass
                
                elif "Genre" in linea or "Website" in linea or "Bitrate" in linea:
                    "Información Sobre un Streaming de Radio. Ejemplo:"
                    "Genre  : Pop Rock Top 40 RnB 80s"
                    "Website: http://www.RauteMusik.FM/"
                    "Bitrate: 128kbit/s"
                    pass
                    
                elif "Opening" in linea or "AUDIO" in linea or "Selected" in linea:
                    "Información sobre Codecs Utilizados. Ejemplo:"
                    "Opening video decoder: [ffmpeg] FFmpeg's libavcodec codec family"
                    "Selected video codec: [ffh264] vfm: ffmpeg (FFmpeg H.264)"
                    "Opening audio decoder: [ffmpeg] FFmpeg/libavcodec audio decoders"
                    "AUDIO: 44100 Hz, 2 ch, s16le, 98.6 kbit/6.99% (ratio: 12323->176400)"
                    "Selected audio codec: [ffaac] afm: ffmpeg (FFmpeg AAC (MPEG-2/MPEG-4 Audio))"
                    pass
                
                else:
                    "Información Diversa. Ejemplo:"
                    "Failed to open /dev/rtc: Permission denied (it should be readable by the us"
                    "Unsupported PixelFormat 61"
                    "Unsupported PixelFormat 53"
                    "Unsupported PixelFormat 81"
                    "eo (h264), -vid 0"
                    "[lavf] stream 1: audio (aac), -aid 0"
                    "VIDEO:  [H264]  640x480  0bpp  30.000 fps  218.3 kbps (26.6 kbyte/s)"
                    "Clip info:"
                    "starttime: 0"
                    "totalduration: 226"
                    "totaldatarate: 338"
                    "bytelength: 9570679"
                    "canseekontime: true"
                    "sourcedata: BC8280065HH1341966475963833"
                    "purl: "
                    "pmsg: "
                    "Load subtitles in /media/4E432D364BC64012/E - Videos/Tylor swift/"
                    "=========================================================================="
                    "libavcodec version 53.35.0 (external)"
                    "Mismatching header version 53.32.2"
                    "=========================================================================="
                    "=========================================================================="
                    "=========================================================================="
                    "A:   0.0 V:   0.0 A-V:  0.014 ct:  0.000   0/  0 ??% ??% ??,?% 0 0 90%"
                    "A: 123.2 V: 123.2 A-V: -0.000 ct:  0.033   0/  0  2%  1%  0.4% 0 0 50%"
                    
                    "Cuando no se puede Acceder a un Streaming. Ejemplo:"
                    "Failed to get value of property 'percent_pos'."
                    "Failed to get value of property 'percent_ANS_ERFailed to get value of"
                    "prANS_ERROR=PROPERTY_UNAFailed toANS_ERROR=PROPERTY_UNAVAILABLE"
                    "ANS_ERROR=PROPERTY_UNAVAILABLE"
                    pass
                
        return True
    
    def get_progress_in_mplayer(self, linea):
        """Obtiene el progreso de la reproduccion y lo
        envia en una señal para actualizar la barra de
        progreso."""
        
        pos = 0
        try:
            if "Cache size" in linea: return
            pos = int(linea.split('=')[1])
            
            if pos != self.posicion:
                self.posicion = pos
                self.emit("newposicion", self.posicion)
                
                if self.posicion >= 100:
                    self.emit("endfile")
                    
        except Exception, e:
            print "Error en Progreso de Reproducción: %s" % (e)
            
    def pause_play(self):
        """Llama a play() o pause()
        segun el estado actual del reproductor."""

        try:
            if self.entrada:
                if self.estado == "playing": # pausa
                    self.pause()
                    
                elif self.estado == "paused":
                    self.pause(True)
                    self.estado = "playing"
                    self.emit("estado", "playing")
                    
                else:
                    #if self.uri: self.load(self.uri)
                    pass
                
        except Exception, e:
            print "HA OCURRIDO UN ERROR EN PAUSE_PLAY DEL REPRODUCTOR", e
            
    def pause(self, reset = False):
        """Pone en pause o unpause a mplayer"""
        
        self.entrada.write('pause 0\n')
        self.entrada.flush()
        self.new_handle(reset)
        self.estado = "paused"
        self.emit("estado", "paused")
        
    def play(self):
        """No hace nada. mplayer utiliza:
        pause, unpause y load en lugar de play."""
        
        pass
        
    def new_handle(self, reset):
        """Elimina o reinicia la funcion que
        envia los datos de actualizacion para
        la barra de progreso del reproductor."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if reset:
            self.actualizador = GObject.timeout_add(35, self.handle)
            
    def set_position(self, posicion):
        """Permite desplazarse por
        la pista que se esta reproduciendo."""
        
        # FIXME: Actualmente no funciona bien
        posicion = int(posicion)
        if posicion != self.posicion:
            self.posicion = posicion
            self.entrada.write('seek %s %i 0\n' % (posicion, 1))
            self.entrada.flush()
            
    def get_volumen(self):
        """Obtiene el volumen de reproducción.
        Lo hace solo al reproducir el primer archivo
        o streaming y envía el dato para actualizar
        el control de volúmen."""
        
        if self.volumen != 0: return
    
        if self.entrada:
            self.entrada.write("%s 0\n" % ("get_property volume"))
            self.entrada.flush()
            linea = self.salida.readline()
            
            if "ANS_volume" in linea:
                valor = float(linea.split("=")[1])
                
                if self.volumen == 0:
                    self.volumen = valor
                    self.emit('volumen', valor)
                    
    def set_volumen(self, valor):
        """Cambia el volúmen de Reproducción."""
        
        if self.entrada:
            if valor != self.volumen:
                self.volumen = valor
                self.entrada.write("%s %s 0\n" % ("set_property volume", valor))
                self.entrada.flush()
                
    def set_balance(self, brillo = None, contraste = None,
        saturacion = None, hue = None, gamma = None):
        """Seteos de balance en la fuente de video.
        Recibe % en float y convierte a los valores del filtro."""
        
        # FIXME: Actualmente no funciona.
        if saturacion != None:
            # int. Range: -100 - 100 Default: 0
            self.config['saturacion'] = int(200 * saturacion / 100 - 100)
            
            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property saturation",
                    self.config['saturacion']))
                self.entrada.flush()
            
        if contraste != None:
            # int. Range: -100 - 100 Default: 0
            self.config['contraste'] = int(200 * contraste / 100 - 100)
            
            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property contrast",
                    self.config['contraste']))
                self.entrada.flush()
            
        if brillo != None:
            # int. Range: -100 - 100 Default: 0
            self.config['brillo'] = int(200 * brillo / 100 - 100)
            
            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property brightness",
                    self.config['brillo']))
                self.entrada.flush()
            
        if hue != None:
            # int. Range: -100 - 100 Default: 0
            self.config['hue'] = int(200 * hue / 100 - 100)
            
            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property hue",
                    self.config['hue']))
                self.entrada.flush()
            
        if gamma != None:
            # int. Range: -100 - 100 Default: 0
            self.config['gamma'] = int(200 * gamma / 100 - 100)
            
            if self.entrada:
                self.entrada.write("%s %i 0\n" % ("set_property gamma",
                    self.config['gamma']))
                self.entrada.flush()
                
    def get_balance(self):
        """Retorna los valores actuales de balance en %."""
        
        return {
        'saturacion': (self.config['saturacion']+100) * 100.0 / 200.0,
        'contraste': (self.config['contraste']+100) * 100.0 / 200.0,
        'brillo': (self.config['brillo']+100) * 100.0 / 200.0,
        'hue': (self.config['hue']+100) * 100.0 / 200.0,
        'gamma': (self.config['gamma']+100) * 100.0 / 200.0
        }
    
    def get_balance_default(self):
        """ Retorna los valores por defecto para balance y gamma en %. """
        
        return {
        'saturacion': 50.0,
        'contraste': 50.0,
        'brillo': 50.0,
        'hue': 50.0,
        'gamma': 10.0
        }
        
    def rotar(self, valor):
        """Mplayer no permite rotación de video."""
        
        pass
        
REC = "/tmp/mplayerrec%d" % time.time()
class MplayerGrabador(GObject.GObject):
    """Graba desde un streaming de radio o tv."""
    
    __gsignals__ = {
    "update":(GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,))}
    
    def __init__(self, uri, archivo):
        
        GObject.GObject.__init__(self)
        
        self.actualizador = None
        self.archivo = None
        self.uri = ""
        self.info = ""
        
        estructura = "%s -slave -idle -nolirc -nomouseinput -noconsolecontrols -nojoystick -dumpstream -dumpfile %s" % (MPLAYER, archivo)
        self.mplayer = subprocess.Popen(estructura, shell = True, stdin = subprocess.PIPE,
            stdout = open(REC,"w+b"), stderr=open(REC,"r+b"), universal_newlines=True)
            
        self.entrada = self.mplayer.stdin
        self.salida = open(REC,"r")
        
        self.entrada.write("loadfile %s 0\n" % uri)
        self.entrada.flush()
        
        self.new_handle(True)
        
    def new_handle(self, reset):
        """Elimina o reinicia la funcion que
        envia los datos de actualizacion."""
        
        if self.actualizador:
            GObject.source_remove(self.actualizador)
            self.actualizador = None
            
        if reset:
            self.actualizador = GObject.timeout_add(35, self.handle)
            
    def handle(self):
        """Consulta el estado y progreso de
        la grabacion."""
        
        if not self.entrada.closed:
            linea = self.salida.readline()
            tamanio = None
            
            if linea:
                if 'Playing' in linea:
                    self.uri = linea.split()[-1]
                    
                if 'dump:' in linea:
                    tamanio = int(int(linea.split()[1])/1024)
                    
                if self.uri and tamanio:
                    info = "Grabando: %s - %s Kb Almacenados." % (str(self.uri), str(tamanio))
                    
                    if self.info != info:
                        self.info = info
                        self.emit('update', self.info)
                        
        return True
        
    def stop(self):
        """Detiene la Grabación actual."""
        
        try:
            if self.entrada:
                self.entrada.write('%s 0\n' % "quit")
                self.entrada.flush()
                self.new_handle(False)
                
        except Exception, e:
            print "HA OCURRIDO UN ERROR EN QUIT DEL GRABADOR", e
            
        self.mplayer.kill()
        
        try:
            if os.path.exists(self.archivo): os.chmod(self.archivo, 0755)
            
        except:
            pass
        
        if os.path.exists(REC): os.unlink(REC)
        