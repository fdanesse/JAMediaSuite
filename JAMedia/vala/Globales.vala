
using Soup;
using Json;


private void __make_base_directory(){
    // FIXME: DirUtils.create_with_parents(folder, 0666)
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
            GLib.File file = GLib.File.new_for_path(dir);
            if (file.query_exists() != true){
                file.make_directory ();
                }
            }
        }
    catch{}
    }


private SList<Streaming> __descarga_lista_de_streamings(string url){
    GLib.stdout.printf("Conectandose a: %s\n", url);
    GLib.stdout.printf("    Descargando Streamings . . .\n");
    GLib.stdout.flush();

    string cabecera = "JAMedia Channels:";
    SList<Streaming> streamings = new SList<Streaming>();
    int contador = 0;

    try{
        Soup.SessionSync session = new Soup.SessionSync();
        Soup.Request request = session.request(url);
        InputStream stream = request.send();
        DataInputStream data_stream = new DataInputStream(stream);

        string? line;
        string text = "";
        while ((line = data_stream.read_line()) != null){
            text += line;
            }

        string streamings_text = text.split(cabecera)[1];
        string streamings_text1 = streamings_text.replace("</div>", "").replace("/>", "").replace("<div>", "");
        string [] lista = streamings_text1.split("<br");

        foreach (string s in lista){
            int length = s.split(",").length;

            if (length != 2){
                continue;
                }
            else{
                string name = s.split(",")[0].strip();
                string direc = s.split(",")[1].strip();

                Streaming streaming = new Streaming(name, direc);
                streamings.append(streaming);
                contador ++;
                }
            }

        GLib.stdout.printf("   Se han Descargado: %i Estreamings.\n", contador);
        GLib.stdout.flush();
        }

    catch (Error e){
        GLib.stderr.printf ("Error: %s\n", e.message);
        GLib.stdout.flush();
        }

    return streamings;
    }


private void __guarda_lista_de_streamings(string path, SList<Streaming> items){
    GLib.File f = GLib.File.parse_name(path);
    if (f.query_exists()){
        GLib.FileUtils.remove(path);
        }

    Json.Builder builder = new Json.Builder();
    builder.begin_object ();
    foreach (Streaming s in items){
        builder.set_member_name(s.nombre);
        builder.add_string_value(s.path);
        }
    builder.end_object();

    //No se entiende pero está acá :P
    //https://mail.gnome.org/archives/commits-list/2012-September/msg03363.html

    Json.Generator generator = new Json.Generator();
    Json.Node root = builder.get_root();
    generator.set_root(root);
    string str = generator.to_data(null);

    var file = GLib.File.new_for_path(path);
    var file_stream = file.create(FileCreateFlags.PRIVATE);
    var data_stream = new DataOutputStream(file_stream);
    data_stream.put_string(str);
    }


public void borrar(string origen){
    GLib.FileUtils.remove(origen);
    }


public void mover(string origen, string dest){
    GLib.File file1 = GLib.File.parse_name(origen);
    string destino = GLib.Path.build_filename(dest, GLib.Path.get_basename(origen));
    GLib.File file2 = GLib.File.parse_name(destino);
    file1.move(file2, GLib.FileCopyFlags.OVERWRITE, null, null);
    }


public void copiar(string origen, string dest){
    GLib.File file1 = GLib.File.parse_name(origen);
    string destino = GLib.Path.build_filename(dest, GLib.Path.get_basename(origen));
    GLib.File file2 = GLib.File.parse_name(destino);
    file1.copy(file2, GLib.FileCopyFlags.OVERWRITE, null, null);
    }


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


public string get_data_directory(){
    string home = GLib.Environment.get_variable("HOME");
    string datos = GLib.Path.build_filename(home, "JAMediaDatos", "Datos");
    try{
        File file = File.new_for_path(datos);
        if(file.query_exists() != true){
            __make_base_directory();
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
            __make_base_directory();
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
            __make_base_directory();
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
            __make_base_directory();
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
            __make_base_directory();
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
            __make_base_directory();
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
            __make_base_directory();
            }
        }
    catch{}
    return datos;
    }


