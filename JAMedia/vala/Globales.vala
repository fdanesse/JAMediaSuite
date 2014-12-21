
using Soup;
using Json;

/*
canales = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-tv-2014'
radios = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-radios-2014'
webcams = 'https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-webcams-2014'


def convert_shelve_to_json(path):
    print "Convert:", path
    import shelve
    _dict = {}
    try:
        archivo = shelve.open(path)
        _dict = dict(archivo)
        archivo.close()
        borrar(path)
        set_dict(path, _dict)
    except:
        pass
    return _dict


def get_dict(path):
    if not os.path.exists(path):
        return {}
    try:
        archivo = codecs.open(path, "r", "utf-8")
        _dict = json.JSONDecoder(encoding="utf-8").decode(archivo.read())
        archivo.close()
    except:
        _dict = convert_shelve_to_json(path)
    return _dict


def set_dict(path, _dict):
    archivo = open(path, "w")
    archivo.write(
        json.dumps(
            _dict,
            indent=4,
            separators=(", ", ":"),
            sort_keys=True))
    archivo.close()


def get_colors(key):
    from gtk import gdk
    _dict = {
        "window": "#ffffff",
        "toolbars": "#778899",
        "widgetvideoitem": "#f0e6aa",
        "drawingplayer": "#000000",
        "naranaja": "#ff6600",
        }
    return gdk.color_parse(_dict.get(key, "#ffffff"))
*/

public bool get_ip(){
    //FIXME: Corregir
    return true;
    /*
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        ret = s.getsockname()[0]
        s.close()
        return bool(ret)
    except:
        return False
    */
    }

/*
def describe_archivo(archivo):
    """
    Devuelve el tipo de un archivo (imagen, video, texto).
    -z, --uncompress para ver dentro de los zip.
    """
    datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
    retorno = ""
    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)
    return retorno


def describe_uri(uri):
    """
    Explica de que se trata el uri, si existe.
    """
    existe = False
    try:
        existe = os.path.exists(uri)
    except:
        return False
    if existe:
        unidad = os.path.ismount(uri)
        directorio = os.path.isdir(uri)
        archivo = os.path.isfile(uri)
        enlace = os.path.islink(uri)
        return [unidad, directorio, archivo, enlace]
    else:
        return False


def describe_acceso_uri(uri):
    """
    Devuelve los permisos de acceso sobre una uri.
    """
    existe = False
    try:
        existe = os.access(uri, os.F_OK)
    except:
        return False
    if existe:
        lectura = os.access(uri, os.R_OK)
        escritura = os.access(uri, os.W_OK)
        ejecucion = os.access(uri, os.X_OK)
        return [lectura, escritura, ejecucion]
    else:
        return False


def borrar(origen):
    try:
        if os.path.isdir(origen):
            shutil.rmtree("%s" % (os.path.join(origen)))
        elif os.path.isfile(origen):
            os.remove("%s" % (os.path.join(origen)))
        else:
            return False
        return True
    except:
        print "ERROR Al Intentar Borrar un Archivo"
        return False


def mover(origen, destino):
    try:
        if os.path.isdir(origen):
            copiar(origen, destino)
            borrar(origen)
            return True
        elif os.path.isfile(origen):
            expresion = "mv \"" + origen + "\" \"" + destino + "\""
            os.system(expresion)
            return True
    except:
        print "ERROR Al Intentar Mover un Archivo"
        return False


def copiar(origen, destino):
    try:
        if os.path.isdir(origen):
            expresion = "cp -r \"" + origen + "\" \"" + destino + "\""
        elif os.path.isfile(origen):
            expresion = "cp \"" + origen + "\" \"" + destino + "\""
        os.system(expresion)
        return True
    except:
        print "ERROR Al Intentar Copiar un Archivo"
        return False

*/

public void make_base_directory(){
    try {
        string home = GLib.Environment.get_variable("HOME");
        string jamedia = GLib.Path.build_filename(home, "JAMediaDatos");
        string archivos = GLib.Path.build_filename(home, "JAMediaDatos", "MisArchivos");
        string datos = GLib.Path.build_filename(home, "JAMediaDatos", "Datos");
        string youtube = GLib.Path.build_filename(home, "JAMediaDatos", "YoutubeVideos");
        string audio = GLib.Path.build_filename(home, "JAMediaDatos", "Audio");
        string video = GLib.Path.build_filename(home, "JAMediaDatos", "Videos");
        string fotos = GLib.Path.build_filename(home, "JAMediaDatos", "Fotos");

        string [] dirlist = {jamedia, archivos, datos, youtube, audio, video, fotos};

        foreach (string dir in dirlist){
            File file = File.new_for_path(dir);
            if(file.query_exists() != true){
                file.make_directory ();
                }
            }
        }
    catch{}
    }


