#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASEPATH = os.path.dirname(__file__)


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
    Por ejemplo, cuando creas un instalador .deb para el proyecto Bichos, JAMediaEditor creará un directorio Bichos dentro de /directorio del usuario/JAMediaEditorCONF/ y
    Construirá allí toda la estructura necesaria para construir el instalador. El archivo .deb final, se guardará en /directorio del usuario/JAMediaEditorCONF/ indicando además su versión.
    Este proceso se sigue para todos los tipos de instaladores generados por JAMediaEditor, de modo que incluso en los archivos finales siempre puedes realizar los
    cambios que desees y volver a construir manualmente los instaladores.

    Debes considerar que cada vez que inicias la interfaz de construcción de un tipo particular de instalador en JAMediaEditor para un proyecto determinado,
    JAMediaEditor limpiará el directorio correspondiente a ese instalador y volverá a construir toda la estructura de archivos y directorios necesaria.
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
    Si deseas un lanzador en algún menú del entorno gráfico, dentro de share creas el directorio applications y en él escribes tu archivo .desktop,
    (ver Ayuda sobre "Instaladores en General").

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
    Bastará con que el usuario haga doble click sobre él, para que el gestor de paquetes lo abra y pueda comenzar su instalación.

    Luego, para desinstalar la aplicación, el usuario debe hacer:

        sudo apt-get remove nombre_de_la_aplicación

Sobre JAMediaEditor:

    Los paquetes .deb son generalmente muchísimo más complejos que el ejemplo explicado aquí, sin embargo,
    basta con lo demostrado acá para construir un instalador .deb funcional.
    A medida que aprendas más sobre instaladores .deb, podrás ir mejorando el archivo control e ir incorporando otros archivos que suelen utilizarse.

    JAMediaEditor sólo pretende automatizar el proceso para hacer esto fácil y tu puedas aprender sobre ello.
    Los instaladores .deb construidos con JAMediaEditor, si bien son muy simples, deben funcionar sin que hagas cambio alguno.
    Si alguno de ellos falla, asegúrate que no se debe a cambios realizados por tí en alguno de los archivos involucrados en el proceso.

    Una forma de aprender sobre esto, por inmersión, puede ser descargar archivos .deb, descomprimirlos y leer los archivos involucrados.
    Si bien un archivo .deb puedes descomprimirlo igual que un zip común, lo correcto es hacerlo mediante:

        dpkg -x paquete.deb directorio
"""


SINROOT = """
La Clave de root:

    Para instalar una aplicación en tu sistema necesitas ser administrador del mismo, es decir, tener la clave de root.
    Esta es una de las medidas de seguridad de linux para prevenir la perdida o robo de información por parte de usuarios no autorizados.
    Para linux, la seguridad de la información de los usuarios, es lo principal.

    Como ya habrás visto, los instaladores pueden a su vez, llamar a instalar a otras aplicaciones y bibliotecas de código necesarias.
    Si linux permitiera que cualquiera instale paquetes en el sistema, nunca estarías seguro sobre que estaría haciendo ese código,
    en cambio, el administrador del sistema, se supone que es garante de no tener código malicioso instalado en el sistema.

Instalaciones locales:

    Sin embargo, linux permite que un usuario particular sin acceso al root, instale aplicaciones dentro de su entorno, sin afectar al
    resto de los usuarios. En este caso, si no tienes acceso al root y tu aplicación no necesita instalar nada extra,
    ya sean bibliotecas u otras aplicaciones, puedes instalarla en el entorno de tu usuario.
    (si tu instalador necesita instalar otras cosas, linux no te permitirá hacerlo sin la clave de root).

    Para hacer esto, se utilizan los directorios dentro de /home/tu usuario/.local
    En ese path, debes replicar los path que utiliza el sistema para instalar las aplicaciones, guardar los archivos .desktop y los lanzadores.

    Es decir, debes utilizar estos directorios:

        /home/tu usuario/.local
            /bin
            /share
                /applications

    Si alguno de ellos no existe, puedes crearlo, y luego, solo debes:

        Copiar el directorio de tu aplicación a /home/tu usuario/.local/share
        Escribir el lanzador en /home/tu usuario/.local/bin
        Escribir el archivo .desktop en /home/tu usuario/.local/share/applications

    Para comprender mejor lo anterior, puedes consultar la Ayuda sobre "Instaladores en General".

