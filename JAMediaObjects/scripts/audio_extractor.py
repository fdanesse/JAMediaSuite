#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
'gst-launch-1.0 filesrc location=/home/flavio/Documentos/001 ! \
    decodebin name=t ! \
        queue ! audioconvert ! lamemp3enc ! filesink \
            location=/home/flavio/Documentos/002.mp3 \
        t. ! queue ! autovideosink')
"""

import os
import sys
import commands

contador = 0

codecs = {
    "MP3": ["lamemp3enc", "mp3"],
    "WAV": ["wavenc", "wav"],
    "OGG": ["vorbisenc ! oggmux", "ogg"],
    }

def extraer(origen, codec):
    """
    Extrae el audio de un video y lo guarda en un archivo con el mismo
    nombre, con la extensión y formato elegido.
    """

    if not os.path.exists(origen):
        print "No se encontró:", origen
        return

    if not os.path.isfile(origen):
        print origen, "no es un archivo"
        return

    print "Extrayendo audio de:", origen
    print "Guardando en Formato:", codec[1]

    destino = "%s.%s" % (origen, codec[1])

    comando = "gst-launch-1.0 filesrc location=\"%s\" !" % origen
    comando = "%s decodebin name=t !" % comando
    comando = "%s queue ! audioconvert ! %s !" % (comando, codec[0])
    comando = "%s filesink location=\"%s\"" % (comando, destino)
    comando = "%s t. ! queue ! autovideosink" % comando

    commands.getoutput(comando)


def get_data(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    """

    datos = commands.getoutput(
        'file -ik %s%s%s' % ("\"", archivo, "\""))

    retorno = ""

    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)

    return retorno


if not len(sys.argv) > 1:
    print "Debes ingresar el nombre de un archivo o directorio."
    print "También Puedes ingresar el formato final (ogg, mp3, wav)."
    sys.exit(0)

origen = sys.argv[1]
codec = codecs["MP3"]

if len(sys.argv) > 2:
    C = str(sys.argv[2]).upper()

    if codecs.get(C, False):
        codec = codecs[C]

if os.path.isdir(origen):

    for archivo in os.listdir(origen):
        arch = os.path.join(origen, archivo)

        if "video" in get_data(arch):
            contador += 1
            extraer(arch, codec)

elif os.path.isfile(origen):
    contador += 1
    extraer(origen, codec)

print "Proceso Terminado. Se han procesado %s archivos." % contador

sys.exit(0)
