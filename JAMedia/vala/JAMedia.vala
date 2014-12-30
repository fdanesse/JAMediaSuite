/*
Compilar con:
    valac --pkg glib-2.0 --pkg gio-2.0 --pkg libsoup-2.4 \
    --pkg gtk+-3.0 --pkg gdk-3.0 --pkg gdk-x11-3.0 --pkg gstreamer-1.0 \
    --pkg json-glib-1.0
Para Utilizar gstreamer 0.10 cambiar: --pkg gstreamer-1.0
por: --pkg gstreamer-0.10 --pkg gstreamer-interfaces-0.10
*/

//http://www.abenga.com/post/2013/7/30/gtk+-programming-using-vala:-background-/

//using GLib;   Se importa siempre por default
using Gtk;
using Gdk;
using Posix;
using Gst;


public class JAMedia : Gtk.Window{

    private Toolbar toolbar = new Toolbar();
    private ToolbarSalir toolbarsalir = new ToolbarSalir();
    private ToolbarAccion toolbaraccion = new ToolbarAccion();
    private ToolbarAddStream add_stream = new ToolbarAddStream();

    private BasePanel base_panel = null;

    private SList<string> archivos = null;
    private bool mouse_in_visor = false;
    private Gdk.Cursor cursor_root = null;
    private Gdk.Cursor cursor_blank = new Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR);
    private Gdk.Cursor jamedia_cursor = null;
    private MouseSpeedDetector mouse_listener = null;

    public JAMedia(){

        this.set_title("JAMedia");
		this.window_position = Gtk.WindowPosition.CENTER;
		this.set_default_size(640, 480);
		this.set_resizable(true);
        this.set("border_width", 2);
        try {
            Gtk.Window.set_default_icon_from_file("Iconos/JAMedia.svg");
            }
        catch(Error e) {
            GLib.stderr.printf("No se Encontró el Ícono: %s\n", e.message);
            GLib.stderr.flush();
            }

        this.base_panel = new BasePanel(this);
        //self.grabador = False

        Gdk.Pixbuf pixbuf = new Gdk.Pixbuf.from_file_at_size("Iconos/jamedia_cursor.svg", -1, 24);
        this.jamedia_cursor = new Gdk.Cursor.from_pixbuf(Gdk.Display.get_default(), pixbuf, 0, 0);

        Gtk.Box box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        box.pack_start(this.toolbar, false, false, 0);
        box.pack_start(this.toolbarsalir, false, false, 0);
        box.pack_start(this.toolbaraccion, false, false, 0);
        box.pack_start(this.add_stream, false, false, 0);
        box.pack_start(this.base_panel, true, true, 0);

        this.realize.connect(this.__realize);

        this.add(box);
        this.show_all();
        this.realize();

        this.mouse_listener = new MouseSpeedDetector(this);
        this.mouse_listener.new_handler(true);

        this.toolbar.credits.connect(this.__show_credits);
        this.toolbar.help.connect(this.__show_help);
        this.toolbar.accion.connect(this.__accion_toolbar);
        this.toolbaraccion.accion_stream.connect(this.__accion_stream);
        this.toolbaraccion.grabar.connect ((stream) => {
			this.__grabar(stream);
		    });
        this.toolbaraccion.stop.connect(this.__stop);
        this.add_stream.add_stream.connect ((lista, stream) => {
			this.__add_stream(lista, stream);
		    });
        this.toolbarsalir.salir.connect(this.__salir);

        this.base_panel.show_controls.connect(this.__ocultar_controles);
        this.base_panel.actualizar_streamings.connect(this.__actualizar_streamings);
        this.base_panel.accion_list.connect(this.__accion_list);

        this.base_panel.menu_activo.connect(this.__cancel_toolbars);
        this.base_panel.add_stream.connect(this.__run_add_stream);
        //self.base_panel.connect("stop-record", self.__detener_grabacion)
        this.base_panel.configurar.connect(this.__activar_config);

        this.mouse_listener.estado.connect(this.__set_mouse);
        this.hide.connect(this.__hide_show);
        this.show.connect(this.__hide_show);
        this.destroy.connect(this.__salir);

        this.resize(640, 480);

        GLib.Idle.add(this.__setup_init);
        GLib.stdout.printf("JAMedia process: %i\n", Posix.getpid());
        GLib.stdout.flush();
        }

    private void __actualizar_streamings(){
        DialogoDescarga dialog = new DialogoDescarga(this, true);
        dialog.run();
        dialog.destroy();
        }

    private void __activar_config(bool valor){
        this.toolbar.configurar.set_sensitive(valor);
        }

    private void __realize(){
        this.cursor_root = this.get_window().get_cursor();
        this.get_window().set_cursor(this.jamedia_cursor);
        }

    private bool __add_stream(string lista, Streaming stream){
        add_streamx(lista, stream);
        int indice = 0;
        if ("Tv" in lista || "TV" in lista){
            indice = 3;
            }
        else if ("Radio" in lista){
            indice = 2;
            }
        else{
            return false;
            }
        this.base_panel.derecha.lista.cargar_lista(indice);
        return true;
        }

    private void __run_add_stream(string title){
        this.add_stream.set_accion(title);
        }

    private void __grabar(Streaming stream){
        GLib.stdout.printf("FIXME: __grabar %s\n", stream.path);
        GLib.stdout.flush();
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

    //def __update_grabador(self, widget, datos):
    //    self.base_panel.izquierda.toolbar_record.set_info(datos)

    /*
    def __detener_grabacion(self, widget=None):
        if self.grabador:
            self.grabador.disconnect_by_func(self.__update_grabador)
            self.grabador.disconnect_by_func(self.__detener_grabacion)
            self.grabador.stop()
            del(self.grabador)
            self.grabador = False
        self.base_panel.izquierda.toolbar_record.stop()
    */

    private void __accion_stream(string accion, Streaming stream){
        string lista = this.base_panel.derecha.lista.toolbar.label.get_text();
        if (accion == "Borrar"){
            eliminar_streaming(stream, lista);
            }
        else if (accion == "Copiar"){
            add_streamx(lista, stream);
            }
        else if (accion == "Mover"){
            add_streamx(lista, stream);
            eliminar_streaming(stream, lista);
            }
        else{
            GLib.stdout.printf("Accion_stream Desconocida: %s\n", accion);
            GLib.stdout.flush();
            }
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
        DialogoDescarga dialog = new DialogoDescarga(this, false);
        dialog.run();
        dialog.destroy();
        return false;
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
            GLib.stdout.printf("__accion_toolbar %s\n", accion);
            GLib.stdout.flush();
            }
        }

    private void __hide_show(){
        //Controlador del mouse funcionará solo si JAMedia es Visible.
        this.mouse_listener.new_handler(this.get_visible());
        }

    private void __set_mouse(string estado){
        Gdk.Window win = this.get_window();
        if (this.mouse_in_visor){  // Solo cuando el mouse está sobre el Visor.
            if (estado == "moviendose"){
                if (win.get_cursor() != this.jamedia_cursor){
                    win.set_cursor(this.jamedia_cursor);
                    }
                }
            else if (estado == "detenido"){
                if (win.get_cursor() != this.cursor_blank){
                    win.set_cursor(this.cursor_blank);
                    }
                }
            else if (estado == "fuera"){
                if (win.get_cursor() != this.cursor_root){
                    win.set_cursor(this.cursor_root);
                    }
                }
            }
        else{
            if (estado == "moviendose" || estado == "detenido"){
                if (win.get_cursor() != this.jamedia_cursor){
                    win.set_cursor(this.jamedia_cursor);
                    }
                }
            else if (estado == "fuera"){
                if (win.get_cursor() != this.cursor_root){
                    win.set_cursor(this.cursor_root);
                    }
                }
            }
        }

    private void __ocultar_controles(bool zona, bool ocultar){
        this.mouse_in_visor = zona;
        if (zona && ocultar){
            this.__cancel_toolbars();
            this.set_border_width(0);
            this.base_panel.set_border_width(0);
            this.toolbar.hide();
            this.base_panel.derecha.hide();
            this.base_panel.izquierda.toolbar_info.hide();
            this.base_panel.izquierda.progress.hide();
            }
        else if (! zona && ocultar){
            this.toolbar.show();
            this.set_border_width(2);
            this.base_panel.set_border_width(2);
            this.base_panel.derecha.show();
            this.base_panel.izquierda.toolbar_info.show();
            this.base_panel.izquierda.progress.show();
            //#if not self.hbox_efectos_en_pipe.get_children():
            //#    self.hbox_efectos_en_pipe.get_parent().get_parent(
            //#        ).get_parent().hide()
            }
        else if (! zona && ! ocultar){
            }
        else if (zona && ! ocultar){
            }
        }

    private void __salir(){
        // FIXME: this.__detener_grabacion();
        // FIXME: this.BasePanel.salir();
        Gtk.main_quit();
        }

    private void __cancel_toolbars(){
        this.toolbarsalir.hide();
        this.toolbaraccion.hide();
        this.add_stream.hide();
        }

    private void __accion_list(Lista lista, string accion, Gtk.TreePath path){
        this.toolbaraccion.set_accion(lista, accion, path);
        }

    //def set_archivos(self, archivos):
    //    self.archivos = archivos

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

    private void __stop(){
        this.base_panel.stop();
        }
}


//def check_path(path):
//    if os.path.exists(path):
//        if os.path.isfile(path):
//            datos = describe_archivo(path)
//            if 'audio' in datos or 'video' in datos or \
//                'application/ogg' in datos or \
//                'application/octet-stream' in datos:
//                    return path
//    return False


public static int main (string[] args) {
    Gtk.init(ref args);
    Gst.init(ref args);
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