public string get_data_directory(){
    string home = GLib.Environment.get_variable("HOME");
    string datos = GLib.Path.build_filename(home, "JAMediaDatos", "Datos");
    try{
        File file = File.new_for_path(datos);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}
    return datos;
    }


public string get_tube_directory(){
    string home = GLib.Environment.get_variable("HOME");
    string youtube = GLib.Path.build_filename(home, "JAMediaDatos", "YoutubeVideos");
    try{
        File file = File.new_for_path((string) youtube);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}
    return youtube;
    }


public string get_audio_directory(){
    string home = GLib.Environment.get_variable("HOME");
    string audio = GLib.Path.build_filename(home, "JAMediaDatos", "Audio");
    try{
        File file = File.new_for_path((string) audio);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}
    return audio;
    }


public string get_imagenes_directory(){
    string home = GLib.Environment.get_variable("HOME");
    string fotos = GLib.Path.build_filename(home, "JAMediaDatos", "Fotos");
    try{
        File file = File.new_for_path((string) fotos);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}
    return fotos;
    }


public string get_video_directory(){
    string home = GLib.Environment.get_variable("HOME");
    string videos = GLib.Path.build_filename(home, "JAMediaDatos", "Videos");
    try{
        File file = File.new_for_path((string) videos);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}
    return videos;
    }


public string get_my_files_directory(){
    string home = GLib.Environment.get_variable("HOME");
    string archivos = GLib.Path.build_filename(home, "JAMediaDatos", "MisArchivos");
    try{
        File file = File.new_for_path((string) archivos);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}
    return archivos;
    }


public string get_JAMedia_Directory(){
    string home = GLib.Environment.get_variable("HOME");
    string datos = GLib.Path.build_filename(home, "JAMediaDatos", "JAMediaDatos");
    try{
        File file = File.new_for_path((string) datos);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}
    return datos;
    }


