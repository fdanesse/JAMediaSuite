
public class PlayerList : Gtk.Frame{
    /*
    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "accion-list": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    "menu_activo": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "add_stream": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}
    */
    private Lista lista = new Lista();
    private JAMediaToolbarList toolbar = new JAMediaToolbarList();

    public PlayerList(){

        //self.directorio = get_JAMedia_Directory()

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

        /*
        self.toolbar.connect("cargar_lista", self.cargar_lista)
        self.toolbar.connect("add_stream", self.__emit_add_stream)
        self.toolbar.connect("menu_activo", self.__emit_menu_activo)

        self.lista.connect("nueva-seleccion", self.__emit_nueva_seleccion)
        self.lista.connect("button-press-event", self.__click_derecho_en_lista)
        */
    }
}


public class Lista : Gtk.TreeView{
    /*
    __gsignals__ = {
    "nueva-seleccion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, ))}
    */

    private Gtk.ListStore lista = new Gtk.ListStore(3, typeof (Gdk.Pixbuf), typeof (string), typeof (string));

    public Lista(){

        this.set_model(this.lista);

        this.set("rules-hint", true);
        this.set("headers_clickable", true);
        this.set("headers_visible", true);
        /*
        self.permitir_select = True
        self.valor_select = False
        self.ultimo_select = False
        */
        this.__setear_columnas();

        //self.get_selection().set_select_function(self.__selecciones, self.get_model())

        this.show_all();

        // FIXME: Ejemplo para agregar elementos a la lista
        //Gtk.TreeIter iter;
        //this.lista.append (out iter);
        //Gdk.Pixbuf pix = new Gdk.Pixbuf.from_file_at_size("Iconos/JAMedia.svg", 24, 24);
        //this.lista.set (iter, 0, pix, 1, "Hola", 2, "URL");
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
}


public class JAMediaToolbarList : Gtk.EventBox{
    /*
    __gsignals__ = {
    "cargar_lista": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "add_stream": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "menu_activo": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, [])}
    */

    public JAMediaToolbarList(){

        //self.ip = False

        Gtk.Toolbar toolbar = new Gtk.Toolbar();
        /*
        self.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        toolbar.modify_bg(gtk.STATE_NORMAL, get_colors("toolbars"))
        */

        Gtk.ToolButton button1 = get_button("Iconos/lista.svg", false, Gdk.PixbufRotation.NONE, 24, "Selecciona una Lista");
		//button1.clicked.connect (() => {
		//	this.__get_menu();
		//});
		toolbar.insert(button1, -1);

		Gtk.SeparatorToolItem separador1 = get_separador(false, 3, false);
        toolbar.insert(separador1, -1);

        Gtk.ToolItem item = new Gtk.ToolItem();
        Gtk.Label label = new Gtk.Label("");
        label.show();
        item.add(label);
        toolbar.insert(item, -1);

        Gtk.SeparatorToolItem separador2 = get_separador(false, 0, true);
        toolbar.insert(separador2, -1);

        Gtk.ToolButton button2 = get_button("Iconos/agregar.svg", false, Gdk.PixbufRotation.NONE, 24, "Agregar Streaming");
		//button1.clicked.connect (() => {
		//	this.__emit_add_stream();
		//});
		toolbar.insert(button2, -1);

        this.add(toolbar);
        this.show_all();
    }
    /*
    def __get_menu(self, widget):
        self.emit("menu_activo")
        menu = gtk.Menu()

        if self.ip:
            item = gtk.MenuItem("JAMedia Radio")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 0)

            item = gtk.MenuItem("JAMedia TV")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 1)

            item = gtk.MenuItem("Mis Emisoras")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 2)

            item = gtk.MenuItem("Mis Canales")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 3)

            item = gtk.MenuItem("Web Cams")
            menu.append(item)
            item.connect_object("activate", self.__emit_load_list, 4)

        item = gtk.MenuItem("Mis Archivos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 5)

        item = gtk.MenuItem("JAMediaTube")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 6)

        item = gtk.MenuItem("Audio-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 7)

        item = gtk.MenuItem("Video-JAMediaVideo")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 8)

        item = gtk.MenuItem("Archivos Externos")
        menu.append(item)
        item.connect_object("activate", self.__emit_load_list, 9)

        menu.show_all()
        menu.attach_to_widget(widget, self.__null)
        gtk.Menu.popup(menu, None, None, None, 1, 0)

    def __null(self):
        pass

    def __emit_load_list(self, indice):
        self.emit("cargar_lista", indice)

    def __emit_add_stream(self, widget):
        self.emit("add_stream")
    */
}