public bool eliminar_streaming(Streaming stream, string lista){
    string data = get_data_directory();
    string path = null;

    if (lista == "Radios"){
        path = GLib.Path.build_filename(data, "MisRadios.JAMedia");
        }
    else if (lista == "TVs"){
        path = GLib.Path.build_filename(data, "MisTvs.JAMedia");
        }
    else if (lista == "JAM-Radio"){
        path = GLib.Path.build_filename(data, "JAMediaRadio.JAMedia");
        }
    else if (lista == "JAM-TV"){
        path = GLib.Path.build_filename(data, "JAMediaTV.JAMedia");
        }
    else if (lista == "WebCams"){
        path = GLib.Path.build_filename(data, "JAMediaWebCams.JAMedia");
        }
    else{
        return false;
        }

    SList<Streaming> streaming_list = new SList<Streaming>();
    SList<Streaming> streamings = get_streamings(path);

    foreach (Streaming stream1 in streamings){
        if (stream1.path != stream.path){
            streaming_list.append(stream1);
            }
        }

    __guarda_lista_de_streamings(path, streaming_list);

    GLib.stdout.printf("Streaming Eliminado: %s de: %s\n", stream.path, lista);
    GLib.stdout.flush();
    return true;
    }


public bool add_streamx(string lista, Streaming stream){
    string data = get_data_directory();
    string path = null;
    if ("TV" in lista || "Tv" in lista){
        path = GLib.Path.build_filename(data, "MisTvs.JAMedia");
        }
    else if ("Radio" in lista){
        path = GLib.Path.build_filename(data, "MisRadios.JAMedia");
        }
    else{
        return false;
        }
    SList<Streaming> streamings = get_streamings(path);
    streamings.append(stream);
    __guarda_lista_de_streamings(path, streamings);
    return true;
    }


public void set_listas_default(){

    string data = get_data_directory();

    string a = GLib.Path.build_filename(data, "JAMediaRadio.JAMedia");
    string b = GLib.Path.build_filename(data, "JAMediaTV.JAMedia");
    string c = GLib.Path.build_filename(data, "MisRadios.JAMedia");
    string d = GLib.Path.build_filename(data, "MisTvs.JAMedia");
    string e = GLib.Path.build_filename(data, "JAMediaWebCams.JAMedia");

    string [] lista = {a, b, c, d, e};

    foreach (string path in lista){
        GLib.File file = GLib.File.parse_name(path);
        if (file.query_exists() == false){
            Json.Builder builder = new Json.Builder();
            builder.begin_object ();
            builder.end_object();
            Json.Generator generator = new Json.Generator();
            Json.Node root = builder.get_root();
            generator.set_root(root);
            string str = generator.to_data(null);
            var file_stream = file.create(FileCreateFlags.PRIVATE);
            var data_stream = new DataOutputStream(file_stream);
            data_stream.put_string(str);
            }
        }
    }


public void download_streamings(){

    string data = get_data_directory();

    string a = GLib.Path.build_filename(data, "JAMediaRadio.JAMedia");
    string b = GLib.Path.build_filename(data, "JAMediaTV.JAMedia");
    string c = GLib.Path.build_filename(data, "JAMediaWebCams.JAMedia");

    SList<Streaming> radios = __descarga_lista_de_streamings("https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-radios-2014");
    SList<Streaming> canales = __descarga_lista_de_streamings("https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-tv-2014");
    SList<Streaming> cams = __descarga_lista_de_streamings("https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-webcams-2014");

    __guarda_lista_de_streamings(a, radios);
    __guarda_lista_de_streamings(b, canales);
    __guarda_lista_de_streamings(c, cams);
    }


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


public bool stream_en_archivo(string streaming, string path){
    SList<Streaming> streaming_list = get_streamings(path);
    foreach (Streaming stream in streaming_list){
        if (stream.path == streaming){
            return true;
            }
        }
    return false;
    }


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
