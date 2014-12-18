/*
Compilar con:
    valac --pkg glib-2.0 --pkg gio-2.0 --pkg libsoup-2.4 \
    --pkg gtk+-3.0 --pkg gdk-3.0 --pkg gdk-x11-3.0 --pkg gstreamer-1.0 \
    --pkg json-glib-1.0
Para Utilizar gstreamer 0.10 cambiar: --pkg gstreamer-1.0
por: --pkg gstreamer-0.10 --pkg gstreamer-interfaces-0.10
*/

//using GLib;   Se importa siempre por default
using Gtk;
using Gdk;


public class JAMedia : Gtk.Window{

    private Toolbar toolbar = new Toolbar();
    private ToolbarSalir toolbarsalir = new ToolbarSalir();
    private ToolbarAccion toolbaraccion = new ToolbarAccion();
    private ToolbarAddStream add_stream = new ToolbarAddStream();

    private BasePanel base_panel = new BasePanel();

    SList<string> archivos = null;

    public JAMedia(){

        this.set_title("JAMedia");
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

        //self.grabador = False
        //self.mouse_in_visor = False
        //self.cursor_root = gtk.gdk.Cursor(gtk.gdk.BLANK_CURSOR)
        //icono = os.path.join(BASE_PATH, "Iconos", "jamedia_cursor.svg")
        //pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 24)
        //self.jamedia_cursor = gtk.gdk.Cursor(
        //    gtk.gdk.display_get_default(), pixbuf, 0, 0)

        Gtk.Box box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        box.pack_start(this.toolbar, false, false, 0);
        box.pack_start(this.toolbarsalir, false, false, 0);
        box.pack_start(this.toolbaraccion, false, false, 0);
        box.pack_start(this.add_stream, false, false, 0);
        box.pack_start(this.base_panel, true, true, 0);

        this.add(box);
        this.show_all();
        this.realize();

        this.toolbar.credits.connect(this.__show_credits);
        this.toolbar.help.connect(this.__show_help);
        this.toolbar.accion.connect(this.__accion_toolbar);
        this.toolbaraccion.accion_stream.connect(this.__accion_stream);
        this.toolbaraccion.grabar.connect(this.__grabar);
        this.add_stream.add_stream.connect(this.__add_stream);
        this.toolbarsalir.salir.connect(this.__exit);

        //self.base_panel.connect("show-controls", self.__ocultar_controles)
        //self.base_panel.connect("accion-list", self.__accion_list)
        this.base_panel.menu_activo.connect(this.__cancel_toolbars);
        this.base_panel.add_stream.connect(this.__run_add_stream);
        //self.base_panel.connect("stop-record", self.__detener_grabacion)

        //self.mouse_listener.connect("estado", self.__set_mouse)
        this.hide.connect(this.__hide_show);
        this.show.connect(this.__hide_show);
        this.destroy.connect(this.__exit);

        this.resize(640, 480);
        //self.mouse_listener = MouseSpeedDetector(self)
        //self.mouse_listener.new_handler(True)

        GLib.Idle.add(this.__setup_init);
        //print "JAMedia process:", os.getpid()
        this.base_panel.checkear_listas();
        }

    private bool __setup_init(){
        this.__cancel_toolbars();
        this.toolbar.configurar.set_sensitive(false);
        this.base_panel.setup_init();
        if (this.archivos != null){
            this.base_panel.set_nueva_lista(this.archivos);
            this.archivos = null;
            }
        this.set_sensitive(true);
        return false;
        }

    private void __hide_show(){
        //Controlador del mouse funcionará solo si JAMedia es Visible.
        //self.mouse_listener.new_handler(widget.get_visible())
        }

    private void __run_add_stream(string title){
        this.add_stream.set_accion(title);
        }

    private void __add_stream(string tipo, string nombre, string url){
        stdout.printf("__add_stream %s %s %s\n", tipo, nombre, url);
        //add_stream(tipo, [nombre, url])
        //if "Tv" in tipo or "TV" in tipo:
        //    indice = 3
        //elif "Radio" in tipo:
        //    indice = 2
        //else:
        //    return
        //self.base_panel.derecha.lista.cargar_lista(None, indice)
        }

    private void __accion_toolbar(string accion){
        this.__cancel_toolbars();
        if (accion == "show-config"){
            this.base_panel.derecha.show_config();
            }
        else if (accion == "salir"){
            this.toolbarsalir.run("JAMedia");
            }
        else{
            stdout.printf("__accion_toolbar %s\n", accion);
            }
        }

    private void __cancel_toolbars(){
        this.toolbarsalir.hide();
        this.toolbaraccion.hide();
        this.add_stream.hide();
        }

    private void __grabar(string stream){
        stdout.printf("__grabar %s\n", stream);
        /*
        self.set_sensitive(False)
        self.__detener_grabacion()

        tipo = "video"
        label = self.base_panel.derecha.lista.toolbar.label.get_text()
        if label == "JAM-TV" or label == "TVs" or label == "WebCams":
            tipo = "video"
        else:
            tipo = "audio"

        hora = time.strftime("%H-%M-%S")
        fecha = str(datetime.date.today())
        archivo = "%s-%s" % (fecha, hora)
        archivo = os.path.join(get_my_files_directory(), archivo)

        self.grabador = JAMediaGrabador(uri, archivo, tipo)

        self.grabador.connect('update', self.__update_grabador)
        self.grabador.connect('endfile', self.__detener_grabacion)

        _thread = threading.Thread(target=self.grabador.play)
        _thread.start()

        self.set_sensitive(True)
        */
        }

    private void __accion_stream(string accion, string url){
        stdout.printf("__accion_stream %s\n", accion);
        /*
        def __accion_stream(self, widget, accion, url):
        lista = self.base_panel.derecha.lista.toolbar.label.get_text()
        if accion == "Borrar":
            eliminar_streaming(url, lista)
            print "Streaming Eliminado:", url
        elif accion == "Copiar":
            modelo, _iter = self.base_panel.derecha.lista.lista.get_selection(
                ).get_selected()
            nombre = modelo.get_value(_iter, 1)
            url = modelo.get_value(_iter, 2)
            tipo = self.base_panel.derecha.lista.toolbar.label.get_text()
            add_stream(tipo, [nombre, url])
        elif accion == "Mover":
            modelo, _iter = self.base_panel.derecha.lista.lista.get_selection(
                ).get_selected()
            nombre = modelo.get_value(_iter, 1)
            url = modelo.get_value(_iter, 2)
            tipo = self.base_panel.derecha.lista.toolbar.label.get_text()
            add_stream(tipo, [nombre, url])
            eliminar_streaming(url, lista)
        else:
            print "accion_stream desconocido:", accion
        */
        }

    private void __show_credits(){
        Creditos dialog = new Creditos(this, "");
        dialog.run();
        dialog.destroy();
        }

    private void __show_help(){
        Help dialog = new Help(this, "");
        dialog.run();
        dialog.destroy();
        }

    private void __exit(){
        // FIXME: this.__detener_grabacion();
        // FIXME: this.BasePanel.salir();
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
    JAMedia app = new JAMedia();
    app.show_all();
    Gtk.main();
    return 0;
}
