
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

    public signal void grabar(string stream);
    public signal void accion_stream(string accion, string stream);
    private Gtk.Label label = new Gtk.Label("");

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
        /*
    def __realizar_accion(self, widget):
        """
        Ejecuta una accion sobre un archivo o streaming en la lista.
        """
        uri = self.lista.get_model().get_value(self.iter, 2)
        if self.accion == "Quitar":
            path = self.lista.get_model().get_path(self.iter)
            path = (path[0] - 1, )
            self.lista.get_model().remove(self.iter)
            self.__reselect(path)
        else:
            if describe_acceso_uri(uri):
                if self.accion == "Copiar":
                    if os.path.isfile(uri):
                        copiar(uri, get_my_files_directory())
                elif self.accion == "Borrar":
                    if os.path.isfile(uri):
                        if borrar(uri):
                            path = self.lista.get_model().get_path(self.iter)
                            path = (path[0] - 1, )
                            self.lista.get_model().remove(self.iter)
                            self.__reselect(path)
                elif self.accion == "Mover":
                    if os.path.isfile(uri):
                        if mover(uri, get_my_files_directory()):
                            path = self.lista.get_model().get_path(self.iter)
                            path = (path[0] - 1, )
                            self.lista.get_model().remove(self.iter)
                            self.__reselect(path)
            else:
                if self.accion == "Borrar":
                    self.emit("accion-stream", "Borrar", uri)
                    path = self.lista.get_model().get_path(self.iter)
                    path = (path[0] - 1, )
                    self.lista.get_model().remove(self.iter)
                    self.__reselect(path)
                elif self.accion == "Copiar":
                    self.emit("accion-stream", "Copiar", uri)
                elif self.accion == "Mover":
                    self.emit("accion-stream", "Mover", uri)
                    path = self.lista.get_model().get_path(self.iter)
                    path = (path[0] - 1, )
                    self.lista.get_model().remove(self.iter)
                    self.__reselect(path)
                elif self.accion == "Grabar":
                    self.emit("grabar", uri)
        self.cancelar()
        */
        }

        /*
    def __reselect(self, path):
        try:
            if path[0] > -1:
                self.lista.get_selection().select_iter(
                    self.lista.get_model().get_iter(path))
            else:
                self.lista.seleccionar_primero()
        except:
            self.lista.seleccionar_primero()

    def set_accion(self, lista, accion, _iter):
        """
        Configura una accion sobre un archivo o streaming y muestra
        toolbaraccion para que el usuario confirme o cancele dicha accion.
        """
        self.lista = lista
        self.accion = accion
        self.iter = _iter
        if self.lista and self.accion and self.iter:
            uri = self.lista.get_model().get_value(self.iter, 2)
            texto = uri
            if os.path.exists(uri):
                texto = os.path.basename(uri)
            if len(texto) > 30:
                texto = " . . . " + str(texto[len(texto) - 30:-1])
            self.label.set_text("¿%s?: %s" % (accion, texto))
            self.show_all()
    */

    public void cancelar(){
        /*
        self.lista = None
        self.accion = None
        self.iter = None
        */
        this.label.set_text("");
        this.hide();
        }
}


public class ToolbarAddStream : Gtk.EventBox{

    public signal void add_stream(string _tipo, string _nombre, string _url);
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
        string _nombre = this.nombre.get_text();
        string _url = this.url.get_text();
        this.add_stream(this.tipo, _nombre, _url);
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
