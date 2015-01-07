using Gtk;
using Gdk;
using Posix;


public class JAMediaEditor : Gtk.Window{

    private Menu menu = new Menu(new Gtk.AccelGroup());

    public JAMediaEditor(){

        this.set_title("JAMediaEditor");
		this.window_position = Gtk.WindowPosition.CENTER;
		this.set_default_size(640, 480);
		this.set_resizable(true);
        this.set("border_width", 5);
        try {
            Gtk.Window.set_default_icon_from_file("Iconos/JAMediaEditor.svg");
            }
        catch(Error e) {}

        Gtk.Box box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        box.pack_start(this.menu, false, false, 0);

        this.add_accel_group(this.menu.accel_group);

        this.add(box);
        this.show_all();

        this.destroy.connect(this.__salir);

        GLib.stdout.printf("JAMediaEditor process: %i\n", Posix.getpid());
        GLib.stdout.flush();
    }

    private void __salir(){
        Gtk.main_quit();
        }
}


public static int main (string[] args) {
    Gtk.init(ref args);
    //var screen = Gdk.Screen.get_default();
    //var css_provider = new Gtk.CssProvider();
    //string style_path = "Estilo.css";
    //css_provider.load_from_path(style_path);
    //Gtk.StyleContext.add_provider_for_screen(
    //    screen, css_provider,
    //    Gtk.STYLE_PROVIDER_PRIORITY_USER);
    JAMediaEditor app = new JAMediaEditor();
    app.show_all();
    Gtk.main();
    return 0;
}
