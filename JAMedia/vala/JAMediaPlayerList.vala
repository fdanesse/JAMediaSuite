
public class JAMediaPlayerList : Gtk.Frame{
    /*
    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "accion-list": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    */

    public signal void add_stream(string title);
    public signal void menu_activo();

    private SList<string> mime = new SList<string> ();
    private string directorio = "";
    private Lista lista = new Lista();
    private JAMediaToolbarList toolbar = new JAMediaToolbarList();

    public JAMediaPlayerList(){

        this.directorio = get_JAMedia_Directory();

        this.mime.append("audio/*");
        this.mime.append("video/*");

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        Gtk.ScrolledWindow scroll = new Gtk.ScrolledWindow(null, null);
        scroll.set("hscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        scroll.add(this.lista);

        vbox.pack_start(this.toolbar, false, false, 0);
        vbox.pack_start(scroll, true, true, 0);

        this.add(vbox);
        this.show_all();

        this.set_size_request(150, -1);

        this.toolbar.cargar_lista.connect(this.cargar_lista);
        this.toolbar.add_stream.connect(this.__emit_add_stream);
        this.toolbar.menu_activo.connect(this.__emit_menu_activo);
        /*
        self.lista.connect("nueva-seleccion", self.__emit_nueva_seleccion)
        self.lista.connect("button-press-event", self.__click_derecho_en_lista)
        */
    }

    private void __emit_add_stream(){
        // El usuario agregará una dirección de streaming
        this.add_stream(this.toolbar.label.get_text());
        }

    private void __emit_menu_activo(){
        // hay un menu contextual presente
        this.menu_activo();
        }
    /*
    def __emit_accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.emit("accion-list", lista, accion, _iter)

    def __emit_nueva_seleccion(self, widget, pista):
        # item seleccionado en la lista
        self.emit('nueva-seleccion', pista)
    */

    private void __seleccionar_lista_de_stream(string archivo, string titulo){
        //items = get_streamings(archivo)
        //self.__load_list(items, "load", titulo)
        }

    private void __seleccionar_lista_de_archivos(string directorio, string titulo){
        SList<string> items = null;
        GLib.Dir dir = GLib.Dir.open (directorio, 0);
        string name = null;
		while ((name = dir.read_name ()) != null) {
			string path = GLib.Path.build_filename (directorio, name);
			bool isfile = GLib.FileUtils.test (path, GLib.FileTest.IS_REGULAR);
			if (isfile == true){
			    items.append(path);
			    }
			}
        this.__load_files(items, titulo);
        }

    private void __load_files(SList<string> archivos, string titulo){
        SList<Streaming> items = null;
        foreach (unowned string path in archivos) {
            bool isfile = GLib.FileUtils.test(path, GLib.FileTest.IS_REGULAR);
            if (isfile == true){
                Streaming item = new Streaming(GLib.Path.get_basename(path), path);
                items.append(item);
                this.directorio = GLib.Path.get_dirname(path);
                }
			}
        this.__load_list(items, "load", titulo);
        // FIXME: Mostrar clear y add para agregar archivos a la lista
        }

    private void __load_list(SList<Streaming> items, string tipo, string titulo){
        if (tipo == "load"){
            this.lista.limpiar();
            //FIXME: self.emit("accion-list", False, "limpiar", False)
            }
        if ((bool)items){
            this.lista.agregar_items(items);
            }
        else{
            //FIXME: self.emit('nueva-seleccion', False)
            }
        if ((bool) titulo){
            this.toolbar.label.set_text(titulo);
            }
        }

    /*
    def __click_derecho_en_lista(self, widget, event):
        boton = event.button
        pos = (event.x, event.y)
        tiempo = event.time
        path, columna, xdefondo, ydefondo = (None, None, None, None)
        try:
            path, columna, xdefondo, ydefondo = widget.get_path_at_pos(
                int(pos[0]), int(pos[1]))
        except:
            return
        # TreeView.get_path_at_pos(event.x, event.y) devuelve:
        # * La ruta de acceso en el punto especificado (x, y),
        # en relación con las coordenadas widget
        # * El gtk.TreeViewColumn en ese punto
        # * La coordenada X en relación con el fondo de la celda
        # * La coordenada Y en relación con el fondo de la celda
        if boton == 1 or boton == 2:
            return
        elif boton == 3:
            self.__emit_menu_activo()
            menu = MenuList(
                widget, boton, pos, tiempo, path, widget.get_model())
            menu.connect('accion', self.__emit_accion_list)
            gtk.Menu.popup(menu, None, None, None, boton, tiempo)
    */

    public void seleccionar_primero(){
        this.lista.seleccionar_primero();
        }

    public void seleccionar_ultimo(){
        this.lista.seleccionar_ultimo();
        }

    public void seleccionar_anterior(){
        this.lista.seleccionar_anterior();
        }

    public void seleccionar_siguiente(){
        this.lista.seleccionar_siguiente();
        }

    //def select_valor(self, path_origen):
    //    self.lista.select_valor(path_origen)

    public void limpiar(){
        this.lista.limpiar();
        }

    public void set_mime_types(SList<string> mimelist){
        this.mime = mimelist.copy();
        }

    /*
    def get_selected_path(self):
        modelo, _iter = self.lista.get_selection().get_selected()
        valor = self.lista.get_model().get_value(_iter, 2)
        return valor

    def get_items_paths(self):
        filepaths = []
        model = self.lista.get_model()
        item = model.get_iter_first()
        self.lista.get_selection().select_iter(item)
        while item:
            filepaths.append(model.get_value(item, 2))
            item = model.iter_next(item)
        return filepaths
    */

    public void setup_init(){
        this.toolbar.boton_agregar.hide();
        }

    public void cargar_lista(int indice){
        string data = get_data_directory();

        string a = GLib.Path.build_filename(data, "JAMediaRadio.JAMedia");
        string b = GLib.Path.build_filename(data, "JAMediaTV.JAMedia");
        string c = GLib.Path.build_filename(data, "MisRadios.JAMedia");
        string d = GLib.Path.build_filename(data, "MisTvs.JAMedia");
        string e = GLib.Path.build_filename(data, "JAMediaWebCams.JAMedia");
        string f = get_my_files_directory();
        string g = get_tube_directory();
        string h = get_audio_directory();
        string i = get_video_directory();

        this.toolbar.boton_agregar.hide();

        switch (indice){
            case 0:{
                this.__seleccionar_lista_de_stream(a, "JAM-Radio");
                break;
            }
            case 1:{
                this.__seleccionar_lista_de_stream(b, "JAM-TV");
                break;
            }
            case 2:{
                this.__seleccionar_lista_de_stream(c, "Radios");
                this.toolbar.boton_agregar.show();
                break;
            }
            case 3:{
                this.__seleccionar_lista_de_stream(d, "TVs");
                this.toolbar.boton_agregar.show();
                break;
            }
            case 4:{
                this.__seleccionar_lista_de_stream(e, "WebCams");
                break;
            }
            case 5:{
                this.__seleccionar_lista_de_archivos(f, "Archivos");
                break;
            }
            case 6:{
                this.__seleccionar_lista_de_archivos(g, "JAM-Tube");
                break;
            }
            case 7:{
                this.__seleccionar_lista_de_archivos(h, "JAM-Audio");
                break;
            }
            case 8:{
                this.__seleccionar_lista_de_archivos(i, "JAM-Video");
                break;
            }
            case 9:{
                // FIXME: this.get_toplevel() no hace lo que debiera.
                My_FileChooser selector = new My_FileChooser(
                    "Abrir Archivos", this.get_toplevel() as Gtk.Window,
                    Gtk.FileChooserAction.OPEN, new SList<string> (), this.mime,
                    this.directorio);
                selector.load_files.connect(this.__load_files);
                selector.run();
                selector.destroy();
                break;
            }
            default:{
                stdout.printf("Indice de lista sin tratar: %i\n", indice);
				stdout.flush();
                break;
            }
        }
        }

    public void set_ip(bool valor){
        this.toolbar.ip = valor;
    }

    public void set_nueva_lista(SList<string> archivos){
        this.__load_files(archivos, "Archivos");
    }
}


public class Lista : Gtk.TreeView{
    /*
    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}
    */

