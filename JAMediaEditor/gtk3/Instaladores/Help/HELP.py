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

    El sistema de creación de instaladores de JAMediaEditor es muy sencillo pues persigue el objetivo de facilitarle el proceso
    de construcción de este tipo de paquetes a aquellos usuarios que están aprendiendo a programar.
    No pretende ser una solución ni siquiera medianamente avanzada a la construcción de instaladores, sin embargo, lo básico
    lo hace bien y si necesitas complejizar más los guiones de cualquier paquete instalador creado por JAMediaEditor y sabes como hacerlo,
    solo debes editar los archivos del mismo durante el proceso de construcción o luego de creado el paquete base.

    Los paquetes instaladores creados por JAMediaEditor, se guardan en: /directorio del usuario/JAMediaEditorCONF/
    Dentro de ese directorio, hay varios directorios que refieren al tipo de instalador que JAMediaEditor va a crear (DEB, SUGAR, etc . . .)
    Por ejemplo, cuando creas un instalador .deb para el proyecto Bichos, JAMediaEditor creará un directorio Bichos dentro del directorio DEB y
    Construirá allí toda la estructura necesaria para construir el instalador. El archivo .deb final, se guardará en JAMediaEditorCONF indicando además su versión.
    Este proceso se sigue para todos los tipos de instaladores generados por JAMediaEditor, de modo que incluso en los archivos finales siempre puedes realizar los
    cambios que desees y volver a construir manualmente los instaladores.

    Debes considerar que cada vez que inicias la interfaz de construcción de un tipo particular de instalador en JAMediaEditor para un proyecto determinado,
    JAMediaEditor limpiará el directorio correspondiente a ese tipo de instalador y volverá a construir toda la estructura de archivos y directorios necesaria.
"""


DEB = """
Los paquetes .deb son instaladores gestionados por el Sistema de gestión de paquetes debian (apt = Advanced Packaging Tool).

Sistema de gestión de paquetes:

    Un sistema de gestión de paquetes, es una colección de herramientas que sirven para automatizar el proceso de instalación, actualización,
    configuración y eliminación de paquetes de software. El término se usa comúnmente para referirse a los gestores de paquetes en sistemas Unix-like,
    especialmente GNU/Linux, ya que se apoyan considerablemente en ellos.

    En estos sistemas, el software se distribuye en forma de paquetes, frecuentemente encapsulado en un solo fichero.
    Estos paquetes incluyen otra información importante, además del software en sí, como pueden ser el nombre completo, una descripción de su funcionalidad,
    el número de versión, el distribuidor del software, la suma de verificación y una lista de otros paquetes requeridos para el correcto funcionamiento del software.
    Esta metainformación se introduce normalmente en una base de datos de paquetes local.

    Los sistemas de gestión de paquetes tienen la tarea de organizar todos los paquetes instalados en el sistema y se encargan de mantener su usabilidad.

    Esto se consigue combinando las siguientes técnicas:

        Comprobación de la suma de verificación para evitar que haya diferencias entre la versión local de un paquete y la versión oficial.
        Comprobación de la firma digital.
        Instalación, actualización y eliminación simple de paquetes.
        Resolución de dependencias para garantizar que el software funcione correctamente.
        Búsqueda de actualizaciones para proveer la última versión de un paquete.
        Agrupamiento de paquetes según su función para evitar la confusión al instalarlos o mantenerlos.

    Muchos de los sistemas de gestión de paquetes ampliamente utilizados utilizan backends simples para instalar los paquetes.
    Por ejemplo, YUM utiliza RPM y APT utiliza dpkg.

Sistemas basados en paquetes binarios:

    dpkg, usado originalmente por Debian y ahora también por otros sistemas, usa el formato .deb y fue el primero en poseer una herramienta
    de resolución de dependencias ampliamente conocida, APT.

