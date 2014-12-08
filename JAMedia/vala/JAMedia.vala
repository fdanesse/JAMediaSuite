/*
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


public class JAMedia : Gtk.Window{

    public JAMedia(){

        this.title = "JAMedia";
		this.window_position = Gtk.WindowPosition.CENTER;
		this.set_default_size(640, 480);
		this.set_resizable(true);
        this.set("border_width", 2);
        try {
            Gtk.Window.set_default_icon_from_file(
                "Iconos/JAMedia.svg");
        }
        catch(Error e) {
            stderr.printf ("No se Encontró el Ícono: %s\n", e.message);
        }

        Gtk.Box box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        this.add(box);
        this.show_all();

        this.destroy.connect(this.exit);
    }

    private void exit(){
        Gtk.main_quit();
    }
}


public static int main(string[] args){
    try {
        Gtk.init (ref args);
        new JAMedia();
        Gtk.main();
        return 0;
    }
    catch {
        return 1;
    }
    }
