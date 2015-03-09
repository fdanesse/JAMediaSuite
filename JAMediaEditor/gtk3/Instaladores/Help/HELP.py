#!/usr/bin/env python
# -*- coding: utf-8 -*-


INSTALADORES = """
Conceptos Generales:
    La instalación de programas computacionales, (software) es el proceso fundamental por el cual un programa
    es transferido a un ordenador con el fin de ser configurado, y preparado para ser ejecutado en el sistema.

    Básicamente se trata de un proceso donde se copia cada archivo del programa a un directorio del sistema y
    se le da los permisos correctos para que luego pueda ser ejecutado por los usuarios del mismo.

    Una instalación exitosa es condición necesaria para el buen funcionamiento de cualquier software.
    Cuanto más complejo sea el software, es decir, cuanto más archivos contenga,
    mayor sea la dispersión de esos archivos y mayor sea la interdependencia con otros programas o bibliotecas,
    mayor es el riesgo de que se produzcan errores durante la instalación y también durante la ejecución del mismo.
    Si la instalación falla aunque sea parcialmente, el fin que persigue la instalación posiblemente no podrá ser alcanzado.
    Por esa razón, sobre todo en casos de software complejo, el desarrollo de un proceso de instalación confiable y seguro
    es una parte fundamental del desarrollo del software.

    La desinstalación de software es el proceso por el cual se elimina el software del computador.

Descripción básica para linux:

    En un sistema linux, un programa instalado en el sistema cuenta con:
        1- Un lanzador en el path del sistema que hace referencia al ejecutable principal de la aplicación.
        2- Un directorio con el código de la aplicación.

    Directorio de Instalación de las Aplicaciones:
        Las aplicaciones se deben instalar en /usr/share o /usr/local/share
        Esto quiere decir que el instalador debe copiar el directorio de tu aplicación a una de esas rutas.

    Lanzador de aplicaciones:
        El lanzador es el archivo que hará que tu aplicación se ejecute.
        Contendrá algo como:
            #!/bin/sh
            exec "/usr/bin/python" "/usr/share/JAMediaEditor/Main.py" "$@"

        Este archivo debe estar en el path del sistema.

    El PATH del Sistema:
        Los directorios del path del sistema son los directorios donde linux busca ejecutables que hagan referencia a las
        ordenes que tu le pasas en una terminal. Por ejemplo si tu escribes nano en una terminal y das enter, el sistema busca en los
        directorios del path un ejecutable con ese nombre, si lo encuentra, lo ejecuta, de lo contrario te dirá que esa orden no existe.

        Puedes saber donde se encuentra instalado nano y donde su lanzador en el path del sistema, ejecutando en una terminal:
            whereis nano
        Obtendrás algo como:
            nano: /usr/bin/nano /bin/nano /usr/share/nano /usr/share/man/man1/nano.1.gz

        Esta información dice que:
            El lanzador se encuentra en /usr/bin/nano y /bin/nano
            La aplicación está instalada en /usr/share/nano
            (/usr/share/man/man1/nano.1.gz es el manual de nano)

        Para saber que directorios se encuentran en el path puedes ejecutar lo siguiente en una terminal:
            echo $PATH
        Obtendrás algo como esto:
            /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games

        Básicamente, los directorios del path del sistema se organizan de esta forma:

        /bin
            lanzadores del sistema utilizados durante el arranque.
        /sbin
            Igual que el anterior pero para lanzadores creados por el root.
        /usr/bin
            lanzadores de la distribución para todo el sistema.
        /usr/sbin
            Igual que el anterior pero para lanzadores creados por el root.

        La ruta /usr/local es para aquellos lanzadores que no están administrados por el sistema o la distribución,
        por lo cual, los lanzadores de tus aplicaciones deben instalarse en una de estas rutas:
            /usr/local/bin
            /usr/local/sbin

Agregar archivo desktop:
    Si quieres que tu aplicación se ejecute desde el menú del entorno gráfico, debes agregar un archivo .desktop
    Un archivo desktop hace referencia al ícono y ejecutable de la aplicación.

    Ejemplo del contenido de un archivo .desktop:
        [Desktop Entry]
        Encoding=UTF-8
        Name=JAMediaEditor
        GenericName=JAMediaEditor
        Comment=Editor de Codigo
        Exec=/usr/local/bin/jamediaeditor_run
        Terminal=false
        Type=Application
        Icon=/usr/local/share/JAMediaEditor/JAMediaObjects/Iconos/JAMediaEditor.svg
        Categories=GTK;Development;IDE
        StartupNotify=true
        Keywords=Code;Editor;Programming;
        MimeType=application/x-ide;text/plain;text/x-chdr;text/x-csrc;text/x-c++hdr;text/x-c++src;text/x-java;text/x-dsrc;text/x-pascal;text/x-perl;text/x-python;application/x-php;application/x-httpd-php3;application/x-httpd-php4;application/x-httpd-php5;application/xml;text/html;text/css;text/x-sql;text/x-diff;

    Este archivo debe guardarse en /usr/share/applications/

Sobre JAMediaEditor:
    El sistema de creación de instaladores de JAMediaEditor es muy sencillo, persigue el objetivo de facilitarle el proceso
    de construcción de este tipo de paquetes a aquellos usuarios que están aprendiendo a programar.
    No pretende ser una solución ni siquiera medianamente avanzada a la construcción de instaladores, sin embargo, lo básico
    lo hace bien y si necesitas complejizar más los guiones de cualquier paquete instalador creado por JAMediaEditor y sabes como hacerlo,
    solo debes editar los archivos del mismo luego de crear el paquete base.
    (Los paquetes instaladores creados por JAMediaEditor, se guardan en: /directorio del usuario/JAMediaEditorCONF/)
"""


def get_help(help):
    if help == "help instaladores":
        return INSTALADORES
    elif help == "help deb":
        return ""
    elif help == "help rmp":
        return ""
    elif help == "help standard":
        return ""
    elif help == "help sin root":
        return ""
    elif help == "help sugar":
        return ""
    else:
        return ""
