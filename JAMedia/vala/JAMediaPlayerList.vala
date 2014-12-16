
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
    /*
    def __emit_add_stream(self, widget):
        # El usuario agregará una dirección de streaming
        self.emit("add_stream", self.toolbar.label.get_text())

    def __emit_menu_activo(self, widget=False):
        # hay un menu contextual presente
        self.emit("menu_activo")

    def __emit_accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.emit("accion-list", lista, accion, _iter)

    def __emit_nueva_seleccion(self, widget, pista):
        # item seleccionado en la lista
        self.emit('nueva-seleccion', pista)

    def __seleccionar_lista_de_stream(self, archivo, titulo):
        items = get_streamings(archivo)
        self.__load_list(items, "load", titulo)

    def __seleccionar_lista_de_archivos(self, directorio, titulo):
        archivos = sorted(os.listdir(directorio))
        lista = []
        for path in archivos:
            archivo = os.path.join(directorio, path)
            if os.path.isfile(archivo):
                lista.append(archivo)
        self.__load_files(False, lista, titulo)

    def __load_files(self, widget, archivos, titulo=False):
        items = []
        archivos.sort()
        for path in archivos:
            archivo = os.path.basename(path)
            items.append([archivo, path])
            self.directorio = os.path.dirname(path)
        self.__load_list(items, "load", titulo)
        # FIXME: Mostrar clear y add para agregar archivos a la lista

    def __load_list(self, items, tipo, titulo=False):
        if tipo == "load":
            self.lista.limpiar()
            self.emit("accion-list", False, "limpiar", False)
        if items:
            self.lista.agregar_items(items)
        else:
            self.emit('nueva-seleccion', False)
        if titulo != False:
            self.toolbar.label.set_text(titulo)

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

    def seleccionar_primero(self):
        self.lista.seleccionar_primero()

    def seleccionar_ultimo(self):
        self.lista.seleccionar_ultimo()
    */

    public void seleccionar_anterior(){
        this.lista.seleccionar_anterior();
        }

    public void seleccionar_siguiente(){
        this.lista.seleccionar_siguiente();
        }

    /*
    def select_valor(self, path_origen):
        self.lista.select_valor(path_origen)

    def limpiar(self):
        self.lista.limpiar()

    def set_mime_types(self, mime):
        self.mime = mime

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

    def setup_init(self):
        ocultar(self.toolbar.boton_agregar)

    def cargar_lista(self, widget, indice):
        _dict = {
            0: os.path.join(get_data_directory(), 'JAMediaRadio.JAMedia'),
            1: os.path.join(get_data_directory(), 'JAMediaTV.JAMedia'),
            2: os.path.join(get_data_directory(), 'MisRadios.JAMedia'),
            3: os.path.join(get_data_directory(), 'MisTvs.JAMedia'),
            4: os.path.join(get_data_directory(), 'JAMediaWebCams.JAMedia'),
            5: get_my_files_directory(),
            6: get_tube_directory(),
            7: get_audio_directory(),
            8: get_video_directory(),
            }
        ocultar(self.toolbar.boton_agregar)
        if indice == 0:
            self.__seleccionar_lista_de_stream(_dict[0], "JAM-Radio")
        elif indice == 1:
            self.__seleccionar_lista_de_stream(_dict[1], "JAM-TV")
        elif indice == 2:
            self.__seleccionar_lista_de_stream(_dict[2], "Radios")
            mostrar(self.toolbar.boton_agregar)
        elif indice == 3:
            self.__seleccionar_lista_de_stream(_dict[3], "TVs")
            mostrar(self.toolbar.boton_agregar)
        elif indice == 4:
            self.__seleccionar_lista_de_stream(_dict[4], "WebCams")
        elif indice == 5:
            self.__seleccionar_lista_de_archivos(_dict[indice], "Archivos")
        elif indice == 6:
            self.__seleccionar_lista_de_archivos(_dict[indice], "JAM-Tube")
        elif indice == 7:
            self.__seleccionar_lista_de_archivos(_dict[indice], "JAM-Audio")
        elif indice == 8:
            self.__seleccionar_lista_de_archivos(_dict[indice], "JAM-Video")
        elif indice == 9:
            selector = My_FileChooser(parent=self.get_toplevel(),
                filter_type=[], action=gtk.FILE_CHOOSER_ACTION_OPEN,
                mime=self.mime, title="Abrir Archivos", path=self.directorio)
            selector.connect('load-files', self.__load_files, "Archivos")
            selector.run()
            if selector:
                selector.destroy()

    def set_ip(self, valor):
        self.toolbar.ip = valor

    def set_nueva_lista(self, archivos):
        self.__load_files(False, archivos, titulo="Archivos")
    */
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

    def __ejecutar_agregar_elemento(self, elementos):
        self.permitir_select = False
        self.set_sensitive(False)
        if not elementos:
            self.permitir_select = True
            self.seleccionar_primero()
            self.set_sensitive(True)
            return False

        texto, path = elementos[0]
        descripcion = describe_uri(path)
        icono = os.path.join(BASE_PATH, "Iconos", "sonido.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 24, -1)

        if descripcion:
            if descripcion[2]:
                # Es un Archivo
                tipo = describe_archivo(path)
                if 'video' in tipo or 'application/ogg' in tipo:
                    icono = os.path.join(BASE_PATH, "Iconos", "video.svg")
                    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                        icono, 24, -1)
                elif 'audio' in tipo or 'application/octet-stream' in tipo:
                    pass
                else:
                    if "image" in tipo:
                        icono = path
                        try:
                            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                icono, 50, -1)
                        except:
                            icono = os.path.join(BASE_PATH,
                                "Iconos", "sonido.svg")
                            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                                icono, 24, -1)

        self.get_model().append([pixbuf, texto, path])
        elementos.remove(elementos[0])
        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)
        return False

    def limpiar(self):
        self.permitir_select = False
        self.get_model().clear()
        self.valor_select = False
        self.ultimo_select = False
        self.permitir_select = True

    def agregar_items(self, elementos):
        gobject.idle_add(self.__ejecutar_agregar_elemento, elementos)
    */
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
    /*
    def seleccionar_primero(self, widget=None):
        self.get_selection().select_path(0)

    def seleccionar_ultimo(self, widget=None):
        model = self.get_model()
        item = model.get_iter_first()
        _iter = None
        while item:
            _iter = item
            item = model.iter_next(item)
        if _iter:
            self.get_selection().select_iter(_iter)
            #path = model.get_path(iter)

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