    private Gtk.ListStore lista = new Gtk.ListStore(3, typeof (Gdk.Pixbuf), typeof (string), typeof (string));
    private bool permitir_select = true;
    private string valor_select = null;
    private string ultimo_select = null;

    public Lista(){

        this.set_model(this.lista);

        this.set("rules-hint", true);
        this.set("headers_clickable", true);
        this.set("headers_visible", true);

        this.__setear_columnas();

        //self.get_selection().set_select_function(self.__selecciones, self.get_model())

        this.show_all();
    }

    private void __setear_columnas(){
        Gtk.CellRendererPixbuf cr1 = new Gtk.CellRendererPixbuf();
        //cr1.set_property("cell-background", get_colors("toolbars"))
        Gtk.TreeViewColumn col1 = new Gtk.TreeViewColumn();
        col1.set_title("");
        col1.pack_start(cr1, false);
        col1.set_attributes(cr1, "pixbuf", 0);
        col1.set_property("resizable", false);
        col1.set_property("visible", true);
        col1.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE);
        this.append_column(col1);

        Gtk.CellRendererText cr2 = new Gtk.CellRendererText();
        //cr2.set_property("background", get_colors("window"))
        //cr2.set_property("foreground", get_colors("drawingplayer"))
        Gtk.TreeViewColumn col2 = new Gtk.TreeViewColumn();
        col2.set_title("Archivo");
        col2.pack_start(cr2, false);
        col2.set_attributes(cr2, "text", 1);
        col2.set_property("resizable", false);
        col2.set_property("visible", true);
        col2.set_sort_column_id(1);
        col2.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE);
        this.append_column(col2);

