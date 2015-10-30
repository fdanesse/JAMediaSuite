public class Derecha : Gtk.EventBox{

    /*
    __gsignals__ = {
    "add_remove_efecto": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN)),
    'configurar_efecto': (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_STRING, gobject.TYPE_PYOBJECT))}
    */

    public signal void cargar_reproducir(string pista);
    public signal void accion_controls(string accion);
    public signal void add_stream(string title);
    public signal void menu_activo();
    public signal void balance_valor(string prop, double valor);
    public signal void accion_list (Lista lista, string accion, Gtk.TreePath path);

    private Gtk.ScrolledWindow scroll = new Gtk.ScrolledWindow(null, null);
    public BalanceWidget balance = new BalanceWidget();
    public JAMediaPlayerList lista = new JAMediaPlayerList();
    public PlayerControls player_controls = new PlayerControls();

    public Derecha(){

        Gtk.Box vbox = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
        Gtk.Box conf_box = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);

        //#self.efectos = VideoEfectos()
        //#conf_box.pack_start(self.efectos, True, True, 0)

        this.scroll.set("hscrollbar_policy", Gtk.PolicyType.NEVER);
        this.scroll.set("vscrollbar_policy", Gtk.PolicyType.AUTOMATIC);
        this.scroll.add_with_viewport(conf_box);

        vbox.pack_start(this.scroll, true, true, 0);
        vbox.pack_start(this.lista, true, true, 0);
        vbox.pack_end(this.player_controls, false, false, 0);

        conf_box.pack_start(this.balance, false, false, 0);

        this.add(vbox);
        this.show_all();

        this.balance.balance_valor.connect(this.__emit_balance);
        //#self.efectos.connect("click_efecto", self.__emit_add_remove_efecto)
        //#self.efectos.connect("configurar_efecto", self.__emit_config_efecto)

        this.lista.nueva_seleccion.connect(this.__emit_cargar_reproducir);
        this.lista.accion_list.connect(this.__emit_accion_list);
        this.lista.menu_activo.connect(this.__emit_menu_activo);
        this.lista.add_stream.connect(this.__emit_add_stream);
        this.lista.len_items.connect(this.__items_in_list);

        this.player_controls.accion_controls.connect(this.__emit_accion_controls);

        this.set_size_request(150, -1);
    }

    private void __items_in_list(int items){
        this.player_controls.activar(items);
        }

    private void __emit_balance(string prop, double valor){
        this.balance_valor(prop, valor);
        }

    private void __emit_accion_controls(string accion){
        this.accion_controls(accion);
        }

    private void __emit_add_stream(string title){
        this.add_stream(title);
        }

    private void __emit_menu_activo(){
        this.menu_activo();
        }

    private void __emit_accion_list(Lista lista, string accion, Gtk.TreePath path){
        // borrar, copiar, mover, grabar, etc . . .
        this.accion_list(lista, accion, path);
        }

    private void __emit_cargar_reproducir(string pista){
        this.cargar_reproducir(pista);
        }

    public void show_config(){
        if (this.scroll.get_visible() == true){
            this.scroll.hide();
            this.lista.show();
            this.player_controls.show();
            }
        else{
            this.scroll.show();
            this.lista.hide();
            this.player_controls.hide();
            }
        }

    public void setup_init(){
        this.scroll.hide();
        this.lista.setup_init();
        this.player_controls.activar(0);
        // self.efectos.cargar_efectos(list(get_jamedia_video_efectos()))
        }

    public void set_ip(bool valor){
        this.lista.set_ip(valor);
        }

    public void set_nueva_lista(SList<string> archivos){
        this.lista.set_nueva_lista(archivos);
        }
}
