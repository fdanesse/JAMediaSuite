//valac --pkg gtk+-3.0 --pkg gdk-x11-3.0 --pkg gstreamer-0.10 --pkg gstreamer-interfaces-0.10 UbuntuRadio.vala

using Gtk;      //--pkg gtk+-3.0
using Gdk;
//using GLib;   Se importa siempre por default

public class UbuntuRadio : Gtk.Window {
    /* Ventana Principal */


    public UbuntuRadio () {
        /* Constructor default */

        this.title = "Ubuntu Radio";
        this.set_default_icon_from_file("Iconos/ubuntu_radio.svg");
		this.window_position = Gtk.WindowPosition.CENTER;
		this.set_default_size (200, 400);
		this.set_opacity(0.5);
		this.set_decorated(false);
		//this.set_resizable(true);
        this.set("border_width", 5);

        this.destroy.connect (this.exit);

        this.show_all();
    }

    private void exit(){
        /* Sale de la aplicación */

        Gtk.main_quit();
    }

}


public static int main (string[] args) {
    /* main de la aplicación */

    Gtk.init (ref args);

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