        Gtk.CellRendererText cr3 = new Gtk.CellRendererText();
        Gtk.TreeViewColumn col3 = new Gtk.TreeViewColumn();
        col3.set_title("");
        col3.pack_start(cr3, false);
        col3.set_attributes(cr3, "text", 2);
        col3.set_property("visible", false);
        this.append_column(col3);
        }
    /*
    def __selecciones(self, path, column):
        if not self.permitir_select:
            return True
        _iter = self.get_model().get_iter(path)
        valor = self.get_model().get_value(_iter, 2)
        if self.valor_select != valor:
            self.valor_select = valor
            gobject.timeout_add(3, self.__select,
                self.get_model().get_path(_iter))
        return True

    def __select(self, path):
        if self.ultimo_select != self.valor_select:
            self.emit('nueva-seleccion', self.valor_select)
            self.ultimo_select = self.valor_select
        self.scroll_to_cell(path)
        return False
    */

    private bool __ejecutar_agregar_elemento(SList<Streaming> items){
        //FIXME: Funcionalidad, no es igual a la versión python.
        this.permitir_select = false;
        this.set_sensitive(false);

        string icono = "Iconos/sonido.svg";
        Gdk.Pixbuf pixbuf = new Gdk.Pixbuf.from_file_at_size(icono, 24, -1);

        Gtk.TreeIter iter;
        foreach (Streaming stream in items){
            bool isfile = GLib.FileUtils.test(stream.path, GLib.FileTest.IS_REGULAR);
            if (isfile == true){
                GLib.File file = GLib.File.parse_name(stream.path);
                var file_info = file.query_info ("*", GLib.FileQueryInfoFlags.NONE);
                string tipo = file_info.get_content_type();
                if ("video" in tipo || "application/ogg" in tipo){
                    icono = "Iconos/video.svg";
                    pixbuf = new Gdk.Pixbuf.from_file_at_size(icono, 24, -1);
                    }
                }
            if (! GLib.FileUtils.test(stream.path, GLib.FileTest.IS_DIR)){
                this.lista.append(out iter);
                this.lista.set(iter, 0, pixbuf, 1, stream.nombre, 2, stream.path);
                }
			}
        this.permitir_select = true;
        this.seleccionar_primero();
        this.set_sensitive(true);
        return false;
        }

    public void limpiar(){
        this.permitir_select = false;
        this.lista.clear();
        this.valor_select = null;
        this.ultimo_select = null;
        this.permitir_select = true;
        }

    public void agregar_items(SList<Streaming> items){
        // FIXME: Convertir en Función GLib.
        //GLib.Idle.add_full(GLib.Priority.DEFAULT_IDLE, this.__ejecutar_agregar_elemento, items, null);
        this.__ejecutar_agregar_elemento(items);
        }

    public void seleccionar_siguiente(){
        //modelo, _iter = self.get_selection().get_selected()
        //try:
        //    self.get_selection().select_iter(
        //        self.get_model().iter_next(_iter))
        //except:
        //    self.seleccionar_primero()
        //return False
        }

    public void seleccionar_anterior(){
        //modelo, _iter = self.get_selection().get_selected()
        //try:
        //    # HACK porque: model no tiene iter_previous
        //    #self.get_selection().select_iter(
        //    #    self.get_model().iter_previous(_iter))
        //    path = self.get_model().get_path(_iter)
        //    path = (path[0] - 1, )
        //    if path > -1:
        //        self.get_selection().select_iter(
        //            self.get_model().get_iter(path))
        //except:
        //    self.seleccionar_ultimo()
        //return False
        }

    public void seleccionar_primero(){
        //self.get_selection().select_path(0)
        }

    public void seleccionar_ultimo(){
        //model = self.get_model()
        //item = model.get_iter_first()
        //_iter = None
        //while item:
        //    _iter = item
        //    item = model.iter_next(item)
        //if _iter:
        //    self.get_selection().select_iter(_iter)
        //    #path = model.get_path(iter)
        }

    /*
    def select_valor(self, path_origen):
        model = self.get_model()
        _iter = model.get_iter_first()
        valor = model.get_value(_iter, 2)
        while valor != path_origen:
            _iter = model.iter_next(_iter)
            valor = model.get_value(_iter, 2)
        if _iter:
            self.get_selection().select_iter(_iter)
    */
}


