//valac --pkg gtk+-3.0 --pkg gdk-x11-3.0 --pkg gstreamer-0.10 --pkg gstreamer-interfaces-0.10 UbuntuRadio.vala

//using GLib;   Se importa siempre por default
using Gtk;      //--pkg gtk+-3.0
using Gdk;
using Gst;      //--pkg gstreamer-1.0

public class UbuntuRadio : Gtk.Window {
    /* Ventana Principal */

    private MenuUbuntuRadio menu = new MenuUbuntuRadio();
    private ItemPlayer itemplayer = new ItemPlayer();
    private Gtk.ScrolledWindow scroll_list = new Gtk.ScrolledWindow(null, null);
    private Lista lista = new Lista();

    public UbuntuRadio () {
        /* Constructor default */

        this.title = "Ubuntu Radio";
        try {
            Gtk.Window.set_default_icon_from_file(
                "Iconos/ubuntu_radio.svg");
        }
        catch{
        }
		this.window_position = Gtk.WindowPosition.CENTER;
		this.set_default_size (200, 400);
		this.set_opacity(0.5);
		this.set_decorated(false);
		//this.set_resizable(true);
        this.set("border_width", 5);

        Gtk.Box box = new Gtk.Box (Gtk.Orientation.VERTICAL, 0);

        this.scroll_list.set_policy (
            PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
        this.scroll_list.add (this.lista);

        box.pack_start (this.menu, false, true, 0);
        box.pack_start (this.itemplayer, false, true, 0);
        box.pack_start (this.scroll_list, true, true, 0);

        this.add (box);

        this.menu.salir.connect (this.exit);
        this.lista.selected.connect (this.do_clicked_in_list);
        this.destroy.connect (this.exit);

        this.show_all();

        this.load_list ();
    }

    private void load_list () {
        /* Carga la lista de streamings */

        //Lista compleja
        Streaming [] streaming_list = new Streaming [3];

        streaming_list[0] = new Streaming(
            "", "RauteMusik JaM (Alemania)",
            "http://main-office.rautemusik.fm");
        streaming_list[1] = new Streaming(
            "", "Oceano FM 93.9 (Montevideo - Uruguay)",
            "http://radio1.oceanofm.com:8010/");
        streaming_list[2] = new Streaming(
            "", "Azul FM 101.9 (Montevideo - Uruguay)",
            "http://74.222.5.162:9698/");

        this.lista.set_lista(streaming_list);
    }

    private void do_clicked_in_list(string val1, string val2, string val3){
        /* Cuando se hace doble click en un elemento de la lista */

        //stdout.printf ("%s %s %s\n", val1, val2, val3);

        this.itemplayer.load(val1, val2, val3);
    }

    private void exit(){
        /* Sale de la aplicación */

        this.itemplayer.stop();
        Gtk.main_quit();
    }

}


public static int main (string[] args) {
    /* main de la aplicación */

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
