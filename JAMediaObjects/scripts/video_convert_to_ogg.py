#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convertir audio y video a ogg
    gst-launch-0.10 filesrc location=/home/flavio/Documentos/001 ! \
    decodebin name=decodificador ! \
        queue ! audioconvert ! audioresample ! \
            vorbisenc ! \
                oggmux name=contenedor ! filesink location=/home/flavio/Documentos/004.ogg \
        decodificador. ! queue ! ffmpegcolorspace ! videorate ! \
            theoraenc ! contenedor.
"""

import os
import sys
import commands

contador = 0


def convertir(origen):
    """
    Convierte un video a formato ogg.
    """

    if not os.path.exists(origen):
        print "No se encontró:", origen
        return

    if not os.path.isfile(origen):
        print origen, "no es un archivo"
        return

    print "Convirtiendo:", origen

    destino = "%s.ogg" % (origen)

    comando = "gst-launch-1.0 filesrc location=\"%s\" !" % origen
    comando = "%s decodebin name=t !" % comando
    comando = "%s queue ! audioconvert ! audioresample !" % (comando)
    comando = "%s vorbisenc ! oggmux name=contenedor !" % comando
    comando = "%s filesink location=\"%s\"" % (comando, destino)
    comando = "%s t. ! queue ! videoconvert !" % comando
    comando = "%s videorate ! theoraenc ! contenedor." % comando

    print commands.getoutput(comando)


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
    sys.exit(0)

origen = sys.argv[1]

if os.path.isdir(origen):

    for archivo in os.listdir(origen):
        arch = os.path.join(origen, archivo)

        if "video" in get_data(arch):
            contador += 1
            convertir(arch)

elif os.path.isfile(origen):
    contador += 1
    convertir(origen)

print "Proceso Terminado. Se han procesado %s archivos." % contador

sys.exit(0)