public class JAMediaToolbarList : Gtk.EventBox{

    public signal void add_stream();
    public signal void menu_activo();
    public signal void cargar_lista(int indice);

    public bool ip = false;
    public Gtk.Label label = new Gtk.Label("");
    public Gtk.ToolButton boton_agregar = get_button("Iconos/agregar.svg", false, Gdk.PixbufRotation.NONE, 24, "Agregar Streaming");

    public JAMediaToolbarList(){

        Gtk.Toolbar toolbar = new Gtk.Toolbar();

        Gtk.ToolButton button1 = get_button("Iconos/lista.svg", false, Gdk.PixbufRotation.NONE, 24, "Selecciona una Lista");
		button1.clicked.connect (() => {
			this.__get_menu(button1);
		});
		toolbar.insert(button1, -1);

		Gtk.SeparatorToolItem separador1 = get_separador(false, 3, false);
        toolbar.insert(separador1, -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        this.label.show();
        item.add(this.label);
        toolbar.insert(item, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 0, true);
        toolbar.insert(separador2, -1);

		this.boton_agregar.clicked.connect (() => {
		    this.__emit_add_stream();
		});
		toolbar.insert(this.boton_agregar, -1);

        this.add(toolbar);
        this.show_all();
    }

    private void __get_menu(Gtk.Widget widget){
        this.menu_activo();
        Gtk.Menu menu = new Gtk.Menu();

        if (this.ip == true){
            Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("JAMedia Radio");
            menu.append(item1);
            item1.activate.connect (() => {
			    this.__emit_load_list(0);
		    });

            Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("JAMedia TV");
            menu.append(item2);
            item2.activate.connect (() => {
			    this.__emit_load_list(1);
		    });

            Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Mis Emisoras");
            menu.append(item3);
            item3.activate.connect (() => {
			    this.__emit_load_list(2);
		    });

            Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Mis Canales");
            menu.append(item4);
            item4.activate.connect (() => {
			    this.__emit_load_list(3);
		    });

            Gtk.MenuItem item5 = new Gtk.MenuItem.with_label("Web Cams");
            menu.append(item5);
            item5.activate.connect (() => {
			    this.__emit_load_list(4);
		    });
		    }

        Gtk.MenuItem item6 = new Gtk.MenuItem.with_label("Mis Archivos");
        menu.append(item6);
        item6.activate.connect (() => {
			this.__emit_load_list(5);
		});

        Gtk.MenuItem item7 = new Gtk.MenuItem.with_label("JAMediaTube");
        menu.append(item7);
        item7.activate.connect (() => {
			this.__emit_load_list(6);
		});

        Gtk.MenuItem item8 = new Gtk.MenuItem.with_label("Audio-JAMediaVideo");
        menu.append(item8);
        item8.activate.connect (() => {
			this.__emit_load_list(7);
		});

        Gtk.MenuItem item9 = new Gtk.MenuItem.with_label("Video-JAMediaVideo");
        menu.append(item9);
        item9.activate.connect (() => {
			this.__emit_load_list(8);
		});

        Gtk.MenuItem item10 = new Gtk.MenuItem.with_label("Archivos Externos");
        menu.append(item10);
        item10.activate.connect (() => {
			this.__emit_load_list(9);
		});

        menu.popup(null, null, null, 1, Gtk.get_current_event_time());

        menu.show_all();
        menu.attach_to_widget(widget, null);
        }

    private void __emit_load_list(int indice){
        this.cargar_lista(indice);
        }

    private void __emit_add_stream(){
        this.add_stream();
        }
}


public class My_FileChooser : Gtk.FileChooserDialog{

