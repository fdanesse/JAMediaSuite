
public class Toolbar : Gtk.EventBox{

    public signal void accion(string acc);
    public signal void credits();
    public signal void help();

    public Toolbar(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.SeparatorToolItem separador1 = get_separador(false, 3, false);
        toolbar.insert(separador1, -1);

        Gtk.ToolButton button1 = get_button("Iconos/JAMedia.svg", false, 35, "Creditos");
		button1.clicked.connect (() => {
			this.__emit_credits();
		});
		toolbar.insert(button1, -1);

        Gtk.ToolButton button2 = get_button("Iconos/JAMedia-help.svg", false, 24, "Ayuda");
		button2.clicked.connect (() => {
			this.__emit_help();
		});
		toolbar.insert(button2, -1);

        Gtk.ToolButton button3 = get_button("Iconos/configurar.svg", false, 24, "Configuraciones");
		button3.clicked.connect (() => {
			this.__emit_accion("show-config");
		});
		toolbar.insert(button3, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 0, true);
        toolbar.insert(separador2, -1);

        Gtk.ToolButton button4 = get_button("Iconos/button-cancel.svg", false, 24, "Salir");
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

        Gtk.ToolButton button1 = get_button("Iconos/button-cancel.svg", false, 24, "Cancelar");
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

        Gtk.ToolButton button2 = get_button("Iconos/dialog-ok.svg", false, 24, "Aceptar");
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

        Gtk.ToolButton button1 = get_button("Iconos/button-cancel.svg", false, 24, "Cancelar");
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

        Gtk.ToolButton button2 = get_button("Iconos/dialog-ok.svg", false, 24, "Aceptar");
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
        self.label.set_text("")
        self.lista = None
        self.accion = None
        self.iter = None
        self.hide()
        */
        this.label.set_text("");
        this.hide();
        }
}