Sobre JAMediaEditor:

    Para ayudarte a construir este instalador, JAMediaEditor cuenta con una plantilla que permite crear todos los archivos necesarios y
    copiarlos a los sitios referidos anteriormente, en el mismo momento de instalar tu aplicación.

    Básicamente, cuando selecciones para construir este tipo de instalador, JAMediaEditor te presentará un script python con el código
    que permitirá crear toda la estructura de directorios en caso de que no existieran, e instalar tu aplicación al momento de ser ejecutado.
    Esta forma de hacerlo se debe a que el instalador debe tomar algunos datos del sistema donde vayas a instalarlo para crear el archivo .desktop.

    Cuando construyas el instalador, JAMediaEditor guardará todo y construirá un archivo .zip con el paquete de tu aplicación indicando la versión,
    dejandolo listo para ser distribuido.

    Para instalar la aplicación, el usuario, luego de descargar el .zip y descomprimirlo, tendrá que ejecutar el archivo install.py
    Para desinstalarla, el usuario tendrá que borrar el archivo .desktop y el directorio de la aplicación que se encontrarán en la estructura de
    directorios anteriormente detallada.

    Por defecto, este instalador no crear un lanzador ya que no es necesario si el archivo .desktop apunta al main de tu aplicación.
    Tampoco crea un desinstalador, pero en ambos casos, tu puedes agregarlos si lo deseas, modificando install.py para que los cree al ser ejecutado.