    public signal void load_files(SList<string> filenames, string titulo);

    private Gtk.FileFilter filtro = new Gtk.FileFilter();

    public My_FileChooser(string title, Gtk.Window parent,
        Gtk.FileChooserAction action, SList<string> filter_type,
        SList<string> mime, string path){

        this.set_title(title);
        this.set_modal(true);
        this.set_transient_for(parent);
        this.set_resizable(true);
        this.set_size_request(320, 240);

        this.set_current_folder(path);
        this.set_property("action", action);
        this.set_select_multiple(true);

        Gtk.Box hbox = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);

        Gtk.Button boton_abrir_directorio = new Gtk.Button();
        boton_abrir_directorio.set_label("Abrir");
        Gtk.Button boton_seleccionar_todo = new Gtk.Button();
        boton_seleccionar_todo.set_label("Seleccionar Todos");
        Gtk.Button boton_salir = new Gtk.Button();
        boton_salir.set_label("Salir");

        boton_salir.clicked.connect(this.__salir);
        boton_abrir_directorio.clicked.connect(this.__file_activated);
        boton_seleccionar_todo.clicked.connect(this.__select_all);

        hbox.pack_end(boton_salir, true, true, 5);
        hbox.pack_end(boton_seleccionar_todo, true, true, 5);
        hbox.pack_end(boton_abrir_directorio, true, true, 5);

        this.set_extra_widget(hbox);
        hbox.show_all();

        this.filtro.set_name("Filtro");
        foreach (unowned string fil in filter_type){
            filtro.add_pattern(fil);
            }
        foreach (unowned string mi in mime){
            filtro.add_mime_type(mi);
            }
        this.add_filter(this.filtro);

        this.add_shortcut_folder_uri("file:///media/");
        this.file_activated.connect(this.__file_activated);

        this.realize.connect(this.__resize);
    }

    private void __resize(){
        this.resize(437, 328);
        }

    private void __file_activated(){
        this.load_files(this.get_filenames(), "Archivos");
        this.__salir();
        }

    private void __select_all(){
        this.select_all();
        }

    private void __salir(){
        this.destroy();
        }
}


public class Streaming : GLib.Object{
    public string nombre;
    public string path;
    public Streaming(string nombre, string path){
        this.nombre = nombre;
        this.path = path;
    }
}
