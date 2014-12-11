/*
Compilar con:
    valac --pkg glib-2.0 --pkg gio-2.0 --pkg libsoup-2.4 \
    --pkg gtk+-3.0 --pkg gdk-3.0 --pkg gdk-x11-3.0 --pkg gstreamer-1.0 \
    --pkg json-glib-1.0
Para Utilizar gstreamer 0.10 cambiar: --pkg gstreamer-1.0
por: --pkg gstreamer-0.10 --pkg gstreamer-interfaces-0.10
*/

//valac --pkg glib-2.0 --pkg gtk+-3.0 --pkg gdk-3.0 JAMedia.vala Toolbars.vala Widgets.vala Globales.vala

//using GLib;   Se importa siempre por default
using Gtk;      //--pkg gtk+-3.0
using Gdk;


public class JAMedia : Gtk.Window{

    private Toolbar toolbar = new Toolbar();
    private ToolbarSalir toolbarsalir = new ToolbarSalir();
    private ToolbarAccion toolbaraccion = new ToolbarAccion();

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

        box.pack_start(this.toolbar, false,false, 0);
        box.pack_start(this.toolbarsalir, false,false, 0);
        box.pack_start(this.toolbaraccion, false,false, 0);

        this.add(box);
        this.show_all();

        this.toolbar.credits.connect(this.__show_credits);
        this.toolbar.help.connect(this.__show_help);
        this.toolbar.accion.connect(this.__toolbar_accion);
        this.toolbaraccion.accion_stream.connect(this.__accion_stream);
        this.toolbaraccion.grabar.connect(this.__grabar);
        this.toolbarsalir.salir.connect(this.__exit);
        this.destroy.connect(this.__exit);
        }

    private void __toolbar_accion(string accion){
        if (accion == "show-config"){
            // FIXME: this.base_panel.derecha.show_config();
            stdout.printf("%s\n", accion);
            }
        else if (accion == "salir"){
            this.__exit();
            }
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
