using Gtk;
using Gdk;
using Posix;


public class JAMediaEditor : Gtk.Window{

    private Menu menu = new Menu(new Gtk.AccelGroup());
    private ToolbarEstado status = new ToolbarEstado();
    private BasePanel base_panel = new BasePanel();

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
        box.pack_start(this.base_panel, true, true, 0);
        box.pack_end(this.status, false, false, 0);
        //self.jamediapygihack = JAMediaPyGiHack()

        this.add_accel_group(this.menu.accel_group);

        this.add(box);
        this.show_all();
        this.maximize();

        //self.jamediapygihack.hide()

        this.destroy.connect(this.__salir);

        this.menu.accion.connect((_accion, valor) => {
			this.__accion_menu(_accion, valor);
		    });
        //self.jamediapygihack.connect('salir', self.__run_editor)

        this.base_panel.accion.connect ((_accion) => {
            this.__accion_toolbar(_accion);
		    });

        GLib.stdout.printf("JAMediaEditor process: %i\n", Posix.getpid());
        GLib.stdout.flush();
    }

    private void __accion_toolbar(string _accion){
        switch (_accion){
            case "Abrir Archivo":{
                this.__run_chooser_open_files();
                break;
                }
            default:{
                GLib.stdout.printf("__accion_base_panel: %s\n", _accion);
                GLib.stdout.flush();
                break;
                }
            }
        }

    private void __run_chooser_open_files(){
        // FIXME: El path debe ser el directorio del archivo seleccionado actualmente, o en su defecto:
        // el directorio del proyecto abierto si lo hay, o WorkPath() si no hay ninguno de los anteriores.
        string path = WorkPath();

        SList<string> mimelist = null;
        mimelist.append("text/*");
        mimelist.append("image/svg+xml");

        Multiple_FileChooser selector = new Multiple_FileChooser(
            "Abrir Archivos", this,
            Gtk.FileChooserAction.OPEN, new SList<string> (), mimelist,
            path);

        SList<string> archivos = null;
        if (selector.run() == Gtk.ResponseType.ACCEPT){
            archivos = selector.get_filenames();
            foreach (unowned string archivo in archivos){
                GLib.stdout.printf("%s\n", archivo);
                GLib.stdout.flush();
                }
            }
        selector.destroy();
        // FIXME: Abrir archivos seleccionados.
        }

    private void __accion_menu(string _accion, bool valor){
        switch (_accion){
            case "Abrir Archivo":{
                this.__run_chooser_open_files();
                break;
                }
            default:{
                GLib.stdout.printf("__accion_menu: %s %s\n", _accion, valor.to_string());
                GLib.stdout.flush();
                break;
                }
            }
        }

    private void __salir(){
        Gtk.main_quit();
        }
}


public static int main (string[] args) {
    Gtk.init(ref args);
    var screen = Gdk.Screen.get_default();
    var css_provider = new Gtk.CssProvider();
    string style_path = "Estilo.css";
    css_provider.load_from_path(style_path);
    Gtk.StyleContext.add_provider_for_screen(
        screen, css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER);
    JAMediaEditor app = new JAMediaEditor();
    app.show_all();
    Gtk.main();
    return 0;
}
