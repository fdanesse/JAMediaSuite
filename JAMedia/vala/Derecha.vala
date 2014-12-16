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

    public signal void accion_controls(string accion);
    public signal void add_stream(string title);

    private Gtk.ScrolledWindow scroll = new Gtk.ScrolledWindow(null, null);
    private BalanceWidget balance = new BalanceWidget();
    public JAMediaPlayerList lista = new JAMediaPlayerList();
    private PlayerControls player_controls = new PlayerControls();

    public Derecha(){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
        Gtk.Box conf_box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        /*
        #self.efectos = VideoEfectos()
        self.lista = PlayerList()
        self.lista.set_mime_types(["audio/*", "video/*"])
        #conf_box.pack_start(self.efectos, True, True, 0)
        */

        this.scroll.set("hscrollbar_policy", Gtk.PolicyType.NEVER);
        this.scroll.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        this.scroll.add_with_viewport(conf_box);

        vbox.pack_start(this.scroll, true, true, 0);
        vbox.pack_start(this.lista, true, true, 0);
        vbox.pack_end(this.player_controls, false, false, 0);

        conf_box.pack_start(this.balance, false, false, 0);

        this.add(vbox);
        this.show_all();

        /*
        self.balance.connect("balance-valor", self.__emit_balance)
        #self.efectos.connect("click_efecto", self.__emit_add_remove_efecto)
        #self.efectos.connect("configurar_efecto", self.__emit_config_efecto)

        self.lista.connect("nueva-seleccion", self.__emit_cargar_reproducir)
        self.lista.connect("accion-list", self.__emit_accion_list)
        self.lista.connect("menu_activo", self.__emit_menu_activo)
        */
        this.lista.add_stream.connect(this.__emit_add_stream);

        this.player_controls.accion_controls.connect(this.__emit_accion_controls);

        this.set_size_request(150, -1);
    }

    /*
    def __emit_balance(self, widget, valor, prop):
        # brillo, contraste, saturación, hue, gamma
        self.emit('balance-valor', valor, prop)
    */

    private void __emit_accion_controls(string accion){
        // anterior, siguiente, pausa, play, stop
        this.accion_controls(accion);
        }

    private void __emit_add_stream(string title){
        // El usuario agregará una dirección de streaming
        this.add_stream(title);
        }
    /*
    def __emit_menu_activo(self, widget=False):
        # hay un menu contextual presente
        self.emit("menu_activo")

    def __emit_accion_list(self, widget, lista, accion, _iter):
        # borrar, copiar, mover, grabar, etc . . .
        self.emit("accion-list", lista, accion, _iter)

    def __emit_cargar_reproducir(self, widget, path):
        if path:
            self.player_controls.activar(True)
        else:
            self.player_controls.activar(False)
        self.emit("cargar-reproducir", path)

    def show_config(self):
        objs = self.get_child().get_children()
        valor = objs[0].get_visible()
        if valor:
            ocultar(objs[0])
            map(mostrar, objs[1:])
        else:
            mostrar(objs[0])
            map(ocultar, objs[1:])
    */

    public void setup_init(){
        this.scroll.hide();
        this.lista.setup_init();
        this.player_controls.activar(false);
        // self.efectos.cargar_efectos(list(get_jamedia_video_efectos()))
        }

    /*
    def set_ip(self, valor):
        self.lista.set_ip(valor)

    def set_nueva_lista(self, archivos):
        self.lista.set_nueva_lista(archivos)
    */
}