/*
def eliminar_streaming(url, lista):
    """
    Elimina un Streaming de una lista de jamedia.
    """
    DIRECTORIO_DATOS = get_data_directory()

    if lista == "Radios":
        path = os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia")
    elif lista == "TVs":
        path = os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")
    elif lista == "JAM-Radio":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia")
    elif lista == "JAM-TV":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia")
    elif lista == "WebCams":
        path = os.path.join(DIRECTORIO_DATOS, "JAMediaWebCams.JAMedia")
    else:
        return

    _dict = get_dict(path)
    cambios = False
    items = _dict.items()
    for item in items:
        if url == str(item[1]):
            cambios = True
            del(_dict[item[0]])
    if cambios:
        set_dict(path, _dict)


def add_stream(tipo, item):
    """
    Agrega un streaming a la lista correspondiente de jamedia.
    """
    DIRECTORIO_DATOS = get_data_directory()
    if "TV" in tipo or "Tv" in tipo:
        path = os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia")
    elif "Radio" in tipo:
        path = os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia")
    else:
        return
    _dict = get_dict(path)
    _dict[item[0].strip()] = item[1].strip()
    set_dict(path, _dict)


def set_listas_default():
    """
    Crea las listas para JAMedia si es que no existen y
    llena las default en caso de estar vacías.
    """
    DIRECTORIO_DATOS = get_data_directory()

    listas = [
        os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "MisRadios.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "MisTvs.JAMedia"),
        os.path.join(DIRECTORIO_DATOS, "JAMediaWebCams.JAMedia")
        ]

    for archivo in listas:
        if not os.path.exists(archivo):
            jamedialista = set_dict(archivo, {})
            os.chmod(archivo, 0666)

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    _dict = get_dict(os.path.join(DIRECTORIO_DATOS, "JAMediaTV.JAMedia"))
    lista = _dict.items()

    if not lista:
        try:
            # Streamings JAMediatv
            lista_canales = descarga_lista_de_streamings(canales)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
                "JAMediaTV.JAMedia"), lista_canales)
        except:
            print "Error al descargar Streamings de TV."

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    _dict = get_dict(os.path.join(DIRECTORIO_DATOS, "JAMediaRadio.JAMedia"))
    lista = _dict.items()

    if not lista:
        try:
            # Streamings JAMediaradio
            lista_radios = descarga_lista_de_streamings(radios)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
                "JAMediaRadio.JAMedia"), lista_radios)
        except:
            print "Error al descargar Streamings de Radios."

    # verificar si las listas están vacías,
    # si lo están se descargan las de JAMedia
    _dict = get_dict(os.path.join(DIRECTORIO_DATOS, "JAMediaWebCams.JAMedia"))
    lista = _dict.items()

    if not lista:
        try:
            # Streamings JAMediaWebCams
            lista_webcams = descarga_lista_de_streamings(webcams)
            guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
                "JAMediaWebCams.JAMedia"), lista_webcams)
        except:
            print "Error al descargar Streamings de WebCams."


def get_streaming_default():
    """
    Descarga los streaming desde la web de JAMedia.
    """
    DIRECTORIO_DATOS = get_data_directory()

    try:
        # Streamings JAMediatv
        lista_canales = descarga_lista_de_streamings(canales)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaTV.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaTV.JAMedia"), lista_canales)
    except:
        print "Error al descargar Streamings de TV."

    try:
        # Streamings JAMediaradio
        lista_radios = descarga_lista_de_streamings(radios)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaRadio.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaRadio.JAMedia"), lista_radios)
    except:
        print "Error al descargar Streamings de Radios."

    try:
        # Streamings JAMediaWebCams
        lista_webcams = descarga_lista_de_streamings(webcams)
        clear_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaWebCams.JAMedia"))
        guarda_lista_de_streamings(os.path.join(DIRECTORIO_DATOS,
            "JAMediaWebCams.JAMedia"), lista_webcams)
    except:
        print "Error al descargar Streamings de webcams."


def descarga_lista_de_streamings(url):
    """
    Recibe la web donde se publican los streamings de radio o televisión de
    JAMedia y devuelve la lista de streamings.

    Un streaming se representa por una lista:
        [nombre, url]
    """

    print "Conectandose a:", url, "\n\tDescargando Streamings . . ."

    import urllib

    cont = 0
    urls = []
    cabecera = 'JAMedia Channels:'
    streamings = []

    try:
        web = urllib.urlopen(url)
        t = web.readlines()
        web.close()

        text = ""
        for l in t:
            text = "%s%s" % (text, l)

        streamings_text = text.split(cabecera)[1]
        streamings_text = streamings_text.replace('</div>', "")
        streamings_text = streamings_text.replace('/>', "")
        lista = streamings_text.split('<br')

        for s in lista:
            if not len(s.split(",")) == 2:
                continue

            name, direc = s.split(",")
            name = name.strip()
            direc = direc.strip()

            if not direc in urls:
                urls.append(direc)
                stream = [name, direc]
                streamings.append(stream)
                cont += 1

            else:
                print "Direccion Descartada por Repetición:", name, direc

        print "\tSe han Descargado:", cont, "Estreamings.\n"
        return streamings

    except:
        return []


def clear_lista_de_streamings(path):
    set_dict(path, {})


def guarda_lista_de_streamings(path, items):
    """
    Recibe el path a un archivo de lista de streamings
    de JAMedia y una lista de items [nombre, url] y los almacena
    en el archivo.
    """
    _dict = get_dict(path)
    for item in items:
        _dict[item[0].strip()] = item[1].strip()
    set_dict(path, _dict)
*/


public SList<Streaming> get_streamings(string path){
    SList<Streaming> streaming_list = new SList<Streaming> ();

    Json.Parser parser = new Json.Parser();
    parser.load_from_file(path);
    Json.Node node = parser.get_root();
    unowned Json.Object obj = node.get_object();

    foreach (unowned string name in obj.get_members()){
        unowned Json.Node item = obj.get_member(name);
        Streaming streaming = new Streaming(name, item.get_string());
        streaming_list.append(streaming);
    }
    return streaming_list;
}


/*
def stream_en_archivo(streaming, path):
    """
    Verifica si un streaming está en
    un archivo de lista de jamedia determinado.
    """
    _dict = get_dict(path)
    items = _dict.values()
    for item in items:
        if streaming == item:
            return True
    return False

*/


public Gtk.SeparatorToolItem get_separador(bool draw, int ancho, bool expand){
    Gtk.SeparatorToolItem separador = new Gtk.SeparatorToolItem();
    separador.set_draw(draw);
    separador.set_size_request(ancho, -1);
    separador.set_expand(expand);
    return separador;
    }


public Gtk.ToolButton get_button(string archivo, bool flip, Gdk.PixbufRotation rotacion, int pixels, string tooltip){
    Gdk.Pixbuf pix = new Gdk.Pixbuf.from_file_at_size(archivo, pixels, pixels);
    Gdk.Pixbuf pixbuf = null;
    if (flip == true){
        // false espeja en la vertical
        pixbuf = pix.flip(flip);
        }
    else{
        pixbuf = pix;
        }
    pixbuf = pixbuf.rotate_simple(rotacion);
    Gtk.Image img = new Gtk.Image.from_pixbuf(pixbuf);
	Gtk.ToolButton button = new Gtk.ToolButton(img, null);
	button.set_tooltip_text(tooltip);
    return button;
    }