"""


PYTHON = """
Un instalador python requiere de los siguientes archivos:

    setup.cfg
    setup.py
    MANIFEST

    Además de estos archivos, hay que agregar el lanzador y el .desktop ya que son necesarios para ejecutar la aplicación cuando esté instalada.
    Para saber que información llevan estos dos últimos archivos, lee la Ayuda sobre "Instaladores en General").

    El archivo setup.cfg debe contener los paths de instalación de tu proyecto como se muestra en el siguiente ejemplo:

        [install]
        install_lib=/usr/local/share/JAMediaTube
        install_data=/usr/local/share/JAMediaTube
        install_scripts=/usr/local/bin

    El archivo MANIFEST, debe contener toda la estructura de archivos y directorios interna de tu proyecto. Cualquier archivo que desees distribuir
    con tu aplicación, debe estar listado en MANIFEST. A continuación vemos un fragmento de uno de estos archivos:

        JAMedia/Iconos/JAMedia.svg
        JAMedia/Iconos/agregar.svg
        JAMedia/Iconos/JAMediaCredits.svg
        JAMedia/JAMediaReproductor/JAMediaGrabador.py
        JAMedia/JAMediaReproductor/JAMediaBins.py
        JAMedia/JAMediaReproductor/JAMediaReproductor.py
        JAMedia/JAMediaReproductor/__init__.py
        AUTHORS
        jamediatube_run
        PanelTube.py
        JAMediaTube.desktop
        Globales.py
        COPYING
        jamediatube_uninstall
        youtube-dl
        setup.cfg
        JAMediaYoutube.py
        __init__.py
        Widgets.py
        PanelTubeWidgets.py
        setup.py
        MANIFEST
        TubeListDialog.py
        JAMediaTube.py

    Nota:
        En el archivo MANIFEST, también deben estar listados los archivos de instalación: setup.cfg, setup.py y MANIFEST
        Obviamente es muy engorroso llenar a mano este archivo si tu proyecto es muy grande.

    El archivo setup.py es el más complejo de los tres, en él, hay que importar la función setup de distutils.core y
    llamarla pasándole en sus parámetros, la información de nuestro proyecto para que ella pueda construir el paquete distribuible
    de nuestro instalador.

    Esta función, setup, toma muchos parámetros los cuales se detallan a continuación:

    Metadatos del proyecto:

        name = "JAMediaTube",
        version = "10.0.0",
        author = "Flavio Danesse",
        author_email = "fdanesse@gmail.com",
        url = "https://sites.google.com/site/sugaractivities/jamediaobjects/jamediatube",
        license = "GPL3",

    Lanzadores de la aplicación:

        scripts = ["jamediatube_run", "jamediatube_uninstall"],

    Main ejecutable de la aplicación:

        py_modules = ["JAMediaTube"],

    Archivos de la aplicación:

        data_files =[
        ("/usr/share/applications/", ["JAMediaTube.desktop"]),
        ("",[
            "JAMediaTube.py",
            "TubeListDialog.py",
            "MANIFEST",
            "setup.py",
            etc . . .

    La estructura general de este archivo es:

        from distutils.core import setup

        setup(
            name = "",
            version = "",
            author = "",
            author_email = "",
            url = "",
            license = "",

            scripts = [],

            py_modules = [],

            data_files =[
                (path destino, [archivos en mi proyecto]),
                (otro path destino,[archivos en mi proyecto]),
                (etc . . .,[etc . . .]),
                ])

    Los primeros datos sólo son metadatos del proyecto, por lo cual no es difícil de incorporarlos, pero los otros entrañan mucha
    dificultad si debes escribirlos a mano, dado que que hay que especificar los paths correctamente de cada archivo en el proyecto.

    Los archivos detallados en scripts son los lanzadores de la aplicación y deben escribirse con el path relativo en que se encuentran
    dentro del directorio de tu proyecto. Estos archivos se instalarán en el path establecido en el campo install_scripts del archivo setup.cfg
    Además, deben estar correctamente listados en MANIFEST.

    Como ya habrás comprendido, los archivos setup.cfg, setup.py y MANIFEST, trabajan juntos.

    El parámetro py_modules debe listar los archivos "main" de python de tu proyecto, es decir, el archivo principal de tu aplicación, o
    los archivos principales si hubiera más de uno. También acá debe respetarse el path relativo al directorio de tu proyecto y este archivo debe
    estar correctamente listado en MANIFEST. Este archivo se instalará en el path establecido en el campo install_data de setup.cfg

    El parámetro data_files, debe contener la lista completa de archivos a instalar.
    Cada elemento de esta lista, es una tupla de dos elementos.
    El primer elemento es el directorio destino de los archivos listados en el segundo elemento de la tupla.

    Por ejemplo, para el archivo desktop:

        ("/usr/share/applications/", ["JAMediaTube.desktop"])

    Lo que se establece allí es que todos los archivos de la lista que ocupan el segundo lugar de la tupla (en este caso solo JAMediaTube.desktop),
    se instalarán en /usr/share/applications/

    Si por ejemplo, tuviera una lista de íconos a instalar y quisiera instalarlos dentro de un directorio "Iconos" que a su vez estuviera dentro
    del path de instalación de mi proyecto, escribiría:

        ("Iconos/",[
            "Iconos/JAMedia.svg",
            "Iconos/yt_videos_black.png",
            "Iconos/JAMedia-help.svg",
            etc . . .
            ])

    Básicamente ahí estoy diciendo que cuando mi aplicación se instale, en el path en que se instaló, debe crearse el directorio "Iconos" y dentro
    deben copiarse todos los íconos listados.

    De modo que si el archivo setup.cfg dice:

        install_data=/usr/local/share/JAMediaTube

    Mis íconos se copiarán en:

        /usr/local/share/JAMediaTube/Iconos/

    Resumen:
        El elemento de la izquierda de la tupla, determina el path destino de los elementos de la derecha de la tupla.
        El path definitivo, depende de lo que se establezca en el campo install_data de setup.cfg

    Nota:
        En el archivo setup.py puedes escribir el código que desees fuera de la llamada a la función setup de distutils.core.
        Esto es útil para establecer permisos de archivos o limpiar directorios antes o después de la instalación de tu aplicación.

Construcción del paquete distribuible:

    Una vez escritos los archivos necesarios, hay que construir el instalador y el distribuible.
    El archivo distribuible es un archivo tar.gz que contiene al instalador.
    Se pueden construir por separado pero no tiene mucho sentido hacerlo de esa forma ya que se pueden hacer ambas cosas en un solo paso.

    Para construir el paquete definitivo debes ejecutar:

        python setup.py sdist

    Con ese sencillo paso, se construirá el paquete tar.gz que debes distribuir en internet para que puedan instalar tu aplicación.
    Quien desee utilizarlo, luego de descargarlo debe descomprimirlo, abrir una terminal, entrar en el directorio donde descomprimió el paquete y ejecutar:

        sudo python setup.py install

    Si no lanza ningún error, la instalación estará completa y la aplicación lista para ser utilizada.

    Nota:
        Para desinstalar la aplicación, el usuario debe borrar el directorio donde fue instalada, los lanzadores y el archivo .desktop, a menos que crees un script
        que haga todo esto y lo distribuyas con tu aplicación. En este caso, ese escript debie incluirse en el parámetro "scripts" de la función "setup" de "setup.py"
        Cuando ejecutas: python setup.py, puedes pasarle varios parámetros, acá solo se nombraron install y sdist, consulta la web de python para aprender sobre esto.

Sobre JAMediaEditor:

    Como habrás visto, resulta bastante engorroso construir este instalador, sobre todo si tu proyecto es muy complejo.
    Por eso JAMediaEditor automatiza todo este proceso analizando el directorio de tu proyecto y presentandote los archivos de instalación para que tu corrijas, agregues
    o quites lo que desees de ellos. Por defecto, JAMediaEditor debiera construir este instalador correctamente sin que cambies nada y ese instalador debiera funcionar
    sin ningún tipo de problemas. Si este no fuera el caso, asegúrate que no has hecho cambios que contengan errores en los archivos del instalador.

    Si quieres aprender más sobre esta forma de hacer un instalador, puedes crear un proyecto pequeño en JAMediaEditor y construir este instalador en él, luego
    descomprime el tar.gz resulante y analiza los archivos involucrados (MANIFEST, setup.py, setup.cfg, el lanzador y el .desktop).

    Si quieres analizar la forma en que JAMediaEditor arma este instalador, mira el archivo JAMediaEditor/Instaladores/ApiProyecto.py dentro del path de instalación
    de JAMediaEditor.
"""


SUGAR = """
El Instalador Sugar:

    Un Instalador Sugar es un simple archivo zip que contiene un directorio con toda la aplicación a instalar.

    Ese zip debe nombrarse de la siguiente forma:

        NombreAplicación.activity.xo

    Es decir que para JAMediaEditor, sería:

        JAMediaEditor.activity.xo

    Para este ejemplo, cuando JAMediaEditor se instale en sugar, se creará un directorio JAMediaEditor.activity dentro de /home/olpc/Activities/
    y dentro se copiarán todos los archivos y directorios de la aplicación.

Crear una Aplicación Sugar:

    Para crear una aplicación Sugar, debes crear un directorio con el nombre de la aplicación y agregarle ".activity".
    Dentro, desarrollas toda tu aplicación, tomando en cuenta que el archivo main de tu proyecto, debe estar en ese directorio y
    debe contener una clase que herede de sugar.activity.activity.Activity

    Un ejemplo de esta clase principal es:

        from sugar.activity.activity import Activity

        class Bichos(Activity):

            def __init__(self, handle):

                Activity.__init__(self, handle, False)

    También dentro de ese directorio, debe haber un archivo setup.py que debe contener lo siguiente:

        #!/usr/bin/python
        # -*- coding: utf-8 -*-

        from sugar.activity import bundlebuilder
        bundlebuilder.start()

    Además, dentro de ese mismo directorio, debe haber otro directorio llamado "activity", el cual debe contener:

        el ícono de la aplicación en formato svg y de 50 x 50 pixeles.
        un archivo llamado activity.info

    El archivo activity.info es como un .desktop (ver Ayuda sobre "Instaladores en General") con contenido similar al siguiente:

        [Activity]
        name = Bichos
        bundle_id = org.laptop.Bichos
        exec = sugar-activity SugarBichos.Bichos
        icon = Bichos
        activity_version = 1
        show_launcher = yes

    Los campos verdaderamente importantes en este archivo son bundle_id, exec y activity_version.

        bundle_id:

            Es un identificador único para la aplicación.
            En el sitio de descargas de Sugar nunca podrás subir un paquete .xo que contenga en este campo el mismo valor que
            otra aplicación existente. Tampoco podrás subir una actualización de una aplicación que no contenga el mismo identificador que
            el explicitado en el sitio de descargas para esa aplicación.

        exec:

            Refiere al archivo y clase principal de la aplicación (SugarBichos.Bichos)
            Si estableces mal este campo, la aplicación no iniciará luego de instalada.

        activity_version:

            Este campo es importante al momento de descargar e instalar una aplicación en sugar.
            Esto se debe a que sugar solo instala versiones más nuevas de una aplicación que ya tiene instalada.

    Resumiendo, la estructura de tu proyecto sugar debe contener:

        MiAplicacion.activity/
            activity/
                icono.svg
                activity.info
            setup.py
            ArchivoPrincipal.py (con Clase Principal que herede de sugar.activity.activity.Activity)

        Luego de tener todo esto en orden, debes:

            Establecer los permisos de archivos y directorios en forma correcta.
                Cada archivo debe tener los permisos 644 y los directorios 755, incluso el directorio principal de la aplicación.
            Luego comprimes el directorio principal de tu aplicación en un archivo zip.
            Le cambias la extensión a .xo.
            Al archivo .xo, le das los permisos 755 y estará listo para subirlo a internet y distribuirlo o instalarlo en sugar.

Sobre JAMediaEditor:

    JAMediaEditor realiza todo este proceso en forma automática pero el resultado depende de que tu establezcas correctamente el main
    del proyecto y toda la información del archivo activity.info.
    JAMediaEditor solo intenta guiarte en cada instalador creando plantillas de los archivos necesarios, pero nunca modificará los archivos de tu proyecto.
"""


def get_help(help):
    if help == "Programar Clase 0":
        arch = open(os.path.join(BASEPATH, "ProgramarPython", "001.txt"), "r")
        text = arch.read()
        arch.close()
        return text

    elif help == "help instaladores":
        return INSTALADORES
    elif help == "help deb":
        return DEB
    elif help == "help rmp":
        return ""
    elif help == "help python":
        return PYTHON
    elif help == "help sin root":
        return SINROOT
    elif help == "help sugar":
        return SUGAR
    else:
        return ""
