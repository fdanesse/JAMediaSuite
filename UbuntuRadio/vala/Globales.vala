/*
   Globales.vala por:
   Flavio Danesse <fdanesse@gmail.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

valac --pkg gio-2.0 Necesario.
*/

using Soup;     //--pkg libsoup-2.4
using Json;     //--pkg json-glib-1.0

//def set_estilo(dict_colors):
//def get_estilo():
//def get_config():
//def load_estilo(path):

public void make_base_directory(){
    /*
    Crea toda la estructura de Directorios necesaria para
    Ubuntu Radio, en el path de JAMedia.
    */

    try {
        string home = GLib.Environment.get_variable("HOME");

        string jamedia = GLib.Path.build_filename(
            home, "JAMediaDatos");

        string archivos = GLib.Path.build_filename(
            home, "JAMediaDatos", "MisArchivos");

        string datos = GLib.Path.build_filename(
            home, "JAMediaDatos", "Datos");

        string [] dirlist = {jamedia, archivos, datos};

        foreach (string dir in dirlist){
            File file = File.new_for_path(dir);

            if(file.query_exists() != true) {
                file.make_directory ();
            }
        }
    }
    catch{
    }
}

public string get_data_directory(){
    /*
    Devuelve el Directorio de Datos de JAMedia.
    */

    string home = GLib.Environment.get_variable("HOME");
    string datos = GLib.Path.build_filename(
        home, "JAMediaDatos", "Datos");

    try{
        File file = File.new_for_path(datos);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}

    return datos;
}

public string get_my_files_directory(){
    /*
    Devuelve el directorio mis archivos, (donde se guardan las grabaciones).
    */

    string home = GLib.Environment.get_variable("HOME");
    string archivos = GLib.Path.build_filename(
        home, "JAMediaDatos", "MisArchivos");

    try{
        File file = File.new_for_path((string) archivos);
        if(file.query_exists() != true){
            make_base_directory();
            }
        }
    catch{}

    return archivos;
}


public SList<Streaming> get_streamings(){
    /*
    Devuelve la lista de Streamings
    */

    SList<Streaming> streaming_list = new SList<Streaming> ();

    string home = GLib.Environment.get_variable("HOME");
    string radios = GLib.Path.build_filename(
        home, "JAMediaDatos", "Datos", "JAMediaRadio.json");

    Json.Parser parser = new Json.Parser();
    parser.load_from_file(radios);
    Json.Node node = parser.get_root();
    unowned Json.Object obj = node.get_object();

    foreach (unowned string name in obj.get_members()){
        unowned Json.Node item = obj.get_member(name);
        Streaming streaming = new Streaming("", name, item.get_string());
        streaming_list.append(streaming);
    }

    return streaming_list;
}

public SList<Streaming> descarga_lista_de_streamings(){
    /*
    Descarga la lista desde la web de JAMedia.
    Esta función solo se llama desde get_streaming_default
    */

    string url = "https://sites.google.com/site/sugaractivities/jamediaobjects/jam/lista-de-radios-2014";
    stdout.printf("Conectandose a: %s \n\tDescargando Streamings . . .", url);

    //SList<string> urls = new SList<string> ();
    string cabecera = "JAMedia Channels:";
    SList<Streaming> streamings = new SList<Streaming> ();

    try{
        Soup.SessionSync session = new Soup.SessionSync ();
        Soup.Request request = session.request (url);
        InputStream stream = request.send ();
        DataInputStream data_stream = new DataInputStream(stream);

        string? line;
        string text = "";
		while ((line = data_stream.read_line()) != null){
		    text += line;
			}

        string streamings_text = text.split(cabecera)[1];
        string streamings_text1 = streamings_text.replace(
            "</div>", "").replace("/>", "").replace("<div>", "");
        string [] lista = streamings_text1.split("<br");

        foreach (string s in lista){
            int length = s.split(",").length;

            if (length != 2){
                continue;
            }

            else{
                string name = s.split(",")[0].strip();
                string direc = s.split(",")[1].strip();

                //FIXME: No es posible en SList
                //if (direc in urls){
                //    stdout.printf("Direccion Descartada por Repetición: %s, %s\n", name, direc);
                //}
                //else{
                    //urls.append(direc);
                    Streaming streaming = new Streaming("", name, direc);
                    streamings.append(streaming);
                //}
            }
        }

        //stdout.printf("\tSe han Descargado: %s Estreamings.\n",
        //    (string) streamings.length);
        }

    catch (Error e){
        stderr.printf ("Error: %s\n", e.message);
        }

    return streamings;
}

public void set_listas_default(){
    /*
    Si la lista de strimings no se encuentra, se descarga.
    */

    string datos = get_data_directory();
    string home = GLib.Environment.get_variable("HOME");
    string radios = GLib.Path.build_filename(
        home, "JAMediaDatos", "Datos", "JAMediaRadio.json");

    File file = File.new_for_path(radios);
    if(file.query_exists() != true){
        get_streaming_default();
    }
}


public void get_streaming_default(){
    /*
    Descarga la lista de streamings de JAMedia
    */

    try{
        string DATOS = get_data_directory();
        SList<Streaming> lista_radios = descarga_lista_de_streamings();

        Json.Builder builder = new Json.Builder();
	    builder.begin_object ();

	    foreach (Streaming s in lista_radios){
	        builder.set_member_name(s.nombre);
	        builder.add_string_value(s.url);
	    }

	    builder.end_object();

        //FIXME: No se entiende pero está acá :P
        //https://mail.gnome.org/archives/commits-list/2012-September/msg03363.html

        Json.Generator generator = new Json.Generator();
	    Json.Node root = builder.get_root();
	    generator.set_root(root);
	    string str = generator.to_data(null);

        string home = GLib.Environment.get_variable("HOME");
        string jamedia = GLib.Path.build_filename(
            home, "JAMediaDatos", "Datos", "JAMediaRadio.json");

        var file = File.new_for_path(jamedia);
        var file_stream = file.create(FileCreateFlags.PRIVATE);
        var data_stream = new DataOutputStream(file_stream);
        data_stream.put_string(str);
    }
    catch{
        stdout.printf("Error al descargar Streamings de Radios.");
    }
}

//def stream_en_archivo(streaming, path):
//def eliminar_streaming(url, lista):
