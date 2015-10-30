
public class JAMediaPlayerList : Gtk.Frame{

    public signal void nueva_seleccion(string pista);
    public signal void add_stream(string title);
    public signal void menu_activo();
    public signal void accion_list (Lista lista, string accion, Gtk.TreePath path);
    public signal void len_items (int items);

    private SList<string> mime = new SList<string> ();
    private string directorio = "";
    private Lista lista = new Lista();
    public JAMediaToolbarList toolbar = new JAMediaToolbarList();

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

        this.lista.nueva_seleccion.connect(this.__emit_nueva_seleccion);
        this.lista.button_press_event.connect ((event) => {
			bool ret = this.__click_derecho_en_lista(event);
			return ret;
		    });
		this.lista.len_items.connect(this.__re_emit_len_items);
    }

    private void __re_emit_len_items(int items){
        this.len_items(items);
        }

    private void __emit_add_stream(){
        this.add_stream(this.toolbar.label.get_text());
        }

    private void __emit_menu_activo(){
        this.menu_activo();
        }

    private void __emit_accion_list(Lista lista, string accion, Gtk.TreePath path){
        // borrar, copiar, mover, grabar, etc . . .
        this.accion_list(lista, accion, path);
        }

    private void __emit_nueva_seleccion(string pista){
        this.nueva_seleccion(pista);
        }

    private void __seleccionar_lista_de_stream(string archivo, string titulo){
        SList<Streaming> items = get_streamings(archivo);
        this.__load_list(items, "load", titulo);
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
            // FIXME: Creo que no se necesita this.accion_list(null, "limpiar", "");
            }
        if ((bool)items){ //FIXME Modificar bool
            this.lista.agregar_items(items);
            }
        else{
            this.nueva_seleccion("");
            }
        if (titulo != ""){
            this.toolbar.label.set_text(titulo);
            }
        }

    private bool __click_derecho_en_lista(Gdk.EventButton event){

        if ((int) event.button == 3){
            this.__emit_menu_activo();
            Gtk.TreePath path;
            Gtk.TreeViewColumn column;
            int cell_x;
            int cell_y;
            this.lista.get_path_at_pos ((int) event.x, (int) event.y, out path, out column, out cell_x, out cell_y);
            MenuList menu = new MenuList(this.lista, path);
            menu.accion.connect ((lista, accion, path) => {
			    this.__emit_accion_list(lista, accion, path);
		        });
		    return true;
            }
        else{
            return false;
            }
    }

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

    public void limpiar(){
        this.lista.limpiar();
        }

    // FIXME: No se está utilizando
    //public void set_mime_types(SList<string> mimelist){
    //    this.mime = mimelist.copy();
    //    }

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
                // FIXME: Corregir esto. this.get_toplevel() no hace lo que debiera.
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
                GLib.stdout.printf("Indice de lista sin tratar: %i\n", indice);
				GLib.stdout.flush();
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

    public signal void nueva_seleccion(string pista);
    public signal void len_items (int items);

    public Gtk.ListStore lista = new Gtk.ListStore(3, typeof (Gdk.Pixbuf), typeof (string), typeof (string));
    private bool permitir_select = true;
    private string valor_select = null;
    public int _len_items = 0;

    public Lista(){

        this.set_model(this.lista);

        this.set("rules-hint", true);
        this.set("headers_clickable", true);
        this.set("headers_visible", true);

        this.__setear_columnas();

        Gtk.TreeSelection select = this.get_selection();
        select.set_mode(Gtk.SelectionMode.SINGLE);
        select.set_select_function(this.__selecciones);

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

    private bool __selecciones(Gtk.TreeSelection selection, Gtk.TreeModel filter,
        Gtk.TreePath path, bool path_currently_selected){
        if (! this.permitir_select || path_currently_selected){
            return true;
            }
        this.permitir_select = false;
        Gtk.TreeIter _iter;
        this.get_model().get_iter(out _iter, path);
        GLib.Value val;
        this.get_model().get_value(_iter, 2, out val);
        string valor = val.dup_string();

        if (this.valor_select != valor){
            GLib.Idle.add (() => {
                this.__select(this.get_model().get_path(_iter), valor);
                return false;
                });
            }
        return true;
        }

    private void __select(Gtk.TreePath path, string valor){
        this.valor_select = valor;
        this.nueva_seleccion(this.valor_select);
        //self.scroll_to_cell(self.get_model().get_path(_iter))
        //FIXME: Verificar:
        //this.scroll_to_cell (TreePath? path, TreeViewColumn? column, bool use_align, float row_align, float col_align)
        this.permitir_select = true;
        }

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
        this.permitir_select = true;
        this._len_items = 0;
        this.len_items(0);
        }

    public void agregar_items(SList<Streaming> items){
        this._len_items = (int) items.length();
        this.len_items(this._len_items);
        // FIXME: Convertir en Función GLib.
        //GLib.Idle.add_full(GLib.Priority.DEFAULT_IDLE, this.__ejecutar_agregar_elemento, items, null);
        this.__ejecutar_agregar_elemento(items);
        }

    public void seleccionar_siguiente(){
        Gtk.TreeModel modelo;
        Gtk.TreeIter _iter;
        this.get_selection().get_selected(out modelo, out _iter);
        bool val = modelo.iter_next(ref _iter);
        if (val){
            this.get_selection().select_iter(_iter);
            }
        else{
            if (this._len_items == 1){
                this.nueva_seleccion(this.valor_select);
                }
            else{
                this.seleccionar_primero();
                }
            }
        }

    public void seleccionar_anterior(){
        Gtk.TreeModel modelo;
        Gtk.TreeIter _iter;
        this.get_selection().get_selected(out modelo, out _iter);
        if (modelo.iter_previous(ref _iter)){
            this.get_selection().select_iter(_iter);
            }
        else{
            this.seleccionar_ultimo();
            }
        }

    public void seleccionar_primero(){
        //this.get_selection().select_path(new Gtk.TreePath.first());
        Gtk.TreeIter _iter;
        this.get_model().get_iter_first(out _iter);
        //this.get_selection().select_path(this.get_model().get_path(_iter));
        this.get_selection().select_iter(_iter);
        }

    public void seleccionar_ultimo(){
        Gtk.TreeModel modelo;
        Gtk.TreeIter _iter;
        this.get_selection().get_selected(out modelo, out _iter);
        Gtk.TreeIter _iter2;
        this.get_model().get_iter_first(out _iter2);
        while (modelo.iter_next(ref _iter)){
            _iter2 = _iter;
            }
        this.get_selection().select_iter(_iter2);
        }
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


