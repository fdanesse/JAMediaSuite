/*
   UbuntuRadio.vala por:
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

Compilar con:
    valac --pkg glib-2.0 --pkg gio-2.0 --pkg libsoup-2.4 \
    --pkg gtk+-3.0 --pkg gdk-3.0 --pkg gdk-x11-3.0 --pkg gstreamer-1.0 \
    --pkg json-glib-1.0 \
    UbuntuRadio.vala Widgets.vala RadioPlayer.vala \
    RadioRecord.vala Globales.vala

Para Utilizar gstreamer 0.10 cambiar: --pkg gstreamer-1.0
por: --pkg gstreamer-0.10 --pkg gstreamer-interfaces-0.10
*/

//using GLib;   Se importa siempre por default
using Gtk;      //--pkg gtk+-3.0
using Gdk;
using Gst;      //--pkg gstreamer-1.0


public class UbuntuRadio : Gtk.Window {
    /*
    Ventana Principal
    */

    private MenuUbuntuRadio menu = new MenuUbuntuRadio();
    private ItemPlayer itemplayer = new ItemPlayer();
    private ItemRecord itemrecord = new ItemRecord();
    private Gtk.ScrolledWindow scroll_list = new Gtk.ScrolledWindow(null, null);
    private Lista lista = new Lista();

    public UbuntuRadio () {

        this.title = "Ubuntu Radio";
        try {
            Gtk.Window.set_default_icon_from_file(
                "Iconos/ubuntu_radio.svg");
        }
        catch{
        }
		this.window_position = Gtk.WindowPosition.CENTER;
		this.set_default_size (200, 400);
		this.set_opacity (0.5);
		this.set_decorated(false);
		//this.set_resizable(true);
        this.set("border_width", 5);

        Gtk.Box box = new Gtk.Box (Gtk.Orientation.VERTICAL, 0);

        this.scroll_list.set_policy (
            PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
        this.scroll_list.add (this.lista);

        box.pack_start (this.menu, false, true, 0);
        box.pack_start (this.itemplayer, false, true, 0);
        box.pack_start (this.itemrecord, false, true, 0);
        box.pack_start (this.scroll_list, true, true, 0);

        this.add (box);

        this.menu.radios.connect (this.radios);
        this.menu.configurar.connect (this.configurar);
        this.menu.creditos.connect (this.creditos);
        this.menu.actualizar.connect (this.actualizar);
        this.menu.salir.connect (this.exit);

        this.lista.play.connect (this.do_play_in_list);
        this.lista.record.connect (this.do_record_in_list);
        this.destroy.connect (this.exit);

        this.show_all();

        this.load_list ();
    }

    private void load_list () {
        /*
        Carga la lista de streamings
        */

        set_listas_default();
        SList<Streaming> streaming_list = get_streamings();
        this.lista.set_lista(streaming_list);
    }

    private void do_play_in_list(string val1, string val2, string val3){
        /*
        Cuando se hace reproducir en un elemento de la lista
        */

        this.itemplayer.load(val1, val2, val3);
    }

    private void do_record_in_list(string val1, string val2, string val3){
        /*
        Cuando se hace grabar en un elemento de la lista
        */

        this.itemrecord.load(val1, val2, val3);
    }

    private void radios(){

        if (this.scroll_list.get_visible()){
            this.scroll_list.hide();
            this.resize (200, 10);
        }
        else{
            this.scroll_list.show();
            this.resize (200, 400);
        }
    }

    private void configurar(){
    }

    private void creditos(){

        Creditos credits = new Creditos(this, "");
        credits.run();
        credits.destroy();
    }

    private void actualizar(){

        Descargas descarga = new Descargas(this, "");
        descarga.run();
    }

    private void exit(){

        this.itemplayer.stop();
        this.itemrecord.stop();
        Gtk.main_quit();
    }

}


public static int main (string[] args) {

    try {
        Gtk.init (ref args);
        Gst.init(ref args);

        var screen = Gdk.Screen.get_default();
        var css_provider = new Gtk.CssProvider();
        string style_path = "Estilo.css";
        css_provider.load_from_path(style_path);
        Gtk.StyleContext.add_provider_for_screen(
            screen, css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER);

        new UbuntuRadio ();
        Gtk.main ();
        return 0;
    }
    catch {
        return 1;
    }
}
