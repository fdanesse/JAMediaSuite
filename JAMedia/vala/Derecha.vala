public class Derecha : Gtk.EventBox{

    /*
    __gsignals__ = {
    "cargar-reproducir": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "accion-list": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)),
    "menu_activo": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "add_stream": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "accion-controls": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    'balance-valor': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,
        gobject.TYPE_STRING)),
    "add_remove_efecto": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN)),
    'configurar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}
    */

    public Derecha(){

        /*
        self.modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        vbox = gtk.VBox()
        conf_box = gtk.VBox()

        self.balance = BalanceWidget()
        #self.efectos = VideoEfectos()
        self.lista = PlayerList()
        self.lista.set_mime_types(["audio/*", "video/*"])
        self.player_controls = PlayerControls()

        conf_box.pack_start(self.balance, False, False, 0)
        #conf_box.pack_start(self.efectos, True, True, 0)

        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.add_with_viewport(conf_box)
        scroll.get_child().modify_bg(gtk.STATE_NORMAL, get_colors("window"))

        vbox.pack_start(scroll, True, True, 0)
        vbox.pack_start(self.lista, True, True, 0)
        vbox.pack_end(self.player_controls, False, False, 0)

        self.add(vbox)
        */

        this.show_all();

        /*
        self.balance.connect("balance-valor", self.__emit_balance)
        #self.efectos.connect("click_efecto", self.__emit_add_remove_efecto)
        #self.efectos.connect("configurar_efecto", self.__emit_config_efecto)

        self.lista.connect("nueva-seleccion", self.__emit_cargar_reproducir)
        self.lista.connect("accion-list", self.__emit_accion_list)
        self.lista.connect("menu_activo", self.__emit_menu_activo)
        self.lista.connect("add_stream", self.__emit_add_stream)

        self.player_controls.connect("accion-controls",
            self.__emit_accion_controls)
        */

        this.set_size_request(150, -1);
    }
}
