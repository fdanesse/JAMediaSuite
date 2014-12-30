
public class Toolbar : Gtk.EventBox{

    public signal void accion(string acc);
    public signal void credits();
    public signal void help();

    public Gtk.ToolButton configurar = get_button("Iconos/configurar.svg", false, Gdk.PixbufRotation.NONE, 24, "Configuraciones");

    public Toolbar(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 3, false);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/JAMedia.svg", false, Gdk.PixbufRotation.NONE, 35, "Creditos");
		button1.clicked.connect (() => {
			this.__emit_credits();
		    });
		toolbar.insert(button1, -1);

        Gtk.ToolButton button2 = get_button("Iconos/JAMedia-help.svg", false, Gdk.PixbufRotation.NONE, 24, "Ayuda");
		button2.clicked.connect (() => {
			this.__emit_help();
		    });
		toolbar.insert(button2, -1);

		this.configurar.clicked.connect (() => {
			this.__emit_accion("show-config");
		    });
		toolbar.insert(this.configurar, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 0, true);
        toolbar.insert(separador2, -1);

        Gtk.ToolButton button4 = get_button("Iconos/button-cancel.svg", false, Gdk.PixbufRotation.NONE, 24, "Salir");
		button4.clicked.connect (() => {
			this.__emit_accion("salir");
		    });
		toolbar.insert(button4, -1);

        Gtk.SeparatorToolItem separador3 = get_separador(false, 3, false);
        toolbar.insert(separador3, -1);

        this.add(toolbar);
        this.show_all();
    }

    private void __emit_credits(){
        this.credits();
    }

    private void __emit_help(){
        this.help();
    }

    private void __emit_accion(string accion){
        this.accion(accion);
    }
}


public class ToolbarSalir : Gtk.EventBox{

    public signal void salir();
    private Gtk.Label label = new Gtk.Label("");

    public ToolbarSalir(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 0, true);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/button-cancel.svg", false, Gdk.PixbufRotation.NONE, 24, "Cancelar");
		button1.clicked.connect (() => {
			this.cancelar();
		});
		toolbar.insert(button1, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 3, false);
        toolbar.insert(separador2, -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        label.show();
        item.add(this.label);
        toolbar.insert(item, -1);

        Gtk.SeparatorToolItem separador3 = get_separador(false, 3, false);
        toolbar.insert(separador3, -1);

        Gtk.ToolButton button2 = get_button("Iconos/dialog-ok.svg", false, Gdk.PixbufRotation.NONE, 24, "Aceptar");
		button2.clicked.connect (() => {
			this.__emit_salir();
		});
		toolbar.insert(button2, -1);

        Gtk.SeparatorToolItem separador4 = get_separador(false, 0, true);
        toolbar.insert(separador4, -1);

        this.add(toolbar);
        this.show_all();
    }

    public void __emit_salir(){
        this.cancelar();
        this.salir();
        }

    public void run(string nombre_aplicacion){
        string text = string.join(" ", "¿Salir de", nombre_aplicacion, "?");
        this.label.set_text(text);
        this.show();
        }

    public void cancelar(){
        this.label.set_text("");
        this.hide();
        }
}


public class ToolbarAccion : Gtk.EventBox{

    public signal void grabar(Streaming stream);
    public signal void stop();
    public signal void accion_stream(string accion, Streaming stream);

    private Gtk.Label label = new Gtk.Label("");
    private Lista lista = null;
    private string accion = null;
    private Gtk.TreePath path = null;

    public ToolbarAccion(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 0, true);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/button-cancel.svg", false, Gdk.PixbufRotation.NONE, 24, "Cancelar");
		button1.clicked.connect (() => {
			this.cancelar();
		    });
		toolbar.insert(button1, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 3, false);
        toolbar.insert(separador2, -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        label.show();
        item.add(this.label);
        toolbar.insert(item, -1);

        Gtk.SeparatorToolItem separador3 = get_separador(false, 3, false);
        toolbar.insert(separador3, -1);

        Gtk.ToolButton button2 = get_button("Iconos/dialog-ok.svg", false, Gdk.PixbufRotation.NONE, 24, "Aceptar");
		button2.clicked.connect (() => {
			this.__realizar_accion();
		    });
		toolbar.insert(button2, -1);

        Gtk.SeparatorToolItem separador4 = get_separador(false, 0, true);
        toolbar.insert(separador4, -1);

        this.add(toolbar);
        this.show_all();
    }

