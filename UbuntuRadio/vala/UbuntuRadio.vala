//valac --pkg gtk+-3.0 --pkg gdk-x11-3.0 --pkg gstreamer-0.10 --pkg gstreamer-interfaces-0.10 UbuntuRadio.vala

//using GLib;   Se importa siempre por default
using Gtk;      //--pkg gtk+-3.0
using Gdk;
using Gst;      //--pkg gstreamer-1.0

public class UbuntuRadio : Gtk.Window {
    /* Ventana Principal */

    private MenuUbuntuRadio menu = new MenuUbuntuRadio();
    private ItemPlayer itemplayer = new ItemPlayer();

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

        Gtk.Box box = new Gtk.Box (Gtk.Orientation.VERTICAL, 0);

        box.pack_start (this.menu, false, true, 0);
        box.pack_start (this.itemplayer, false, true, 0);

        this.add (box);

        this.menu.salir.connect (this.exit);
        this.destroy.connect (this.exit);

        this.show_all();
    }

    private void exit(){
        /* Sale de la aplicación */

        this.itemplayer.stop();
        Gtk.main_quit();
    }

}


public static int main (string[] args) {
    /* main de la aplicación */

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