public class MenuList : Gtk.Menu{

    public signal void accion (Lista lista, string accion, Gtk.TreePath path);

    public MenuList(Lista treeview, Gtk.TreePath path){

        Gtk.TreeIter _iter;
	    GLib.Value val3;

	    treeview.lista.get_iter(out _iter, path);
        treeview.lista.get_value(_iter, 2, out val3);

        Gtk.MenuItem item1 = new Gtk.MenuItem.with_label("Quitar de la Lista");
        item1.activate.connect (() => {
			this.__emit_accion(treeview, path, "Quitar");
		    });
        this.append(item1);

        string uri = val3.get_string();
        bool isfile = GLib.FileUtils.test(uri, GLib.FileTest.IS_REGULAR);
        GLib.File my_files_directory = GLib.File.parse_name(get_my_files_directory());

        if (isfile == true){
            GLib.File file = GLib.File.parse_name(uri);
            if (file.get_parent() != my_files_directory){
                Gtk.MenuItem item2 = new Gtk.MenuItem.with_label("Copiar a JAMedia");
                item2.activate.connect (() => {
			        this.__emit_accion(treeview, path, "Copiar");
		            });
                this.append(item2);

                Gtk.MenuItem item3 = new Gtk.MenuItem.with_label("Mover a JAMedia");
                item3.activate.connect (() => {
			        this.__emit_accion(treeview, path, "Mover");
		            });
                this.append(item3);
                }
            Gtk.MenuItem item4 = new Gtk.MenuItem.with_label("Borrar el Archivo");
            item4.activate.connect (() => {
                this.__emit_accion(treeview, path, "Borrar");
                });
            this.append(item4);
            }
        else{
            Gtk.MenuItem item5 = new Gtk.MenuItem.with_label("Borrar Streaming");
            item5.activate.connect (() => {
                this.__emit_accion(treeview, path, "Borrar");
                });
            this.append(item5);

            string data = get_data_directory();

            string a = GLib.Path.build_filename(data, "JAMediaRadio.JAMedia");
            string b = GLib.Path.build_filename(data, "JAMediaTV.JAMedia");
            string c = GLib.Path.build_filename(data, "MisRadios.JAMedia");
            string d = GLib.Path.build_filename(data, "MisTvs.JAMedia");
            //string e = GLib.Path.build_filename(data, "JAMediaWebCams.JAMedia");

            bool jtv = stream_en_archivo(uri, b);
            bool jr = stream_en_archivo(uri, a);
            bool r = stream_en_archivo(uri, c);
            bool tv = stream_en_archivo(uri, d);
            // webcam = stream_en_archivo(uri, listas[4])

            if ((jtv && ! tv) || (jr && ! r)){
                Gtk.MenuItem item6 = new Gtk.MenuItem.with_label("Copiar a JAMedia");
                item6.activate.connect (() => {
                    this.__emit_accion(treeview, path, "Copiar");
                    });
                this.append(item6);

                Gtk.MenuItem item7 = new Gtk.MenuItem.with_label("Mover a JAMedia");
                item7.activate.connect (() => {
                    this.__emit_accion(treeview, path, "Mover");
                    });
                this.append(item7);
                }

            Gtk.MenuItem item8 = new Gtk.MenuItem.with_label("Grabar");
            item8.activate.connect (() => {
                this.__emit_accion(treeview, path, "Grabar");
                });
            this.append(item8);
            }

        this.popup(null, null, null, 1, Gtk.get_current_event_time());
        this.show_all();
        this.attach_to_widget(treeview, null);
    }

    private void __emit_accion(Lista treeview, Gtk.TreePath path, string accion){
        this.accion(treeview, accion, path);
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