Advanced Packaging Tool (apt):

    Es un sistema de gestión de paquetes creado por el proyecto Debian.
    APT simplifica en gran medida la instalación y eliminación de programas en los sistemas GNU/Linux.
    No existe un programa apt en sí mismo, sino que APT es una biblioteca de funciones C++ que es empleada por varios programas de
    línea de comandos para distribuir paquetes. En especial, apt-get y apt-cache.

    Existen también programas que proporcionan un frontend para APT, generalmente basados en apt-get, como aptitude con una interfaz de texto ncurses,
    Synaptic con una interfaz gráfica GTK+, o Adept con una interfaz gráfica Qt.

    Existe un repositorio central con más de 25.000 paquetes apt utilizados por apt-get y programas derivados para descargar e instalar
    aplicaciones directamente desde Internet, conocida como una de las mejores cualidades de Debian.

    APT fue rápidamente utilizado para funcionar con paquetes .deb, en los sistemas Debian y distribuciones derivadas, pero desde entonces ha sido
    modificado para trabajar con paquetes RPM, con la herramienta apt-rpm, y para funcionar en otros sistemas operativos, como Mac OS X y OpenSolaris.

Como crear un paquete .deb:

    Un paquete debian, utiliza:

        Un archivo de control para manejar la información del paquete.
        Una estructura de directorios con el software a distribuir.

    Hagamos un ejemplo práctico:

    En un directorio llamado "Proyecto", creamos la estructura de directorios de instalación del software.
    Esta estructura debe replicar la estructura final de instalación de nuestro software, de modo que creamos dos directorios, (bin y share).
    Dentro del directorio share, copiamos el directorio que contiene nuestro software a instalar.
    Dentro del directorio bin, escribimos el lanzador de nuestra aplicación, (ver Ayuda sobre "Instaladores en General").
    Si deseas un lanzador en algún menú del entorno gráfico, dentro de share creas el directorio applications y en él escribes tu archivo .desktop, (ver Ayuda sobre "Instaladores en General").

    Además, en el directorio "Proyecto", debes crear el directorio DEBIAN y dentro escribir el archivo control.

    La estructura final de directorios y archivos para el caso de JAMediaEditor, será:

        JAMediaEditor
            DEBIAN
                control
            bin
                lanzador
            share
                applications
                    jamediaeditor.desktop
                JAMediaEditor
                    Todo el código de JAMediaEditor . . .

    Ejemplo de archivo control:

        Package: bichos
        Source: Bichos
        Version: 1
        Section: Game
        Priority: optional
        Architecture: all
        Maintainer: flavio danesse <fdanesse@gmail.com>
        Homepage: https://sites.google.com/site/sugaractivities/cucarasims
        Depends:
        Description: Este campo es obligatorio
         Este campo es obligatorio y debe tener un espacio vacío al comienzo

    Luego de tener toda la estructura de directorios y archivos lista, debes asegurarte de dar los permisos de lectura y ejecución adecuados a cada archivo y directorio.
    En particular, todos los ejecutables deben tener permisos de ejecución, esto incluye el lanzador y el archivo .desktop.
    Cuando esté todo listo, desde la terminal construimos el paquete .deb utilizando dpkg:

        dpkg -b ./deb /directorio_construido_anteriormente /directorio_destino_del_paquete_deb/nombre_paquete.deb

    El archivo .deb resultante está listo para ser distribuido o instalado con el gestor de paquetes. (Recuerda darle permisos de ejecución).

Sobre JAMediaEditor:

    Los paquetes .deb son generalmente muchísimo más complejos que el ejemplo explicado aquí, sin embargo,
    basta con lo demostrado acá para construir un instalador .deb funcional.
    A medida que aprendas más sobre instaladores .deb, podrás ir mejorando el archivo control e ir incorporando otros archivos que suelen utilizarse.

    JAMediaEditor sólo pretende automatizar el proceso para hacer fácil lo sencillo y tu puedas aprender sobre ello.
    Los instaladores .deb construidos con JAMediaEditor, si bien son muy simples, deben funcionar sin que hagas cambio alguno.
    Si alguno de ellos falla, asegúrate que no se debe a cambios realizados por tí en alguno de los archivos involucrados en el proceso.

    Una forma de aprender sobre esto, por inmersión, puede ser descargar archivos .deb, descomprimirlos y leer los archivos involucrados.
    Si bien un archivo .deb puedes descomprimirlo igual que un zip común, lo correcto es hacerlo mediante:

        dpkg -x paquete.deb directorio
"""


def get_help(help):
    if help == "help instaladores":
        return INSTALADORES
    elif help == "help deb":
        return DEB
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