    public void __realizar_accion(){
        // Valores para acción
        Gtk.TreeIter _iter;
	    GLib.Value val3;
	    GLib.Value val2;
	    this.lista.lista.get_iter(out _iter, this.path);
	    this.lista.lista.get_value(_iter, 1, out val2);
        this.lista.lista.get_value(_iter, 2, out val3);
        string nombre = val2.get_string();
        string uri = val3.get_string();

        // valores para determinar si es necesario seleccionar otro item
        Gtk.TreeModel modelo;
        Gtk.TreeIter _new;
        GLib.Value selected;
        this.lista.get_selection().get_selected(out modelo, out _new);
        this.lista.lista.get_value(_new, 2, out selected);

        if (this.accion == "Quitar"){
            this.lista._len_items --;
            if (uri == selected.get_string()){
                this.__reselect(_new);
                }
            this.lista.lista.remove(_iter);
            }

        else{
            bool isfile = GLib.FileUtils.test(uri, GLib.FileTest.IS_REGULAR);
            if (isfile == true){
                if (this.accion == "Copiar"){
                    copiar(uri, get_my_files_directory());
                    }
                else if (this.accion == "Borrar"){
                    borrar(uri);
                    this.lista._len_items --;
                    if (uri == selected.get_string()){
                        this.__reselect(_new);
                        }
                    this.lista.lista.remove(_iter);
                    }
                else if (this.accion == "Mover"){
                    mover(uri, get_my_files_directory());
                    this.lista._len_items --;
                    if (uri == selected.get_string()){
                        this.__reselect(_new);
                        }
                    this.lista.lista.remove(_iter);
                    }
                }

            else{
                Streaming stream = new Streaming(nombre, uri);
                if (this.accion == "Borrar" || this.accion == "Mover"){
                    this.accion_stream(this.accion, stream);
                    this.lista._len_items --;
                    if (uri == selected.get_string()){
                        this.__reselect(_new);
                        }
                    this.lista.lista.remove(_iter);
                    }
                else if (this.accion == "Copiar"){
                    this.accion_stream(this.accion, stream);
                    }
                else if (this.accion == "Grabar"){
                    this.grabar(stream);
                    }
                }
            }

        this.cancelar();
        }

    private bool __reselect(Gtk.TreeIter _new){
        bool val = this.lista.lista.iter_next(ref _new);
        if (val){
            this.lista.get_selection().select_iter(_new);
            return true;
            }

        val = this.lista.lista.iter_previous(ref _new);
        if (val){
            this.lista.get_selection().select_iter(_new);
            return true;
            }

        if (this.lista._len_items == 0){
            this.stop();
            return true;
            }
        return false;
        }

    public void set_accion(Lista lista, string accion, Gtk.TreePath path){

        this.lista = lista;
        this.accion = accion;
        this.path = path;

        if (this.lista.lista != null && this.accion != null && this.path != null){
            Gtk.TreeIter _iter;
            GLib.Value val2;
            this.lista.lista.get_iter(out _iter, path);
            this.lista.lista.get_value(_iter, 1, out val2);
            string texto = val2.get_string();
            //FIXME: Analizar si reimplementarlo así:
            //if os.path.exists(val3.get_string()):
            //  texto = os.path.basename(uri)
            //string texto = val2.get_string();
            //if (texto.length > 30){
            //    texto = " . . . " + str(texto[len(texto) - 30:-1])
            //    }
            this.label.set_text(string.join(" ", "¿", accion, "?: ", texto));
            this.show_all();
            }
        }

    public void cancelar(){
        this.lista = null;
        this.accion = null;
        this.path = null;
        this.label.set_text("");
        this.hide();
        }
}


public class ToolbarAddStream : Gtk.EventBox{

    public signal void add_stream(string _tipo, Streaming stream);
    private Gtk.Entry nombre = new Gtk.Entry();
    private Gtk.Entry url = new Gtk.Entry();
    private string tipo = "";

    public ToolbarAddStream(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 0, true);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/button-cancel.svg", false, Gdk.PixbufRotation.NONE, 24, "Cancelar");
		button1.clicked.connect (() => {
			this.cancelar();
		});
		toolbar.insert(button1, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 3, false);
        toolbar.insert(separador2, -1);

        Gtk.ToolItem item1 = new Gtk.ToolItem();
        Gtk.Frame frame1 = new Gtk.Frame("Nombre");
        Gtk.EventBox event1 = new Gtk.EventBox();
        event1.set_border_width(4);
        event1.add(this.nombre);
        frame1.add(event1);
        frame1.show_all();
        item1.add(frame1);
        toolbar.insert(item1, -1);

        Gtk.SeparatorToolItem separador3 = get_separador(false, 3, false);
        toolbar.insert(separador3, -1);

        Gtk.ToolItem item2 = new Gtk.ToolItem();
        Gtk.Frame frame2 = new Gtk.Frame("URL");
        Gtk.EventBox event2 = new Gtk.EventBox();
        event2.set_border_width(4);
        event2.add(this.url);
        frame2.add(event2);
        frame2.show_all();
        item2.add(frame2);
        toolbar.insert(item2, -1);

        Gtk.SeparatorToolItem separador4 = get_separador(false, 3, false);
        toolbar.insert(separador4, -1);

        Gtk.ToolButton button2 = get_button("Iconos/dialog-ok.svg", false, Gdk.PixbufRotation.NONE, 24, "Aceptar");
		button2.clicked.connect (() => {
			this.__emit_add_stream();
		});
		toolbar.insert(button2, -1);

        Gtk.SeparatorToolItem separador5 = get_separador(false, 0, true);
        toolbar.insert(separador5, -1);

        this.add(toolbar);
        this.show_all();
        }

    private void __emit_add_stream(){
        Streaming stream = new Streaming(this.nombre.get_text(), this.url.get_text());
        this.add_stream(this.tipo, stream);
        this.cancelar();
        }

    public void set_accion(string _tipo){
        this.show();
        this.nombre.set_text("");
        this.url.set_text("");
        this.tipo = _tipo;
        }

    public void cancelar(){
        this.tipo = "";
        this.nombre.set_text("");
        this.url.set_text("");
        this.hide();
        }
}
